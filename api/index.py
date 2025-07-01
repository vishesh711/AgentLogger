from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main FastAPI app
from app.main import app as app_main

# Create a new app for Vercel
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the main app
app.mount("/api/v1", app_main)

@app.get("/api/health")
async def health():
    return {"status": "ok", "environment": "vercel"}

# Handle all requests
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return {"error": f"Path not found: {path_name}", "status_code": 404}

# Handler for Vercel serverless
def handler(request, context):
    return app(request, context)
