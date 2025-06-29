import enum

from sqlalchemy import Column, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db.base import BaseModel


class AnalysisStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    """Analysis Request model for database"""
    __tablename__ = "analysis_requests"
    
    # Request details
    language = Column(String, nullable=False)
    code = Column(Text, nullable=False)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, nullable=False)
    
    # Analysis results
    issues = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="analysis_requests")
    fix_requests = relationship("FixRequest", back_populates="analysis_request", cascade="all, delete-orphan") 