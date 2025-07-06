import uuid
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.core.db import Base


class BaseModel(Base):
    """
    Base model for all database models
    """
    __abstract__ = True
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__class__.__table__.columns} 