from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.models.schemas.analysis import (
    AnalysisRequestCreate, AnalysisRequestResponse, AnalysisResult, CodeIssue
)
from app.services.analysis_service import (
    create_analysis_request, get_analysis_request, 
    get_analysis_requests_by_user, analyze_code
)

router = APIRouter()


@router.post("/", response_model=AnalysisRequestResponse)
async def create_analysis(
    analysis_data: AnalysisRequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new code analysis request
    
    The analysis will run asynchronously in the background.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = UUID("00000000-0000-0000-0000-000000000000")  # Placeholder
    
    # Create the analysis request
    analysis = await create_analysis_request(db, analysis_data, user_id)
    
    # Run the analysis in the background
    background_tasks.add_task(analyze_code, db, analysis.id)
    
    return analysis


@router.get("/{analysis_id}", response_model=AnalysisRequestResponse)
async def get_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific analysis request by ID
    """
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Analysis request with ID {analysis_id} not found",
        )
    
    return analysis


@router.get("/", response_model=List[AnalysisRequestResponse])
async def get_user_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all analysis requests for the current user
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = UUID("00000000-0000-0000-0000-000000000000")  # Placeholder
    
    return await get_analysis_requests_by_user(db, user_id, skip, limit)


@router.post("/{analysis_id}/run", response_model=AnalysisResult)
async def run_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Run or re-run analysis on an existing request
    
    This is a synchronous endpoint that will wait for the analysis to complete.
    """
    # Get the analysis request
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Analysis request with ID {analysis_id} not found",
        )
    
    try:
        # Run the analysis
        issues = await analyze_code(db, analysis_id)
        
        # Get the updated analysis request
        updated_analysis = await get_analysis_request(db, analysis_id)
        
        return AnalysisResult(
            request_id=analysis_id,
            status=updated_analysis.status,
            issues=issues,
            error=updated_analysis.error,
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) 