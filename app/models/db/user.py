from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.db.base import BaseModel


class User(BaseModel):
    """
    Model for user accounts
    """
    __tablename__ = "users"
    
    # User details
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # GitHub integration
    github_username = Column(String, nullable=True)
    github_access_token = Column(String, nullable=True)
    
    # Relationships
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    fix_requests = relationship("FixRequest", back_populates="user", cascade="all, delete-orphan")
    analysis_requests = relationship("AnalysisRequest", back_populates="user", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>" 