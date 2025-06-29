from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.models.db.base import BaseModel


class User(BaseModel):
    """User model for database"""
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    analysis_requests = relationship("AnalysisRequest", back_populates="user", cascade="all, delete-orphan")
    fix_requests = relationship("FixRequest", back_populates="user", cascade="all, delete-orphan") 