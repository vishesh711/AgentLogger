from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.services.ai.groq_client import GroqClient

router = APIRouter()


class ErrorExplanationRequest(BaseModel):
    error_message: str = Field(..., description="The error message to explain")
    code: str = Field(..., description="The code that generated the error")
    language: str = Field(..., description="The programming language of the code")


class ErrorExplanationResponse(BaseModel):
    explanation: str = Field(..., description="Simple explanation of the error")


@router.post("/", response_model=ErrorExplanationResponse)
async def explain_error(
    request: ErrorExplanationRequest,
    db: Session = Depends(get_db),
):
    """
    Explain an error message in simple terms
    
    This endpoint takes an error message, the code that generated it,
    and the programming language, and returns a simple explanation
    of what the error means and how to fix it.
    """
    try:
        # Initialize the Groq client
        groq_client = GroqClient()
        
        # Get the explanation
        explanation = await groq_client.explain_error(
            request.error_message,
            request.code,
            request.language,
        )
        
        return ErrorExplanationResponse(explanation=explanation)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Failed to explain error: {str(e)}",
        ) 