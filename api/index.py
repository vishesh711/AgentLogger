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

# For Vercel serverless functions, we need to handle the app directly
# The app is already configured with all routes and middleware in app.main
# We don't need to create a new app or mount anything

# Export the app as the handler
def handler(request, context):
    return app(request, context)

# Also export as 'app' for compatibility
__all__ = ["app", "handler"]
