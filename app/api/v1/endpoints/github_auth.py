import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from urllib.parse import urlencode

from app.core.config import settings
from app.core.db import get_db
from app.models.db.user import User
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()

GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET
GITHUB_REDIRECT_URI = settings.GITHUB_REDIRECT_URI

@router.get("/authorize")
async def github_authorize():
    """Redirect to GitHub OAuth authorization"""
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "repo user:email",
        "state": "random_state_string"  # In production, use a secure random state
    }
    
    auth_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.post("/callback")
async def github_callback(
    code: str,
    state: str,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Handle GitHub OAuth callback"""
    # Exchange code for access token
    token_data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data=token_data,
            headers={"Accept": "application/json"}
        )
        token_response.raise_for_status()
        token_json = token_response.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get GitHub access token"
        )
    
    # Get user info from GitHub
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        user_response.raise_for_status()
        github_user = user_response.json()
    
    # Update user with GitHub information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.github_username = github_user.get("login")
    user.github_access_token = access_token
    db.commit()
    
    return {
        "message": "GitHub account connected successfully",
        "github_username": github_user.get("login"),
        "github_user_id": github_user.get("id")
    }

@router.get("/repositories")
async def get_user_repositories(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's GitHub repositories"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.github_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub account not connected"
        )
    
    async with httpx.AsyncClient() as client:
        repos_response = await client.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {user.github_access_token}"},
            params={"sort": "updated", "per_page": 100}
        )
        repos_response.raise_for_status()
        repositories = repos_response.json()
    
    # Filter and format repository data
    formatted_repos = []
    for repo in repositories:
        formatted_repos.append({
            "id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo.get("description"),
            "language": repo.get("language"),
            "updated_at": repo["updated_at"],
            "html_url": repo["html_url"],
            "private": repo["private"]
        })
    
    return {"repositories": formatted_repos}

@router.post("/analyze-repository")
async def analyze_repository(
    repo_full_name: str,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Analyze a GitHub repository for issues"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.github_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub account not connected"
        )
    
    # This would integrate with the agent system to analyze the repository
    # For now, return a placeholder
    return {
        "message": f"Repository analysis started for {repo_full_name}",
        "status": "in_progress",
        "repository": repo_full_name
    } 