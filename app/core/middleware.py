import time
from collections import defaultdict
from typing import Callable, Dict, Tuple

from fastapi import HTTPException, Request, Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS

from app.core.config import settings
from app.services.api_key_service import verify_api_key_service

# Simple in-memory rate limiter
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.window_size = 60  # 1 minute window
    
    def is_rate_limited(self, key: str) -> bool:
        """
        Check if a key is rate limited based on requests in the last minute
        """
        current_time = time.time()
        
        # Remove requests older than the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < self.window_size
        ]
        
        # Check if the number of requests exceeds the limit
        if len(self.requests[key]) >= settings.RATE_LIMIT_PER_MINUTE:
            return True
        
        # Add the current request
        self.requests[key].append(current_time)
        return False


# Initialize the rate limiter
rate_limiter = RateLimiter()


async def api_key_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to verify API key for protected routes
    """
    # Skip API key verification for docs, redoc, and health check
    if request.url.path in ["/docs", "/redoc", "/openapi.json", f"{settings.API_V1_STR}/health"]:
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide a valid API key in the X-API-Key header.",
        )
    
    # Verify the API key
    user_id = await verify_api_key_service(api_key)
    
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid API key. Please provide a valid API key.",
        )
    
    # Add the user_id to the request state
    request.state.user_id = user_id
    
    return await call_next(request)


async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to implement rate limiting
    """
    # Skip rate limiting for docs, redoc, and health check
    if request.url.path in ["/docs", "/redoc", "/openapi.json", f"{settings.API_V1_STR}/health"]:
        return await call_next(request)
    
    # Use API key or IP address as the rate limit key
    rate_limit_key = request.headers.get("X-API-Key", request.client.host)
    
    if rate_limiter.is_rate_limited(rate_limit_key):
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_PER_MINUTE} requests per minute allowed.",
        )
    
    return await call_next(request) 