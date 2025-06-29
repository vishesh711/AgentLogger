from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Base API Key Schema
class ApiKeyBase(BaseModel):
    name: Optional[str] = None
    is_active: bool = True
    expires_at: Optional[datetime] = None


# Schema for creating a new API key
class ApiKeyCreate(ApiKeyBase):
    user_id: UUID


# Schema for updating an API key
class ApiKeyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


# Schema for returning an API key
class ApiKeyResponse(ApiKeyBase):
    id: UUID
    key: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for API key creation response
class ApiKeyCreateResponse(BaseModel):
    key: str = Field(..., description="The API key (only shown once)")
    id: UUID
    name: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime 