from fastapi import APIRouter

# Create the main API router
api_router = APIRouter()

# Import and include all endpoint routers
from app.api.v1.endpoints import health
from app.api.v1.endpoints import users
from app.api.v1.endpoints import api_keys
from app.api.v1.endpoints import analyze
from app.api.v1.endpoints import fix
from app.api.v1.endpoints import explain
from app.api.v1.endpoints import github
from app.api.v1.endpoints import agent_debug

# Health check endpoint
api_router.include_router(health.router, tags=["health"])

# User management
api_router.include_router(users.router, prefix="/users", tags=["users"])

# API key management
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])

# Code analysis
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])

# Error explanation
api_router.include_router(explain.router, prefix="/explain", tags=["explain"])

# Code fixing
api_router.include_router(fix.router, prefix="/fix", tags=["fix"])

# GitHub integration
api_router.include_router(github.router, prefix="/github", tags=["github"])

# Agent-based debugging
api_router.include_router(agent_debug.router, prefix="/agent", tags=["agent"])

# Try to import other endpoints, but don't fail if they don't exist yet
try:
    from app.api.v1.endpoints import users
    api_router.include_router(users.router, prefix="/users", tags=["users"])
except ImportError:
    pass

try:
    from app.api.v1.endpoints import api_keys
    api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])
except ImportError:
    pass

try:
    from app.api.v1.endpoints import analyze
    api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
except ImportError:
    pass

try:
    from app.api.v1.endpoints import fix
    api_router.include_router(fix.router, prefix="/fix", tags=["fix"])
except ImportError:
    pass

try:
    from app.api.v1.endpoints import explain
    api_router.include_router(explain.router, prefix="/explain", tags=["explain"])
except ImportError:
    pass

try:
    from app.api.v1.endpoints import github
    api_router.include_router(github.router, prefix="/github", tags=["github"])
except ImportError:
    pass 