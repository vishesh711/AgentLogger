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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import time

# Create a minimal FastAPI app for Vercel
app = FastAPI(
    title="AgentLogger API",
    description="AI-powered code debugging and fixing service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://agentlogger.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic models
class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    environment: str

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    file_path: str = None

class CodeAnalysisResponse(BaseModel):
    message: str
    issues: list = []
    status: str = "success"

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AgentLogger API - Vercel Deployment",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        timestamp=time.time(),
        version="0.1.0",
        environment=os.getenv("ENVIRONMENT", "production")
    )

# Simple analyze endpoint for testing
@app.post("/v1/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    try:
        # Simple mock analysis for now
        issues = []
        
        # Basic syntax checks
        if request.language.lower() == "python":
            if "print(" not in request.code and "def " not in request.code and "class " not in request.code:
                issues.append({
                    "type": "warning",
                    "message": "Code appears to be incomplete or missing main functionality",
                    "severity": "medium",
                    "line": 1
                })
        
        return CodeAnalysisResponse(
            message=f"Analysis completed for {request.language} code",
            issues=issues,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Export the app
__all__ = ["app"] 