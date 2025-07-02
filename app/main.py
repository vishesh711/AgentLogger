from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os
import logging
from fastapi.openapi.utils import get_openapi
import sentry_sdk
import asyncio

from app.core.config import settings
from app.core.middleware import add_middlewares
from app.api.v1.router import api_router
from app.core.dependencies import get_agent_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("agentlogger")

# Initialize Sentry if DSN is provided
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        
        # Enable performance monitoring
        enable_tracing=True,
    )
    logger.info("Sentry integration enabled")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of the application"""
    # Startup
    try:
        agent_sys = get_agent_system()
        # Start the agent system in the background
        asyncio.create_task(agent_sys.start())
        logger.info("Agent system started")
    except Exception as e:
        logger.error(f"Failed to start agent system: {str(e)}")
    
    yield
    
    # Shutdown
    try:
        agent_sys = get_agent_system()
        await agent_sys.stop()
        logger.info("Agent system stopped")
    except Exception:
        pass

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered debugging service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
cors_origins = [str(origin) for origin in settings.CORS_ORIGINS] if settings.CORS_ORIGINS else []

# Add development origins if not already present
dev_origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Default Vite port
    "http://localhost:8080", 
    "http://localhost:8081",  # Alternative Vite port
    "http://localhost:8082",  # Current Vite port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

for origin in dev_origins:
    if origin not in cors_origins:
        cors_origins.append(origin)

if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add custom middleware
add_middlewares(app)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request to {request.url.path} took {process_time:.3f}s")
    return response

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "Welcome to AgentLogger API"}

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the exception
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Capture exception in Sentry if enabled
    if settings.SENTRY_DSN:
        sentry_sdk.capture_exception(exc)
    
    # Return a generic error response
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
    )

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="AI-powered debugging service",
        routes=app.routes,
    )
    
    # Add security scheme for API key
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Apply security to all routes
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Set the custom openapi function
app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 