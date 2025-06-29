from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    database_connected: bool


@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Check the health of the API service
    
    Returns the status, version, and database connection status.
    This endpoint does not require authentication.
    """
    # Check database connection
    try:
        # Try a simple query
        db.execute("SELECT 1")
        database_connected = True
    except Exception:
        database_connected = False
    
    return HealthResponse(
        status="ok",
        version="0.1.0",
        database_connected=database_connected,
    ) 