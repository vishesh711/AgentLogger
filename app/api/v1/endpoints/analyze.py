from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.models.schemas.analysis import (
    AnalysisRequestCreate, AnalysisRequestResponse, AnalysisResult, CodeIssue
)
from app.services.analysis_service import (
    create_analysis_request, get_analysis_request, 
    get_analysis_requests_by_user, analyze_code_with_agents, analyze_code_direct
)
from app.agents.agent_system import AgentSystem

router = APIRouter()

# Import the dependency function
from app.core.dependencies import get_agent_system_dependency


async def analyze_code_background(db: Session, analysis_id: UUID, agent_system: AgentSystem = None):
    """Background task to analyze code"""
    try:
        if agent_system:
            await analyze_code_with_agents(db, analysis_id, agent_system)
        else:
            await analyze_code_direct(db, analysis_id)
    except Exception as e:
        print(f"Background analysis failed: {e}")


@router.post("/", response_model=AnalysisRequestResponse)
async def create_analysis(
    analysis_data: AnalysisRequestCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    """
    Create a new code analysis request
    
    The analysis will run asynchronously in the background.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # Create the analysis request
    analysis = await create_analysis_request(db, analysis_data, UUID(user_id))
    
    # Run the analysis in the background
    background_tasks.add_task(analyze_code_background, db, analysis.id, agent_system)
    
    return analysis


@router.get("/{analysis_id}", response_model=AnalysisRequestResponse)
async def get_analysis(
    analysis_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get a specific analysis request by ID
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Analysis request with ID {analysis_id} not found",
        )
    
    # Verify that the analysis belongs to the current user
    if str(analysis.user_id) != user_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Analysis request with ID {analysis_id} not found",
        )
    
    return analysis


@router.get("/", response_model=List[AnalysisRequestResponse])
async def get_user_analyses(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all analysis requests for the current user
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    return await get_analysis_requests_by_user(db, UUID(user_id), skip, limit)


@router.post("/{analysis_id}/run", response_model=AnalysisResult)
async def run_analysis(
    analysis_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Run or re-run analysis on an existing request
    
    This is a synchronous endpoint that will wait for the analysis to complete.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # Get the analysis request
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Analysis request with ID {analysis_id} not found",
        )
    
    # Verify that the analysis belongs to the current user
    if str(analysis.user_id) != user_id:
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