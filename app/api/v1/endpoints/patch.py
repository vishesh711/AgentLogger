from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.services.ai.groq_client import GroqClient
from app.models.schemas.patch import PatchRequest, PatchResponse

router = APIRouter()


@router.post("/", response_model=PatchResponse)
async def generate_patch(
    request: Request,
    patch_data: PatchRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a patch for a code issue
    
    This endpoint takes the original code, a description of the issue,
    and returns a patch that can be applied to fix the issue.
    """
    try:
        # Get user_id from request state (set by the API key middleware)
        user_id = request.state.user_id
        
        # Initialize Groq client
        groq_client = GroqClient()
        
        # Generate the patch
        patch_result = await groq_client.generate_patch(
            original_code=patch_data.original_code,
            language=patch_data.language,
            issue_description=patch_data.issue_description,
            context=patch_data.context
        )
        
        # Return the patch response
        return PatchResponse(
            patch=patch_result["patch"],
            explanation=patch_result["explanation"],
            can_auto_apply=patch_result["can_auto_apply"]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the patch: {str(e)}"
        ) 