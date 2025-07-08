import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from urllib.parse import urlencode
from typing import Optional

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

@router.get("/callback")
async def github_callback(
    code: str,
    state: Optional[str] = None,
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
    
    # Get user email from GitHub
    async with httpx.AsyncClient() as client:
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
        )
        email_response.raise_for_status()
        emails = email_response.json()
        primary_email = next((email['email'] for email in emails if email['primary']), None)
    
    # Find or create user
    user = db.query(User).filter(User.github_username == github_user.get("login")).first()
    if not user and primary_email:
        user = db.query(User).filter(User.email == primary_email).first()
    
    if not user:
        # Create new user
        from uuid import uuid4
        user = User(
            id=str(uuid4()),
            email=primary_email or f"{github_user.get('login')}@github.local",
            full_name=github_user.get("name") or github_user.get("login"),
            github_username=github_user.get("login"),
            github_access_token=access_token,
            is_active=True
        )
        db.add(user)
    else:
        # Update existing user
        user.github_username = github_user.get("login")
        user.github_access_token = access_token
        if not user.full_name and github_user.get("name"):
            user.full_name = github_user.get("name")
    
    db.commit()
    db.refresh(user)
    
    # Create access token for the user
    from app.api.v1.endpoints.auth import create_access_token
    from datetime import timedelta
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "message": "GitHub authentication successful",
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "github_username": user.github_username
        }
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