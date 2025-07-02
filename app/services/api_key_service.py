from datetime import datetime, timedelta
from typing import Optional, List, Union
from uuid import UUID
import secrets

from sqlalchemy.orm import Session

from app.models.db.api_key import ApiKey
from app.models.db.user import User
from app.models.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyUpdate
from app.core.db import get_db


async def validate_api_key(api_key: str, db: Optional[Session] = None) -> Optional[str]:
    """
    Validate an API key and return the user ID if valid
    
    This is a convenience function that can create a database session
    if none is provided, or use the provided session
    
    Args:
        api_key: API key to validate
        db: Optional database session
        
    Returns:
        User ID if the key is valid, None otherwise
    """
    # If no database session provided, create one
    if db is None:
        from app.core.db import SessionLocal
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        # Verify the API key
        return verify_api_key_service(db, api_key)
    finally:
        # Close the database session only if we created it
        if should_close:
            db.close()


def create_api_key(
    db: Session, 
    api_key_data: ApiKeyCreate,
    user_id: str
) -> dict:
    """
    Create a new API key for a user
    
    Args:
        db: Database session
        api_key_data: API key data
        user_id: User ID who owns the API key
        
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
        user_id=user_id,
        expires_at=expires_at
    )
    
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    # Return the response matching ApiKeyCreateResponse schema
    return {
        "key": raw_api_key,  # The actual API key value (renamed from api_key)
        "id": db_api_key.id,
        "name": db_api_key.name,
        "expires_at": db_api_key.expires_at,
        "created_at": db_api_key.created_at
    }


def get_api_key(db: Session, api_key_id: str) -> Optional[ApiKey]:
    """
    Get an API key by ID
    """
    return db.query(ApiKey).filter(ApiKey.id == api_key_id).first()


def get_api_key_by_key(db: Session, key: str) -> Optional[ApiKey]:
    """
    Get an API key by the key string
    """
    return db.query(ApiKey).filter(ApiKey.key == key).first()


def get_api_keys(db: Session, user_id: str) -> List[ApiKeyResponse]:
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
            name=key.name or "",  # Ensure name is never None
            description=key.description,
            is_active=key.is_active,
            created_at=key.created_at,
            expires_at=key.expires_at,
            user_id=key.user_id
        )
        for key in db_api_keys
    ]


def get_api_keys_by_user(db: Session, user_id: str) -> List[ApiKeyResponse]:
    """
    Get all API keys for a user by user ID
    
    Args:
        db: Database session
        user_id: User ID to get keys for
        
    Returns:
        List of API key responses
    """
    # Convert to string if necessary for database query
    user_id_str = str(user_id)
    
    db_api_keys = db.query(ApiKey).filter(ApiKey.user_id == user_id_str).all()
    
    return [
        ApiKeyResponse(
            id=key.id,
            name=key.name or "",  # Ensure name is never None
            description=key.description,
            is_active=key.is_active,
            created_at=key.created_at,
            expires_at=key.expires_at,
            user_id=key.user_id
        )
        for key in db_api_keys
    ]


def update_api_key(db: Session, api_key_id: str, api_key_data: ApiKeyUpdate) -> Optional[ApiKey]:
    """
    Update an API key
    
    Args:
        db: Database session
        api_key_id: ID of the API key to update
        api_key_data: New API key data
        
    Returns:
        Updated API key or None if not found
    """
    db_api_key = get_api_key(db, api_key_id)
    if not db_api_key:
        return None
    
    # Update fields if provided
    if hasattr(api_key_data, 'name') and api_key_data.name is not None:
        db_api_key.name = api_key_data.name
    if hasattr(api_key_data, 'description') and api_key_data.description is not None:
        db_api_key.description = api_key_data.description
    if hasattr(api_key_data, 'is_active') and api_key_data.is_active is not None:
        db_api_key.is_active = api_key_data.is_active
    if hasattr(api_key_data, 'expires_in_days') and api_key_data.expires_in_days is not None:
        db_api_key.expires_at = datetime.utcnow() + timedelta(days=api_key_data.expires_in_days)
    
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


def delete_api_key(db: Session, api_key_id: str) -> bool:
    """
    Delete an API key
    
    Args:
        db: Database session
        api_key_id: ID of the API key to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_api_key = get_api_key(db, api_key_id)
    if not db_api_key:
        return False
    
    db.delete(db_api_key)
    db.commit()
    return True


def revoke_api_key(db: Session, key_id: str, user_id: str) -> bool:
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
    
    # MyPy might think this is assigning to Column, but it's actually setting the attribute value
    db_api_key.is_active = False  # type: ignore
    db.commit()
    
    return True


def verify_api_key_service(db: Session, api_key: str) -> Optional[str]:
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
    
    # Update last used timestamp - MyPy might think this is Column assignment, but it's setting the value
    db_api_key.last_used_at = datetime.utcnow()  # type: ignore
    db.commit()
    
    return str(db_api_key.user_id) 