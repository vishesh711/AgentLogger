import enum
from typing import List, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, JSON, String, Text, DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from app.models.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.db.user import User
    from app.models.db.fix import FixRequest


class AnalysisStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    """
    Model for code analysis requests
    """
    __tablename__ = "analysis_requests"
    
    # Code details
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    
    # Analysis results
    status = Column(String, nullable=False, default="pending")
    issues = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    
    # Agent system tracking
    session_id = Column(String, nullable=True)  # Track agent system session
    
    # Foreign keys
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships with proper type annotations
    user: Mapped["User"] = relationship("User", back_populates="analysis_requests")
    fix_requests: Mapped[List["FixRequest"]] = relationship("FixRequest", back_populates="analysis", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self) -> str:
        return f"<AnalysisRequest(id='{self.id}', user_id='{self.user_id}', status='{self.status}')>" 