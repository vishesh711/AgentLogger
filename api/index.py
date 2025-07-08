import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Set environment for Vercel
os.environ.setdefault("ENVIRONMENT", "production")
os.environ.setdefault("USE_DOCKER_SANDBOX", "false")
os.environ.setdefault("USE_REDIS", "false")
os.environ.setdefault("ENABLE_ANALYTICS", "false")

# Set a dummy database URL if not provided (will use SQLite in production for Vercel)
if not os.environ.get("DATABASE_URL"):
    os.environ.setdefault("DATABASE_URL", "sqlite:///./agentlogger_vercel.db")

# Import the main FastAPI app
error_message = None
try:
    from app.main import app
except ImportError as import_error:
    # Fallback minimal app for debugging
    from fastapi import FastAPI
    error_message = str(import_error)
    app = FastAPI(title="AgentLogger API - Error")
    
    @app.get("/")
    async def error_root():
        return {"error": f"Import failed: {error_message}", "message": "Check Vercel logs for details"}
    
    @app.get("/health")
    async def error_health():
        return {"status": "error", "error": f"Import failed: {error_message}"}

# Export the app for Vercel
__all__ = ["app"]
