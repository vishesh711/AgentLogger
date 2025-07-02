import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from urllib.parse import urlencode
from uuid import uuid4
from datetime import timedelta
from typing import Optional

from app.core.config import settings
from app.core.db import get_db
from app.models.db.user import User
from app.api.v1.endpoints.auth import create_access_token

router = APIRouter()

# Google OAuth configuration
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID if hasattr(settings, 'GOOGLE_CLIENT_ID') else ""
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET if hasattr(settings, 'GOOGLE_CLIENT_SECRET') else ""
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI if hasattr(settings, 'GOOGLE_REDIRECT_URI') else "http://localhost:8000/api/v1/auth/google/callback"

@router.get("/authorize")
async def google_authorize():
    """Redirect to Google OAuth authorization"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.get("/callback")
async def google_callback(
    code: str,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    # Exchange code for access token
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data=token_data,
            headers={"Accept": "application/json"}
        )
        token_response.raise_for_status()
        token_json = token_response.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get Google access token"
        )
    
    # Get user info from Google
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_response.raise_for_status()
        google_user = user_response.json()
    
    # Find or create user
    user_email = google_user.get("email")
    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        # Create new user
        user = User(
            id=str(uuid4()),
            email=user_email,
            full_name=google_user.get("name"),
            is_active=True
        )
        db.add(user)
    else:
        # Update existing user
        if not user.full_name and google_user.get("name"):
            user.full_name = google_user.get("name")
    
    db.commit()
    db.refresh(user)
    
    # Create access token for the user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "message": "Google authentication successful",
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "github_username": user.github_username
        }
    } 