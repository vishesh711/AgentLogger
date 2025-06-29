# Agent-Based Architecture Implementation

This document provides an overview of the implementation of the agent-based architecture for AgentLogger.

## Current Implementation

The current implementation includes:

1. **Base Agent Framework**
   - `BaseAgent`: Abstract base class for all agents
   - `Message`: Class for agent communication
   - `AgentSystem`: System for managing agents and their communication

2. **Specialized Agents**
   - `CoordinatorAgent`: Orchestrates the debugging workflow
   - `AnalyzerAgent`: Analyzes code and identifies issues
   - `FixGeneratorAgent`: Generates fixes for identified issues

3. **API Integration**
   - `/api/v1/agent/agent-debug`: Endpoint for starting a debugging session
   - `/api/v1/agent/agent-debug/{session_id}`: Endpoint for checking session status

## How It Works

1. **Message-Based Communication**
   - Agents communicate by sending and receiving messages
   - Each message has a type, sender, recipient, and content
   - The `AgentSystem` dispatches messages to the appropriate agents

2. **Workflow**
   - User submits code for debugging
   - CoordinatorAgent creates a debugging plan
   - AnalyzerAgent identifies issues in the code
   - FixGeneratorAgent generates fixes for the issues
   - CoordinatorAgent sends the final report to the user

3. **State Management**
   - Each debugging session has its own state
   - State includes code, issues, fixes, and status
   - Coordinator manages the overall state of the session

## Using the Agent System

### Starting a Debugging Session

```python
from app.agents.agent_system import AgentSystem
from app.services.ai.groq_client import GroqClient

# Initialize the agent system
groq_client = GroqClient(api_key="your_api_key", model="your_model")
agent_system = AgentSystem(llm_client=groq_client)
agent_system.initialize_agents()

# Start the agent system
await agent_system.start()

# Submit a debugging request
session_id = await agent_system.submit_user_request(
    user_id="user_123",
    code="your_code_here",
    language="python",
    error_message="optional_error_message"
)
```

### API Usage

```bash
# Start a debugging session
curl -X POST "http://localhost:8000/api/v1/agent/agent-debug" \
  -H "Content-Type: application/json" \
  -d '{"code": "your_code_here", "language": "python", "error_message": "optional_error_message"}'

# Check session status
curl -X GET "http://localhost:8000/api/v1/agent/agent-debug/{session_id}"
```

## Future Enhancements

1. **Additional Agents**
   - `ExplainerAgent`: Explains issues in human terms
   - `TestAgent`: Validates proposed fixes
   - `PRAgent`: Creates pull requests with fixes

2. **Advanced Capabilities**
   - Learning from past debugging sessions
   - Collaborative debugging with multiple agents
   - Support for more languages and frameworks

3. **System Improvements**
   - Persistent storage for debugging sessions
   - Real-time updates via WebSockets
   - User authentication and authorization

## Implementation Roadmap

1. **Phase 1: Core Framework (Current)**
   - Base agent framework
   - Basic coordinator, analyzer, and fix generator agents
   - API integration

2. **Phase 2: Enhanced Agents**
   - Implement explainer agent
   - Implement test agent
   - Improve agent communication

3. **Phase 3: Advanced Features**
   - Implement PR agent
   - Add learning capabilities
   - Support for more languages

## Contributing

To contribute to the agent-based architecture:

1. Understand the existing agent framework in `app/agents/`
2. Follow the design principles in `docs/development/agent-architecture.md`
3. Create new agents by extending `BaseAgent`
4. Update the `AgentSystem` to include your new agents
5. Add tests for your agents in `tests/agents/`