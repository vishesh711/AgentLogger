from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.db import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    } 