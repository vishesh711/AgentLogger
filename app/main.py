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
from app.core.dependencies import get_agent_system, cleanup_agent_system

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
        # Initialize the agent system (this will start it automatically)
        agent_sys = get_agent_system()
        logger.info("Agent system initialized and starting")
        
        # Give the agent system a moment to start
        await asyncio.sleep(1)
        
        if agent_sys.running:
            logger.info("Agent system started successfully")
        else:
            logger.warning("Agent system may not have started properly")
            
    except Exception as e:
        logger.error(f"Failed to start agent system: {str(e)}")
    
    yield
    
    # Shutdown
    try:
        await cleanup_agent_system()
        logger.info("Agent system stopped")
    except Exception as e:
        logger.error(f"Error stopping agent system: {str(e)}")

# Create FastAPI app
app = FastAPI(
    title="AgentLogger API",
    description="AI-powered code debugging and fixing service with multi-agent architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middlewares
add_middlewares(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AgentLogger API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        agent_sys = get_agent_system()
        agent_status = "running" if agent_sys.running else "stopped"
        agent_count = len(agent_sys.agents)
    except Exception as e:
        agent_status = f"error: {str(e)}"
        agent_count = 0
    
    return {
        "status": "ok",
        "timestamp": time.time(),
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "agent_system": {
            "status": agent_status,
            "agent_count": agent_count
        }
    }

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AgentLogger API",
        version="0.1.0",
        description="AI-powered debugging assistant with multi-agent architecture",
        routes=app.routes,
    )
    
    # Add API key security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Apply security to all routes
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Set the custom OpenAPI schema
app.openapi_schema = custom_openapi()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 