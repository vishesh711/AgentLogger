from typing import List
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped

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
    
    # Additional timestamp for last login
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships with proper type annotations
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    fix_requests: Mapped[List["FixRequest"]] = relationship("FixRequest", back_populates="user", cascade="all, delete-orphan")
    analysis_requests: Mapped[List["AnalysisRequest"]] = relationship("AnalysisRequest", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}')>" 