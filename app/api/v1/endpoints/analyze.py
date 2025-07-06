from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from app.core.db import get_db
from app.models.schemas.analysis import (
    AnalysisRequestCreate, AnalysisRequestResponse, AnalysisResult, CodeIssue
)
from app.services.analysis_service import (
    create_analysis_request, get_analysis_request, 
    get_analysis_requests_by_user, analyze_code_with_agents, analyze_code_direct, analyze_code
)
from app.agents.agent_system import AgentSystem

router = APIRouter()

# Import the dependency function
from app.core.dependencies import get_agent_system_dependency


async def analyze_code_background(db: Session, analysis_id: str, agent_system: AgentSystem = None):
    """Background task to analyze code"""
    try:
        if agent_system and agent_system.running:
            await analyze_code_with_agents(db, analysis_id, agent_system)
        else:
            await analyze_code_direct(db, analysis_id)
    except Exception as e:
        print(f"Background analysis failed: {e}")


@router.post("", response_model=AnalysisRequestResponse)
async def create_analysis(
    analysis_data: AnalysisRequestCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    """
    Create a new code analysis request
    
    The analysis will run asynchronously in the background using the agent system.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid API key."
        )
    
    # Create the analysis request
    analysis = await create_analysis_request(db, analysis_data, user_id)
    
    # Run the analysis in the background with agent system
    background_tasks.add_task(analyze_code_background, db, analysis.id, agent_system)
    
    return analysis


@router.get("/{analysis_id}", response_model=AnalysisRequestResponse)
async def get_analysis(
    analysis_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get an analysis request by ID
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid API key."
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


@router.get("", response_model=List[AnalysisRequestResponse])
async def get_user_analyses(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get all analysis requests for the current user
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid API key."
        )
    
    analyses = await get_analysis_requests_by_user(db, user_id)
    return analyses


@router.post("/{analysis_id}/run", response_model=AnalysisResult)
async def run_analysis(
    analysis_id: str,
    request: Request,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    """
    Run or re-run analysis on an existing request
    
    This is a synchronous endpoint that will wait for the analysis to complete.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid API key."
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
        # Run the analysis using agent system if available
        if agent_system and agent_system.running:
            await analyze_code_with_agents(db, analysis_id, agent_system)
        else:
            # Fallback to direct analysis
            await analyze_code_direct(db, analysis_id)
        
        # Get the updated analysis request
        updated_analysis = await get_analysis_request(db, analysis_id)
        
        # Get the issues
        issues = []
        if updated_analysis.status == "completed" and updated_analysis.issues:
            for issue_data in updated_analysis.issues:
                if isinstance(issue_data, dict):
                    issues.append(CodeIssue(
                        id=issue_data.get("id", "unknown"),
                        type=issue_data.get("type", "unknown"),
                        message=issue_data.get("message", ""),
                        line_start=issue_data.get("line_start", 1),
                        line_end=issue_data.get("line_end"),
                        column_start=issue_data.get("column_start"),
                        column_end=issue_data.get("column_end"),
                        code_snippet=issue_data.get("code_snippet", ""),
                        severity=issue_data.get("severity", "medium")
                    ))
        
        from app.models.db.analysis import AnalysisStatus
        status_enum = AnalysisStatus.COMPLETED if updated_analysis.status == "completed" else AnalysisStatus.FAILED
        
        return AnalysisResult(
            request_id=analysis_id,
            status=status_enum,
            issues=issues,
            error=updated_analysis.error,
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/quick", response_model=AnalysisResult)
async def quick_analysis(
    analysis_data: AnalysisRequestCreate,
    request: Request,
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    """
    Perform a quick analysis without storing in database
    
    This endpoint uses the agent system for immediate analysis.
    """
    # Get user_id from request state
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid API key."
        )
    
    try:
        # Use agent system directly for quick analysis
        if agent_system and agent_system.running:
            session_id = await agent_system.submit_user_request(
                user_id=user_id,
                code=analysis_data.code,
                language=analysis_data.language,
                error_message=getattr(analysis_data, 'traceback', None)
            )
            
            # Wait for analysis to complete (with timeout)
            import asyncio
            import uuid
            
            coordinator = agent_system.agents.get("coordinator_1")
            if coordinator:
                max_wait = 30  # 30 seconds timeout
                waited = 0
                while waited < max_wait:
                    session_data = coordinator.get_session_status(session_id)
                    if session_data and session_data.get("state") in ["completed", "error"]:
                        issues = []
                        for issue_data in session_data.get("issues", []):
                            issues.append(CodeIssue(
                                id=issue_data.get("id", "unknown"),
                                type=issue_data.get("type", "unknown"),
                                message=issue_data.get("message", ""),
                                line_start=issue_data.get("line_start", 1),
                                line_end=issue_data.get("line_end"),
                                column_start=issue_data.get("column_start"),
                                column_end=issue_data.get("column_end"),
                                code_snippet=issue_data.get("code_snippet", ""),
                                severity=issue_data.get("severity", "medium")
                            ))
                        
                        from app.models.db.analysis import AnalysisStatus
                        status_enum = AnalysisStatus.COMPLETED if session_data.get("state") == "completed" else AnalysisStatus.FAILED
                        
                        return AnalysisResult(
                            request_id=session_id,
                            status=status_enum,
                            issues=issues,
                            error=session_data.get("error"),
                        )
                    
                    await asyncio.sleep(1)
                    waited += 1
                
                # Timeout occurred
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Analysis timed out"
                )
            else:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Agent system coordinator not available"
                )
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Agent system not available"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Analysis failed: {str(e)}"
        ) 