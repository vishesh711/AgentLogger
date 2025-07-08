from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for updating a user
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    github_username: Optional[str] = None


# Schema for returning a user
class UserResponse(UserBase):
    id: str
    is_superuser: bool
    github_username: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True} 