from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.db.api_key import ApiKey
from app.models.schemas.api_key import ApiKeyCreate, ApiKeyUpdate


async def create_api_key(db: Session, api_key_data: ApiKeyCreate) -> ApiKey:
    """
    Create a new API key for a user
    """
    db_api_key = ApiKey(
        key=ApiKey.generate_key(),
        name=api_key_data.name,
        is_active=api_key_data.is_active,
        expires_at=api_key_data.expires_at or ApiKey.generate_expiry(),
        user_id=api_key_data.user_id,
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


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


async def get_api_keys_by_user(db: Session, user_id: UUID) -> List[ApiKey]:
    """
    Get all API keys for a user
    """
    return db.query(ApiKey).filter(ApiKey.user_id == user_id).all()


async def update_api_key(db: Session, api_key_id: UUID, api_key_data: ApiKeyUpdate) -> Optional[ApiKey]:
    """
    Update an API key
    """
    db_api_key = await get_api_key(db, api_key_id)
    if not db_api_key:
        return None
    
    update_data = api_key_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_api_key, field, value)
    
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


async def delete_api_key(db: Session, api_key_id: UUID) -> bool:
    """
    Delete an API key
    """
    db_api_key = await get_api_key(db, api_key_id)
    if not db_api_key:
        return False
    
    db.delete(db_api_key)
    db.commit()
    return True


async def update_last_used(db: Session, api_key: ApiKey) -> None:
    """
    Update the last_used_at timestamp for an API key
    """
    api_key.last_used_at = datetime.utcnow()
    db.commit()


async def verify_api_key_service(api_key: str) -> Optional[UUID]:
    """
    Verify an API key and return the user ID if valid
    
    This function is used by the API key middleware
    """
    # This is a placeholder for the actual implementation
    # In a real implementation, this would check the database
    # For now, we'll just return a dummy user ID if the key is not empty
    if api_key and len(api_key) > 10:
        # In the real implementation, we would:
        # 1. Get the API key from the database
        # 2. Check if it's active and not expired
        # 3. Update the last_used_at timestamp
        # 4. Return the user_id
        return UUID("00000000-0000-0000-0000-000000000000")
    return None 