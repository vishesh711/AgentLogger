import enum

from sqlalchemy import Column, Enum, String, Text, Integer
from sqlalchemy.orm import relationship

from app.models.db.base import BaseModel


class PRStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"


class GitHubPR(BaseModel):
    """GitHub Pull Request model for database"""
    __tablename__ = "github_prs"
    
    # Repository details
    owner = Column(String, nullable=False)
    repo = Column(String, nullable=False)
    
    # PR details
    pr_number = Column(Integer, nullable=True)
    pr_url = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    branch_name = Column(String, nullable=False)
    base_branch = Column(String, nullable=False, default="main")
    status = Column(Enum(PRStatus), default=PRStatus.OPEN, nullable=False)
    
    # Relationships
    fix_request = relationship("FixRequest", back_populates="github_pr", uselist=False) 