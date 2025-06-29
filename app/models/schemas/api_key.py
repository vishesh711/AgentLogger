from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Base API Key Schema
class ApiKeyBase(BaseModel):
    """Base schema for API keys"""
    name: str = Field(..., description="Name of the API key")
    description: Optional[str] = Field(None, description="Description of the API key")


# Schema for creating a new API key
class ApiKeyCreate(ApiKeyBase):
    """Schema for creating a new API key"""
    expires_in_days: Optional[int] = Field(None, description="Number of days until the key expires")


# Schema for updating an API key
class ApiKeyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


# Schema for returning an API key
class ApiKeyResponse(ApiKeyBase):
    """Schema for API key response"""
    id: str = Field(..., description="Unique identifier for the API key")
    is_active: bool = Field(..., description="Whether the API key is active")
    created_at: datetime = Field(..., description="When the API key was created")
    expires_at: Optional[datetime] = Field(None, description="When the API key expires")
    user_id: str = Field(..., description="ID of the user who owns the API key")

    model_config = {"from_attributes": True}


# Schema for API key creation response
class ApiKeyCreateResponse(BaseModel):
    key: str = Field(..., description="The API key (only shown once)")
    id: UUID
    name: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime 