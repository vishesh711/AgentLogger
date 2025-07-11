from fastapi import APIRouter

# Create the main API router
api_router = APIRouter(prefix="/api/v1")

# Import and include all endpoint routers
from app.api.v1.endpoints import (
    analyze,
    fix,
    explain,
    patch,
    health,
    users,
    api_keys,
    github,
    agent_debug,
    auth,
    github_auth,
    google_auth,
)

# Health check endpoint
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# GitHub OAuth endpoints  
api_router.include_router(github_auth.router, prefix="/auth/github", tags=["github-auth"])

# Google OAuth endpoints  
api_router.include_router(google_auth.router, prefix="/auth/google", tags=["google-auth"])

# User management
api_router.include_router(users.router, prefix="/users", tags=["users"])

# API key management
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])

# Core agent-powered functionality
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(explain.router, prefix="/explain", tags=["explain"])
api_router.include_router(fix.router, prefix="/fix", tags=["fix"])
api_router.include_router(patch.router, prefix="/patch", tags=["patch"])

# GitHub integration
api_router.include_router(github.router, prefix="/github", tags=["github"])

# Agent debugging and testing
api_router.include_router(agent_debug.router, prefix="/agent-debug", tags=["agent-debug"]) 