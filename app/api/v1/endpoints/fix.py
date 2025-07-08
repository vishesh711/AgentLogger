from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.models.schemas.fix import FixRequestCreate, FixRequestResponse, FixResult
from app.services.fix_service import (
    get_fix_request, 
    get_fix_requests_by_user, get_fix_requests_by_analysis,
    generate_fix, process_fix_with_agents, process_fix_direct
)
from app.agents.agent_system import AgentSystem
from app.core.dependencies import get_agent_system_dependency

router = APIRouter()


async def process_fix_background(db: Session, fix_id: str, agent_system: AgentSystem = None):
    """Background task to process fix request"""
    try:
        from app.models.db.fix import FixRequest, FixStatus
        from datetime import datetime
        
        # Get the fix request
        db_fix_request = db.query(FixRequest).filter(FixRequest.id == fix_id).first()
        if not db_fix_request:
            return
        
        # Update status
        db_fix_request.status = FixStatus.PROCESSING
        db.commit()
        
        try:
            # Try to use the agent system for comprehensive fix generation
            if agent_system:
                fix_result = await process_fix_with_agents(db, db_fix_request, agent_system)
            else:
                # Fallback to direct Groq if agent system is not available
                print("Agent system not provided for fix generation, falling back to direct fix")
                fix_result = await process_fix_direct(db_fix_request)
            
            # Simple validation (just check if we got a fix)
            is_valid = bool(fix_result.get("fixed_code"))
            validation_message = "Fix generated successfully" if is_valid else "No fix generated"
            
            # Update the fix request
            db_fix_request.fixed_code = fix_result["fixed_code"]
            db_fix_request.explanation = fix_result["explanation"]
            db_fix_request.status = FixStatus.COMPLETED if is_valid else FixStatus.FAILED
            db_fix_request.validation_message = validation_message
            db_fix_request.completed_at = datetime.utcnow()
            
            db.commit()
            
        except Exception as e:
            # Handle errors
            db_fix_request.status = FixStatus.FAILED
            db_fix_request.validation_message = f"Error processing fix: {str(e)}"
            db.commit()
            
    except Exception as e:
        print(f"Background fix processing failed: {e}")


@router.post("/", response_model=FixRequestResponse)
async def create_fix(
    fix_request: FixRequestCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    """
    Create a new fix request
    
    The fix generation will run asynchronously in the background.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    # Create the fix request directly in the database
    from app.models.db.fix import FixRequest, FixStatus
    
    db_fix_request = FixRequest(
        user_id=user_id,
        code=fix_request.code,
        language=fix_request.language,
        error_message=fix_request.error_message,
        context=fix_request.context,
        analysis_id=fix_request.analysis_id,
        status=FixStatus.PENDING
    )
    
    db.add(db_fix_request)
    db.commit()
    db.refresh(db_fix_request)
    
    # Start the fix process in the background
    background_tasks.add_task(process_fix_background, db, str(db_fix_request.id), agent_system)
    
    return FixRequestResponse.model_validate(db_fix_request)


@router.get("/{fix_id}", response_model=FixRequestResponse)
async def get_fix(
    fix_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific fix request by ID
    """
    fix = await get_fix_request(db, fix_id)
    if not fix:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Fix request with ID {fix_id} not found",
        )
    
    return fix


@router.get("/", response_model=List[FixRequestResponse])
async def get_user_fixes(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all fix requests for the current user
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User ID not found in request. API key authentication failed."
        )
    
    return await get_fix_requests_by_user(db, user_id, skip, limit)


@router.get("/analysis/{analysis_id}", response_model=List[FixRequestResponse])
async def get_fixes_by_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get all fix requests for a specific analysis
    """
    return await get_fix_requests_by_analysis(db, analysis_id)


@router.post("/{fix_id}/run", response_model=FixResult)
async def run_fix_generation(
    fix_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Run or re-run fix generation on an existing request
    
    This is a synchronous endpoint that will wait for the fix to be generated.
    """
    # Get the fix request
    fix = await get_fix_request(db, fix_id)
    if not fix:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Fix request with ID {fix_id} not found",
        )
    
    try:
        # Generate the fix
        fix_result = await generate_fix(db, fix_id)
        
        # Get the updated fix request
        updated_fix = await get_fix_request(db, fix_id)
        
        return FixResult(
            request_id=fix_id,
            status=updated_fix.status,
            fixed_code=fix_result.get("fixed_code"),
            explanation=fix_result.get("explanation"),
            error=updated_fix.error,
            pr_url=fix_result.get("pr_url"),
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) 