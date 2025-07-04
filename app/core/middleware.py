import time
import jwt
from typing import Dict, Callable, Any
from collections import defaultdict

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal
from app.services.api_key_service import validate_api_key
from app.services.monitoring_service import monitoring_service


class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.window_size = 60  # 1 minute window in seconds
    
    def is_rate_limited(self, key: str) -> bool:
        """
        Check if a given key has exceeded the rate limit
        """
        current_time = time.time()
        
        # Remove old requests outside the time window
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
        client_host = request.client.host if request.client else "unknown"
        client_id = request.headers.get("X-API-Key") or client_host
        
        # Skip rate limiting for certain paths
        if request.url.path in ["/api/v1/health", "/api/v1/health/health", "/docs", "/redoc", "/openapi.json"]:
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
    Middleware for API key and JWT token authentication
    """
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.public_paths = [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/api/v1/docs",
            "/api/v1/redoc", 
            "/api/v1/openapi.json",
            "/api/v1/health",
            "/api/v1/health/health",
            "/api/v1/auth/register",
            "/api/v1/auth/login",
            "/api/v1/auth/github",
            "/api/v1/auth/google",
            "/",
            "/favicon.ico",
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip authentication for public paths
        request_path = request.url.path
        for path in self.public_paths:
            # Exact match or prefix match (but not for root "/" to avoid matching everything)
            if request_path == path or (path != "/" and request_path.startswith(path)):
                return await call_next(request)
        
        # Try JWT token first
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("sub")
                if user_id:
                    request.state.user_id = user_id
                    return await call_next(request)
            except jwt.PyJWTError as e:
                pass  # Fall back to API key authentication
        
        # Fall back to API key authentication
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required. Provide either a valid API key or JWT token."},
            )
        
        # Create database session for validation
        db = SessionLocal()
        
        try:
            # Validate API key
            user_id = await validate_api_key(api_key, db)
            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API key"},
                )
            
            # Store user_id in request state
            request.state.user_id = user_id
            
            # Continue with the request
            return await call_next(request)
        finally:
            # Always close the database session
            db.close()


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for tracking API usage
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip analytics for non-API paths
        if not request.url.path.startswith("/api/v1/"):
            return await call_next(request)
        
        # Start timer
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Get endpoint and status code
        endpoint = request.url.path
        status_code = response.status_code
        
        # Get user_id if available
        user_id = getattr(request.state, "user_id", "anonymous")
        
        # Track API call
        metadata = {
            "method": request.method,
            "query_params": dict(request.query_params),
        }
        
        await monitoring_service.track_api_call(
            endpoint=endpoint,
            user_id=user_id,
            duration_ms=duration_ms,
            status_code=status_code,
            metadata=metadata
        )
        
        return response


def add_middlewares(app: FastAPI) -> None:
    """
    Add middlewares to the FastAPI app
    """
    # Add analytics middleware
    app.add_middleware(AnalyticsMiddleware)
    
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