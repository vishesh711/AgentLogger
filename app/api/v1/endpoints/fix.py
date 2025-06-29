from typing import List, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.models.schemas.fix import FixRequestCreate, FixRequestResponse, FixResult
from app.services.fix_service import (
    create_fix_request, get_fix_request, 
    get_fix_requests_by_user, get_fix_requests_by_analysis,
    generate_fix
)

router = APIRouter()


@router.post("/", response_model=FixRequestResponse)
async def create_fix(
    request: Request,
    fix_data: FixRequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new fix request for an issue
    
    The fix will be generated asynchronously in the background.
    """
    # Get user_id from request state (set by the API key middleware)
    user_id = request.state.user_id
    
    try:
        # Create the fix request
        fix = await create_fix_request(db, fix_data, user_id)
        
        # Generate the fix in the background
        background_tasks.add_task(generate_fix, db, fix.id)
        
        return fix
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


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
    user_id = request.state.user_id
    
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