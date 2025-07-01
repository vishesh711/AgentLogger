from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

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
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Create a new API key
    
    The API key will only be shown once in the response.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # Create the API key with user_id as separate parameter
    return create_api_key(db, api_key_data, user_id)


@router.get("/{api_key_id}", response_model=ApiKeyResponse)
async def get_api_key_by_id(
    api_key_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get a specific API key by ID
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    db_api_key = get_api_key(db, api_key_id)
    if not db_api_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    # Verify that the API key belongs to the current user
    if str(db_api_key.user_id) != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Access denied to this API key",
        )
    
    return db_api_key


@router.get("/", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get all API keys for the current user
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # Use the user_id as string directly
    return get_api_keys_by_user(db, user_id)


@router.put("/{api_key_id}", response_model=ApiKeyResponse)
async def update_api_key_data(
    api_key_id: UUID,
    api_key_data: ApiKeyUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Update an API key
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # First check if the API key exists and belongs to the user
    existing_key = get_api_key(db, api_key_id)
    if not existing_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    if str(existing_key.user_id) != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Access denied to this API key",
        )
    
    db_api_key = update_api_key(db, api_key_id, api_key_data)
    if not db_api_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    return db_api_key


@router.delete("/{api_key_id}")
async def delete_api_key_by_id(
    api_key_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Delete an API key
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # First check if the API key exists and belongs to the user
    existing_key = get_api_key(db, api_key_id)
    if not existing_key:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    if str(existing_key.user_id) != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Access denied to this API key",
        )
    
    success = delete_api_key(db, api_key_id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"API key with ID {api_key_id} not found",
        )
    
    return {"status": "success", "message": f"API key with ID {api_key_id} deleted"} 