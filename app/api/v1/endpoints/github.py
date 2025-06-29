from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.db import get_db
from app.services.github_service import get_pr_status

router = APIRouter()


@router.get("/pr/{pr_id}/status")
async def check_pr_status(
    pr_id: UUID,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """
    Check the status of a GitHub PR
    
    Returns the current status of the PR (open, closed, merged)
    and the PR URL if available.
    """
    try:
        return await get_pr_status(db, pr_id)
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Failed to get PR status: {str(e)}",
        ) 