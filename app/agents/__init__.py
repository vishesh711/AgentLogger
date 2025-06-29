"""
Agent-based architecture for AgentLogger.

This package contains the implementation of the agent-based architecture
for autonomous code debugging and fixing.
"""

from app.agents.base_agent import BaseAgent, Message
from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.analyzer_agent import AnalyzerAgent
from app.agents.fix_generator_agent import FixGeneratorAgent
from app.agents.agent_system import AgentSystem

__all__ = [
    'BaseAgent',
    'Message',
    'CoordinatorAgent',
    'AnalyzerAgent',
    'FixGeneratorAgent',
    'AgentSystem',
] 