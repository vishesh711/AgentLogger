import enum
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from app.models.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.db.user import User
    from app.models.db.analysis import AnalysisRequest
    from app.models.db.github import GitHubPR


class FixStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FixRequest(BaseModel):
    """
    Model for code fix requests
    """
    __tablename__ = "fix_requests"
    
    # User who requested the fix
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship("User", back_populates="fix_requests")
    
    # Related analysis request - Changed from UUID to String for compatibility
    analysis_id = Column(String, ForeignKey("analysis_requests.id"), nullable=True)
    analysis: Mapped[Optional["AnalysisRequest"]] = relationship("AnalysisRequest", back_populates="fix_requests")
    
    # Code to fix
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    error_message = Column(Text, nullable=True)
    context = Column(Text, nullable=True)
    
    # Fix result
    fixed_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    status: FixStatus = Column(Enum(FixStatus), nullable=False, default=FixStatus.PENDING)
    validation_message = Column(Text, nullable=True)
    
    # Agent system tracking
    session_id = Column(String, nullable=True)  # Track agent system session
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # GitHub PR info with proper type annotation
    github_prs: Mapped[List["GitHubPR"]] = relationship("GitHubPR", back_populates="fix_request", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<FixRequest(id='{self.id}', user_id='{self.user_id}', status='{self.status}')>" 