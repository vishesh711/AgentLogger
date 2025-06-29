from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.db.fix import FixStatus


# GitHub PR Schema for Fix Request
class GitHubPRRequest(BaseModel):
    owner: str = Field(..., description="GitHub repository owner")
    repo: str = Field(..., description="GitHub repository name")
    base_branch: str = Field("main", description="Base branch to create PR against")
    title: str = Field(..., description="PR title")
    description: Optional[str] = Field(None, description="PR description")
    file_path: str = Field(..., description="Path to the file to be fixed")


# Base Fix Request Schema
class FixRequestBase(BaseModel):
    issue_id: str = Field(..., description="ID of the issue to fix")
    create_pr: bool = Field(False, description="Whether to create a GitHub PR with the fix")
    github_pr: Optional[GitHubPRRequest] = Field(None, description="GitHub PR details if create_pr is True")


# Schema for creating a new fix request
class FixRequestCreate(FixRequestBase):
    analysis_id: UUID = Field(..., description="ID of the analysis request")


# Schema for returning a fix request
class FixRequestResponse(FixRequestBase):
    id: UUID
    status: FixStatus
    fixed_code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None
    pr_created: bool
    pr_url: Optional[str] = None
    user_id: UUID
    analysis_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for fix result
class FixResult(BaseModel):
    request_id: UUID
    status: FixStatus
    fixed_code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None
    pr_url: Optional[str] = None 