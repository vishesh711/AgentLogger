"""
API endpoints for agent-based debugging.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid

from app.core.db import get_db
from app.agents.agent_system import AgentSystem
from app.services.ai.groq_client import GroqClient
from app.core.config import settings

router = APIRouter()

# Initialize the agent system
groq_client = GroqClient(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL)
agent_system = AgentSystem(llm_client=groq_client)
agent_system.initialize_agents()

# Store for active debugging sessions
active_sessions = {}

@router.post("/agent-debug")
async def start_agent_debug(
    background_tasks: BackgroundTasks,
    code: str,
    language: str,
    error_message: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Start an agent-based debugging session.
    """
    # Generate a user ID (in a real system, this would be authenticated)
    user_id = f"user_{uuid.uuid4()}"
    
    # Submit the request to the agent system
    session_id = await agent_system.submit_user_request(
        user_id=user_id,
        code=code,
        language=language,
        error_message=error_message
    )
    
    # Store the session
    active_sessions[session_id] = {
        "user_id": user_id,
        "status": "started",
        "updates": []
    }
    
    # Return the session ID
    return {
        "session_id": session_id,
        "status": "started",
        "message": "Debugging session started"
    }

@router.get("/agent-debug/{session_id}")
async def get_debug_status(session_id: str):
    """
    Get the status of a debugging session.
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return active_sessions[session_id]

@router.post("/agent-debug/{session_id}/start")
async def start_agent_system(background_tasks: BackgroundTasks):
    """
    Start the agent system in the background.
    """
    background_tasks.add_task(agent_system.start)
    return {"status": "started", "message": "Agent system started in the background"}

@router.post("/agent-debug/{session_id}/stop")
async def stop_agent_system():
    """
    Stop the agent system.
    """
    await agent_system.stop()
    return {"status": "stopped", "message": "Agent system stopped"} 