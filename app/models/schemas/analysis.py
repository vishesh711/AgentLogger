from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.db.analysis import AnalysisStatus


# Issue Schema
class CodeIssue(BaseModel):
    id: str
    type: str
    severity: str
    message: str
    line_start: int
    line_end: Optional[int] = None
    column_start: Optional[int] = None
    column_end: Optional[int] = None
    code_snippet: Optional[str] = None
    fix_suggestions: Optional[List[str]] = None


# Base Analysis Request Schema
class AnalysisRequestBase(BaseModel):
    language: str = Field(..., description="Programming language of the code (e.g., python, javascript)")
    code: str = Field(..., description="Code to analyze")


# Schema for creating a new analysis request
class AnalysisRequestCreate(AnalysisRequestBase):
    pass


# Schema for returning an analysis request
class AnalysisRequestResponse(AnalysisRequestBase):
    id: UUID
    status: AnalysisStatus
    issues: Optional[List[CodeIssue]] = None
    error: Optional[str] = None
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Schema for analysis result
class AnalysisResult(BaseModel):
    request_id: UUID
    status: AnalysisStatus
    issues: Optional[List[CodeIssue]] = None
    error: Optional[str] = None 