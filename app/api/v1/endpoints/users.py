from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.models.db.user import User
from app.models.schemas.user import UserResponse

router = APIRouter()

def get_user_id_from_request(request: Request) -> str:
    """Get the user ID from the request state"""
    return request.state.user_id

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    request_user_id: str = Depends(get_user_id_from_request),
    db: Session = Depends(get_db)
):
    """
    Get the current user based on the API key
    """
    user = db.query(User).filter(User.id == request_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100,
    request_user_id: str = Depends(get_user_id_from_request),
    db: Session = Depends(get_db)
):
    """
    Get all users (admin only)
    """
    # Check if user is admin
    user = db.query(User).filter(User.id == request_user_id).first()
    if not user or not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users 