from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from app.core.db import get_db
from app.models.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    create_user, get_user, get_user_by_email, 
    get_users, update_user, delete_user
)

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user
    """
    # Check if user with this email already exists
    db_user = await get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )
    
    return await create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific user by ID
    """
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    return db_user


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all users with pagination
    """
    return await get_users(db, skip, limit)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_data(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a user
    """
    db_user = await update_user(db, user_id, user_data)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    return db_user


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a user
    """
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    return {"status": "success", "message": f"User with ID {user_id} deleted"} 