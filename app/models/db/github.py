import enum

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.models.db.base import BaseModel


class PRStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"


class GitHubPR(BaseModel):
    """
    Model for GitHub pull requests
    """
    __tablename__ = "github_prs"
    
    # PR details
    repo_name = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    pr_url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    
    # Foreign keys
    fix_id = Column(String, ForeignKey("fix_requests.id"), nullable=False)
    
    # Relationships with proper type annotations
    fix_request: Mapped["FixRequest"] = relationship("FixRequest", back_populates="github_prs")
    
    def __repr__(self) -> str:
        return f"<GitHubPR(id='{self.id}', repo='{self.repo_name}', pr_number={self.pr_number})>" 