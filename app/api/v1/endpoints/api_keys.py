from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.core.db import get_db
from app.models.schemas.api_key import (
    ApiKeyCreate, ApiKeyUpdate, ApiKeyResponse, ApiKeyCreateResponse
)
from app.services.api_key_service import (
    create_api_key, get_api_key, get_api_keys_by_user,
    update_api_key, delete_api_key
)

router = APIRouter()


@router.post("/", response_model=ApiKeyCreateResponse)
async def create_new_api_key(
    api_key_data: ApiKeyCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new API key
    
    The API key will only be shown once in the response.
    """
    return await create_api_key(db, api_key_data)


@router.get("/{api_key_id}", response_model=ApiKeyResponse)
async def get_api_key_by_id(
    api_key_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific API key by ID
    """
    db_api_key = await get_api_key(db, api_key_id)
    if not db_api_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    return db_api_key


@router.get("/user/{user_id}", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get all API keys for a user
    """
    return await get_api_keys_by_user(db, user_id)


@router.put("/{api_key_id}", response_model=ApiKeyResponse)
async def update_api_key_data(
    api_key_id: UUID,
    api_key_data: ApiKeyUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an API key
    """
    db_api_key = await update_api_key(db, api_key_id, api_key_data)
    if not db_api_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    return db_api_key


@router.delete("/{api_key_id}")
async def delete_api_key_by_id(
    api_key_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete an API key
    """
    success = await delete_api_key(db, api_key_id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    return {"status": "success", "message": f"API key with ID {api_key_id} deleted"} 