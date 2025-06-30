# Agent Architecture Implementation

This document provides implementation details for the agent architecture described in [Agent Architecture](agent-architecture.md).

## Base Agent

The `BaseAgent` class defines the interface for all agents in the system. It provides common functionality and ensures that all agents follow the same pattern.

```python
# app/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    """
    
    @abstractmethod
    async def process(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the session data and return the result.
        
        Args:
            session_data: Dictionary containing session data
            
        Returns:
            Dictionary containing the result
        """
        pass
    
    async def handle_error(self, error: Exception, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an error that occurred during processing.
        
        Args:
            error: The exception that occurred
            session_data: Dictionary containing session data
            
        Returns:
            Dictionary containing error information
        """
        return {
            "error": str(error),
            "error_type": error.__class__.__name__
        }
```

## Agent System

The `AgentSystem` class is responsible for initializing and managing agents. It provides a high-level interface for the API endpoints to interact with the agent system.

```python
# app/agents/agent_system.py
from typing import Dict, Any, Type
from .base_agent import BaseAgent
from .coordinator_agent import CoordinatorAgent

class AgentSystem:
    """
    System for managing and interacting with agents.
    """
    
    def __init__(self):
        """
        Initialize the agent system.
        """
        self.coordinator = CoordinatorAgent()
    
    async def process_debugging_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a debugging request using the agent system.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            Dictionary containing the result
        """
        try:
            return await self.coordinator.process(request_data)
        except Exception as e:
            return await self.coordinator.handle_error(e, request_data)
    
    async def process_analysis_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a code analysis request.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            Dictionary containing the analysis result
        """
        return await self.process_debugging_request({
            **request_data,
            "task": "analyze"
        })
    
    async def process_fix_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a fix generation request.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            Dictionary containing the fix result
        """
        return await self.process_debugging_request({
            **request_data,
            "task": "fix"
        })
    
    async def process_explain_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an error explanation request.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            Dictionary containing the explanation result
        """
        return await self.process_debugging_request({
            **request_data,
            "task": "explain"
        })
    
    async def process_patch_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a patch generation request.
        
        Args:
            request_data: Dictionary containing request data
            
        Returns:
            Dictionary containing the patch result
        """
        return await self.process_debugging_request({
            **request_data,
            "task": "patch"
        })
```

## Integration with API Endpoints

The agent system is integrated with the API endpoints to handle user requests. Each endpoint creates an instance of the `AgentSystem` and calls the appropriate method.

```python
# app/api/v1/endpoints/analyze.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.agents.agent_system import AgentSystem
from app.services.api_key_service import validate_api_key

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def analyze_code(
    request: AnalysisRequest,
    api_key: str = Depends(validate_api_key)
):
    """
    Analyze code for issues.
    """
    agent_system = AgentSystem()
    result = await agent_system.process_analysis_request(request.dict())
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result
```

## Agent Implementation Details

### Coordinator Agent

The Coordinator Agent is implemented in `app/agents/coordinator_agent.py`. It:

1. Receives requests from the API endpoints via the `AgentSystem`
2. Determines which agents to invoke based on the task
3. Manages the flow of information between agents
4. Handles errors and retries
5. Returns the final result to the API endpoint

### Analyzer Agent

The Analyzer Agent is implemented in `app/agents/analyzer_agent.py`. It:

1. Receives code and language from the Coordinator Agent
2. Uses the appropriate parser to parse the code
3. Uses the `GroqClient` to analyze the code
4. Returns the analysis results to the Coordinator Agent

### Fix Generator Agent

The Fix Generator Agent is implemented in `app/agents/fix_generator_agent.py`. It:

1. Receives code, language, and analysis results from the Coordinator Agent
2. Uses the `GroqClient` to generate fixes for each issue
3. Validates the fixes
4. Returns the fix results to the Coordinator Agent

## Testing Agents

The agent system includes comprehensive tests to ensure that each agent works correctly and that they work together as expected.

```python
# tests/test_agents.py
import pytest
from app.agents.agent_system import AgentSystem

@pytest.mark.asyncio
async def test_analysis_request():
    """
    Test that the agent system can process an analysis request.
    """
    agent_system = AgentSystem()
    result = await agent_system.process_analysis_request({
        "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
        "language": "python"
    })
    
    assert "issues" in result
    assert len(result["issues"]) > 0
    assert "division by zero" in str(result["issues"])
```

## Conclusion

The agent architecture provides a flexible, extensible framework for implementing debugging capabilities. By breaking down the debugging process into specialized tasks handled by different agents, the system can provide more accurate and helpful results than a monolithic approach.