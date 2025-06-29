from fastapi import APIRouter

from app.api.v1.endpoints import analyze, fix, explain, github, health, users, api_keys

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(fix.router, prefix="/fix", tags=["fix"])
api_router.include_router(explain.router, prefix="/explain", tags=["explain"])
api_router.include_router(github.router, prefix="/github", tags=["github"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"]) 