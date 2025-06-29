from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID
import secrets

from sqlalchemy.orm import Session

from app.models.db.api_key import ApiKey
from app.models.db.user import User
from app.models.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyUpdate


async def create_api_key(
    db: Session, 
    api_key_data: ApiKeyCreate
) -> dict:
    """
    Create a new API key for a user
    
    Args:
        db: Database session
        api_key_data: API key data
        
    Returns:
        Dict with API key response and raw API key
    """
    # Generate a secure random API key
    raw_api_key = secrets.token_urlsafe(32)
    
    # Set expiration date if provided
    expires_at = None
    if api_key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=api_key_data.expires_in_days)
    
    # Create the API key
    db_api_key = ApiKey(
        key=raw_api_key,
        name=api_key_data.name,
        description=api_key_data.description,
        user_id=api_key_data.user_id,
        expires_at=expires_at
    )
    
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    # Return both the response and the raw key
    # The raw key will only be shown once to the user
    return {
        "id": db_api_key.id,
        "name": db_api_key.name,
        "description": db_api_key.description,
        "is_active": db_api_key.is_active,
        "created_at": db_api_key.created_at,
        "expires_at": db_api_key.expires_at,
        "user_id": db_api_key.user_id,
        "api_key": raw_api_key
    }


async def get_api_key(db: Session, api_key_id: UUID) -> Optional[ApiKey]:
    """
    Get an API key by ID
    """
    return db.query(ApiKey).filter(ApiKey.id == api_key_id).first()


async def get_api_key_by_key(db: Session, key: str) -> Optional[ApiKey]:
    """
    Get an API key by the key string
    """
    return db.query(ApiKey).filter(ApiKey.key == key).first()


async def get_api_keys(db: Session, user_id: str) -> list[ApiKeyResponse]:
    """
    Get all API keys for a user
    
    Args:
        db: Database session
        user_id: User ID to get keys for
        
    Returns:
        List of API key responses
    """
    db_api_keys = db.query(ApiKey).filter(ApiKey.user_id == user_id).all()
    
    return [
        ApiKeyResponse(
            id=key.id,
            name=key.name,
            description=key.description,
            is_active=key.is_active,
            created_at=key.created_at,
            expires_at=key.expires_at,
            user_id=key.user_id
        )
        for key in db_api_keys
    ]


async def get_api_keys_by_user(db: Session, user_id: UUID) -> List[ApiKeyResponse]:
    """
    Get all API keys for a user by user ID
    
    Args:
        db: Database session
        user_id: User ID to get keys for
        
    Returns:
        List of API key responses
    """
    db_api_keys = db.query(ApiKey).filter(ApiKey.user_id == user_id).all()
    
    return [
        ApiKeyResponse(
            id=key.id,
            name=key.name,
            description=key.description,
            is_active=key.is_active,
            created_at=key.created_at,
            expires_at=key.expires_at,
            user_id=key.user_id
        )
        for key in db_api_keys
    ]


async def update_api_key(db: Session, api_key_id: UUID, api_key_data: ApiKeyUpdate) -> Optional[ApiKey]:
    """
    Update an API key
    
    Args:
        db: Database session
        api_key_id: ID of the API key to update
        api_key_data: New API key data
        
    Returns:
        Updated API key or None if not found
    """
    db_api_key = await get_api_key(db, api_key_id)
    if not db_api_key:
        return None
    
    # Update fields if provided
    if api_key_data.name is not None:
        db_api_key.name = api_key_data.name
    if api_key_data.description is not None:
        db_api_key.description = api_key_data.description
    if api_key_data.is_active is not None:
        db_api_key.is_active = api_key_data.is_active
    if api_key_data.expires_in_days is not None:
        db_api_key.expires_at = datetime.utcnow() + timedelta(days=api_key_data.expires_in_days)
    
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


async def delete_api_key(db: Session, api_key_id: UUID) -> bool:
    """
    Delete an API key
    
    Args:
        db: Database session
        api_key_id: ID of the API key to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_api_key = await get_api_key(db, api_key_id)
    if not db_api_key:
        return False
    
    db.delete(db_api_key)
    db.commit()
    return True


async def revoke_api_key(db: Session, key_id: str, user_id: str) -> bool:
    """
    Revoke an API key
    
    Args:
        db: Database session
        key_id: API key ID to revoke
        user_id: User ID to verify ownership
        
    Returns:
        True if the key was revoked, False if not found or not owned by the user
    """
    db_api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == user_id
    ).first()
    
    if not db_api_key:
        return False
    
    db_api_key.is_active = False
    db.commit()
    
    return True


async def verify_api_key_service(db: Session, api_key: str) -> Optional[str]:
    """
    Verify an API key and return the user ID if valid
    
    Args:
        db: Database session
        api_key: API key to verify
        
    Returns:
        User ID if the key is valid, None otherwise
    """
    db_api_key = db.query(ApiKey).filter(
        ApiKey.key == api_key,
        ApiKey.is_active == True
    ).first()
    
    if not db_api_key:
        return None
    
    # Check if the key has expired
    if db_api_key.expires_at and db_api_key.expires_at < datetime.utcnow():
        return None
    
    # Update last used timestamp
    db_api_key.last_used_at = datetime.utcnow()
    db.commit()
    
    return db_api_key.user_id 