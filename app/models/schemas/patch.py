from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class PatchRequest(BaseModel):
    """Schema for patch generation request"""
    original_code: str = Field(..., description="The original code with the issue")
    language: str = Field(..., description="The programming language of the code")
    issue_description: str = Field(..., description="Description of the issue to fix")
    context: Optional[str] = Field(None, description="Additional context about the code or issue")


class PatchResponse(BaseModel):
    """Schema for patch generation response"""
    patch: str = Field(..., description="The generated patch in unified diff format")
    explanation: str = Field(..., description="Explanation of what the patch does")
    can_auto_apply: bool = Field(..., description="Whether the patch can be automatically applied")
    
    model_config = {"from_attributes": True} 