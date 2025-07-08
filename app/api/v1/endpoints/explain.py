from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.services.ai.groq_client import GroqClient
from app.models.schemas.explain import ErrorExplanationRequest, ErrorExplanationResponse, ExplanationLevels, LearningResource

router = APIRouter()


@router.post("/", response_model=ErrorExplanationResponse)
async def explain_error(
    request: Request,
    explanation_data: ErrorExplanationRequest,
    db: Session = Depends(get_db),
):
    """
    Get a detailed explanation of an error message with different levels of detail
    based on the user's experience level.
    
    This endpoint takes an error message, code context, and user experience level,
    and returns explanations tailored to that level along with relevant resources.
    """
    try:
        # Get user_id from request state (set by the API key middleware)
        user_id = request.state.user_id
        
        # Initialize Groq client
        groq_client = GroqClient()
        
        # Generate the explanation
        explanation = await groq_client.explain_error(
            error_message=explanation_data.error_trace,
            code=explanation_data.code_context,
            language=explanation_data.language,
            user_level=explanation_data.user_level
        )
        
        # Return the explanation response
        return ErrorExplanationResponse(
            explanation=ExplanationLevels(
                simple=explanation.get("simple", ""),
                detailed=explanation.get("detailed", ""),
                technical=explanation.get("technical", "")
            ),
            learning_resources=[
                LearningResource(**resource) if isinstance(resource, dict) else resource
                for resource in explanation.get("learning_resources", [])
            ],
            related_concepts=explanation.get("related_concepts", [])
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the explanation: {str(e)}"
        ) 