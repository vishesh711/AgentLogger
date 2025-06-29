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
    """Base schema for fix requests"""
    code: str = Field(..., description="The code with errors to fix")
    language: str = Field(..., description="The programming language of the code")
    error_message: Optional[str] = Field(None, description="The error message to fix")
    context: Optional[str] = Field(None, description="Additional context for the fix")


# Schema for creating a new fix request
class FixRequestCreate(FixRequestBase):
    """Schema for creating a fix request"""
    analysis_id: Optional[UUID] = Field(None, description="ID of the analysis request this fix is for")


# Schema for returning a fix request
class FixRequestResponse(FixRequestBase):
    """Schema for fix request response"""
    id: str = Field(..., description="The ID of the fix request")
    user_id: str = Field(..., description="The ID of the user who created the request")
    analysis_id: Optional[UUID] = Field(None, description="ID of the analysis request this fix is for")
    status: FixStatus = Field(..., description="Status of the fix request")
    fixed_code: Optional[str] = Field(None, description="The fixed code")
    explanation: Optional[str] = Field(None, description="Explanation of the fix")
    validation_message: Optional[str] = Field(None, description="Validation message for the fix")
    created_at: datetime = Field(..., description="When the request was created")
    completed_at: Optional[datetime] = Field(None, description="When the request was completed")
    
    model_config = {"from_attributes": True}


# Schema for fix result
class FixResult(BaseModel):
    request_id: UUID
    status: FixStatus
    fixed_code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None
    pr_url: Optional[str] = None


# Schema for updating a fix request
class FixRequestUpdate(BaseModel):
    """Schema for updating a fix request"""
    fixed_code: Optional[str] = Field(None, description="The fixed code")
    explanation: Optional[str] = Field(None, description="Explanation of the fix")
    status: Optional[str] = Field(None, description="Status of the fix request")
    validation_message: Optional[str] = Field(None, description="Validation message for the fix") 