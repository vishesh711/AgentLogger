import secrets
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from app.models.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.db.user import User


class ApiKey(BaseModel):
    """
    Model for API keys
    """
    __tablename__ = "api_keys"
    
    # API key details
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Foreign keys - Changed from UUID to String to match users.id type
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships with proper type annotations
    user: Mapped["User"] = relationship("User", back_populates="api_keys")
    
    # Additional timestamps
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self) -> str:
        return f"<ApiKey(id='{self.id}', user_id='{self.user_id}')>"
    
    @property
    def is_expired(self) -> bool:
        """Check if the API key is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    @classmethod
    def generate_key(cls) -> str:
        """Generate a new API key"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def generate_expiry(cls, days: int = 365) -> datetime:
        """Generate an expiry date for the API key"""
        return datetime.utcnow() + timedelta(days=days) 