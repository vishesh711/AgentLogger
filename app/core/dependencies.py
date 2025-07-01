"""
Dependencies for FastAPI endpoints
"""

from app.services.ai.groq_client import GroqClient
from app.agents.agent_system import AgentSystem

# Global agent system instance
_agent_system = None

def get_agent_system() -> AgentSystem:
    """Get the global agent system instance"""
    global _agent_system
    if _agent_system is None:
        # Initialize the agent system
        groq_client = GroqClient()
        _agent_system = AgentSystem(llm_client=groq_client)
        _agent_system.initialize_agents()
    return _agent_system

def get_agent_system_dependency() -> AgentSystem:
    """FastAPI dependency to get the agent system"""
    return get_agent_system() 