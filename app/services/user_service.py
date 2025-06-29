from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.db.user import User
from app.models.schemas.user import UserCreate, UserUpdate


async def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user
    """
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        is_active=user_data.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user(db: Session, user_id: UUID) -> Optional[User]:
    """
    Get a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get all users with pagination
    """
    return db.query(User).offset(skip).limit(limit).all()


async def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
    """
    Update a user
    """
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


async def delete_user(db: Session, user_id: UUID) -> bool:
    """
    Delete a user
    """
    db_user = await get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True 