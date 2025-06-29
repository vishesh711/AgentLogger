import time
from collections import defaultdict
from typing import Callable, Dict, Tuple

from fastapi import HTTPException, Request, Response, FastAPI, status, Depends
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.db import get_db
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


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting API requests based on client IP or API key.
    """
    def __init__(self, app: FastAPI):
        super().__init__(app)
        # In a production environment, use Redis or another distributed cache
        self.cache: Dict[str, Dict] = {}
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client identifier (API key or IP)
        client_id = request.headers.get("X-API-Key") or request.client.host
        
        # Skip rate limiting for certain paths
        if request.url.path == "/api/v1/health":
            return await call_next(request)
        
        # Check rate limit
        current_time = time.time()
        if client_id in self.cache:
            request_history = self.cache[client_id]
            # Clean old requests
            request_history["timestamps"] = [
                ts for ts in request_history["timestamps"] 
                if current_time - ts < 60  # 1 minute window
            ]
            
            # Check if rate limit exceeded
            if len(request_history["timestamps"]) >= settings.RATE_LIMIT_PER_MINUTE:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
            
            # Add current request timestamp
            request_history["timestamps"].append(current_time)
        else:
            # First request from this client
            self.cache[client_id] = {"timestamps": [current_time]}
        
        # Process the request
        return await call_next(request)


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware for API key authentication.
    """
    def __init__(self, app: FastAPI):
        super().__init__(app)
        # Paths that don't require API key
        self.public_paths = {
            "/api/v1/health", 
            "/docs", 
            "/redoc", 
            "/openapi.json",
            "/api/v1/openapi.json"
        }
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip API key check for public paths
        path = request.url.path
        if any(path.startswith(public_path) for public_path in self.public_paths) or \
           any(path.endswith(public_path) for public_path in ["/openapi.json"]):
            return await call_next(request)
        
        # Check for API key
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing API key"}
            )
        
        # Get database session
        db = next(get_db())
        
        # Verify API key
        user_id = await verify_api_key_service(db, api_key)
        if not user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid API key"}
            )
        
        # Store user ID in request state
        request.state.user_id = user_id
        
        return await call_next(request)


def add_middleware(app: FastAPI) -> None:
    """
    Add all middleware to the FastAPI application.
    """
    # Add rate limiting middleware
    if settings.RATE_LIMIT_PER_MINUTE > 0:
        app.add_middleware(RateLimitMiddleware)
    
    # Add API key middleware
    app.add_middleware(APIKeyMiddleware)
    
    # Add timing middleware for debugging
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response 