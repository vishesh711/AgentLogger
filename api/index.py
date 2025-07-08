import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Set environment for Vercel
os.environ.setdefault("ENVIRONMENT", "production")

# Import the main FastAPI app
from app.main import app

# For Vercel serverless functions, we need to export the app directly
# The app is already configured with all routes and middleware in app.main

# Export the app for Vercel
__all__ = ["app"]
