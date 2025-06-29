import secrets
from datetime import datetime, timedelta

from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db.base import BaseModel


class ApiKey(BaseModel):
    """API Key model for database"""
    __tablename__ = "api_keys"
    
    key = Column(String, unique=True, index=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
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