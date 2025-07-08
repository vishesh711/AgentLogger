from typing import List, Optional
from pydantic import BaseModel, Field


class LearningResource(BaseModel):
    """Schema for a learning resource"""
    title: str = Field(..., description="Title of the resource")
    url: str = Field(..., description="URL of the resource")
    description: Optional[str] = Field(None, description="Brief description of the resource")
    resource_type: Optional[str] = Field(None, description="Type of resource (article, video, documentation)")


class ExplanationLevels(BaseModel):
    """Schema for different levels of explanation"""
    simple: str = Field(..., description="Simple explanation for beginners")
    detailed: str = Field(..., description="Detailed explanation with more context")
    technical: str = Field(..., description="Technical explanation with programming concepts")


class ErrorExplanationRequest(BaseModel):
    """Schema for error explanation request"""
    error_trace: str = Field(..., description="The error message or stack trace")
    code_context: str = Field(..., description="The code that generated the error")
    language: str = Field(..., description="The programming language of the code")
    user_level: str = Field("intermediate", description="User experience level (beginner, intermediate, advanced)")


class ErrorExplanationResponse(BaseModel):
    """Schema for error explanation response"""
    explanation: ExplanationLevels = Field(..., description="Explanations at different levels of detail")
    learning_resources: List[LearningResource] = Field(default_factory=list, description="Relevant learning resources")
    related_concepts: List[str] = Field(default_factory=list, description="Related programming concepts")
    
    model_config = {"from_attributes": True} 