import uuid
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
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
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name automatically from class name
        """
        return cls.__name__.lower() + "s"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 