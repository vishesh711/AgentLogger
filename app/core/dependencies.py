"""
Core dependencies for dependency injection
"""
import asyncio
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.agents.agent_system import AgentSystem
from app.services.ai.groq_client import GroqClient
from app.core.config import settings

# Global agent system instance
_agent_system: AgentSystem = None
_agent_system_task: asyncio.Task = None


def get_db() -> AsyncGenerator[Session, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_agent_system() -> AgentSystem:
    """Get the global agent system instance"""
    global _agent_system, _agent_system_task

    if _agent_system is None:
        # Initialize the Groq client
        groq_client = GroqClient(api_key=settings.GROQ_API_KEY)

        # Create and initialize the agent system
        _agent_system = AgentSystem(llm_client=groq_client)
        _agent_system.initialize_agents()

        # Start the agent system in the background if not already running
        if _agent_system_task is None or _agent_system_task.done():
            try:
                loop = asyncio.get_event_loop()
                _agent_system_task = loop.create_task(
                    _agent_system.start()
                )
            except RuntimeError:
                # If no event loop is running, the task will be created when needed
                _agent_system_task = None

    return _agent_system


def get_agent_system_dependency() -> AgentSystem:
    """Dependency function for FastAPI"""
    return get_agent_system()


async def cleanup_agent_system():
    """Cleanup function to properly stop the agent system"""
    if _agent_system:
        await _agent_system.stop()

    if _agent_system_task and not _agent_system_task.done():
        _agent_system_task.cancel()
        try:
            await _agent_system_task
        except asyncio.CancelledError:
            pass
