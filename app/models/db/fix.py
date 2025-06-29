import enum

from sqlalchemy import Column, Enum, ForeignKey, JSON, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db.base import BaseModel


class FixStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FixRequest(BaseModel):
    """Fix Request model for database"""
    __tablename__ = "fix_requests"
    
    # Request details
    issue_id = Column(String, nullable=False)
    status = Column(Enum(FixStatus), default=FixStatus.PENDING, nullable=False)
    
    # Fix results
    fixed_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    
    # GitHub PR details
    create_pr = Column(Boolean, default=False, nullable=False)
    pr_created = Column(Boolean, default=False, nullable=False)
    pr_url = Column(String, nullable=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analysis_requests.id"), nullable=False)
    github_pr_id = Column(UUID(as_uuid=True), ForeignKey("github_prs.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="fix_requests")
    analysis_request = relationship("AnalysisRequest", back_populates="fix_requests")
    github_pr = relationship("GitHubPR", back_populates="fix_request", uselist=False) 