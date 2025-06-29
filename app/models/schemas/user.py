from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_active: bool = True


# Schema for creating a new user
class UserCreate(UserBase):
    pass


# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


# Schema for returning a user
class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 