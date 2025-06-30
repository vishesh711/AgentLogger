# Agent Architecture

AgentLogger uses an agent-based architecture to provide intelligent debugging capabilities. This document explains the architecture and how the different agents work together.

## Overview

The agent system consists of specialized AI agents that work together to analyze code, identify issues, and generate fixes. Each agent has a specific role and expertise, allowing them to collaborate effectively.

```
┌─────────────────────┐
│                     │
│  Coordinator Agent  │
│                     │
└─────────┬───────────┘
          │
          │ coordinates
          │
┌─────────▼───────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│   Analyzer Agent    │────▶│ Fix Generator Agent │────▶│   GitHub Agent      │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Agent Types

### Coordinator Agent

The Coordinator Agent is responsible for orchestrating the debugging process. It:

- Receives the initial debugging request
- Determines which agents to invoke and in what order
- Manages the flow of information between agents
- Aggregates results and provides the final response

**Implementation**: `app/agents/coordinator_agent.py`

```python
class CoordinatorAgent(BaseAgent):
    """
    Agent responsible for coordinating the debugging process.
    """
    
    async def process(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the debugging session by coordinating other agents.
        """
        # Determine which agents to invoke based on the task
        if "code" in session_data:
            # First analyze the code
            analyzer_agent = AnalyzerAgent()
            analysis_result = await analyzer_agent.process(session_data)
            
            # If issues were found and fix is requested, generate fixes
            if analysis_result.get("issues") and session_data.get("generate_fix", True):
                fix_agent = FixGeneratorAgent()
                fix_result = await fix_agent.process({
                    **session_data,
                    "analysis_result": analysis_result
                })
                
                return {
                    "analysis": analysis_result,
                    "fixes": fix_result.get("fixes", [])
                }
            
            return {"analysis": analysis_result}
            
        elif "error_trace" in session_data:
            # Handle error explanation
            # ...
```

### Analyzer Agent

The Analyzer Agent is responsible for analyzing code and identifying issues. It:

- Parses the code to understand its structure
- Identifies syntax errors, logical bugs, and other issues
- Categorizes issues by type and severity
- Provides detailed information about each issue

**Implementation**: `app/agents/analyzer_agent.py`

```python
class AnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing code and identifying issues.
    """
    
    async def process(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code and identify issues.
        """
        code = session_data.get("code")
        language = session_data.get("language")
        
        if not code or not language:
            return {"error": "Code and language are required"}
        
        # Get the appropriate parser for the language
        parser = parser_factory.get_parser(language)
        
        # Parse the code
        parsed_code = parser.parse(code)
        
        # Use AI to analyze the code
        groq_client = GroqClient()
        issues = await groq_client.analyze_code(code, language)
        
        return {
            "issues": issues,
            "language": language,
            "parsed_structure": parsed_code
        }
```

### Fix Generator Agent

The Fix Generator Agent is responsible for generating fixes for identified issues. It:

- Takes the analysis results from the Analyzer Agent
- Generates potential fixes for each issue
- Validates the fixes to ensure they resolve the issues
- Provides explanations for the fixes

**Implementation**: `app/agents/fix_generator_agent.py`

```python
class FixGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating fixes for identified issues.
    """
    
    async def process(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fixes for identified issues.
        """
        code = session_data.get("code")
        language = session_data.get("language")
        analysis_result = session_data.get("analysis_result", {})
        issues = analysis_result.get("issues", [])
        
        if not issues:
            return {"message": "No issues to fix"}
        
        fixes = []
        groq_client = GroqClient()
        
        for issue in issues:
            # Generate a fix for the issue
            fix_result = await groq_client.fix_issue(code, language, issue)
            
            # Validate the fix
            is_valid = self._validate_fix(code, fix_result.get("fixed_code", ""), issue)
            
            fixes.append({
                "issue_id": issue.get("id"),
                "fixed_code": fix_result.get("fixed_code", ""),
                "explanation": fix_result.get("explanation", ""),
                "is_valid": is_valid
            })
        
        return {"fixes": fixes}
    
    def _validate_fix(self, original_code: str, fixed_code: str, issue: Dict[str, Any]) -> bool:
        """
        Validate that the fix resolves the issue.
        """
        # Implement validation logic
        # ...
```

## Agent Communication

Agents communicate with each other through structured data passed between their `process` methods. The Coordinator Agent manages this flow of information, ensuring that each agent receives the data it needs and that the results are properly aggregated.

## Agent System Workflow

1. **Initialization**: The Coordinator Agent is initialized with the user's request.
2. **Task Determination**: The Coordinator Agent determines the task type (code analysis, error explanation, etc.).
3. **Agent Selection**: The Coordinator Agent selects the appropriate agents to handle the task.
4. **Processing**: Each agent processes its part of the task and returns results.
5. **Aggregation**: The Coordinator Agent aggregates the results from all agents.
6. **Response**: The final response is returned to the user.

## Integration with Services

The agents use various services to perform their tasks:

- **AI Services**: For code analysis, fix generation, and error explanation
- **Parser Services**: For parsing and understanding code
- **Sandbox Services**: For safely executing code to validate fixes
- **GitHub Services**: For creating pull requests with fixes

## Error Handling

The agent system includes robust error handling to ensure that failures in one agent don't crash the entire system:

- Each agent catches and handles its own exceptions
- The Coordinator Agent monitors agent execution and handles failures
- If an agent fails, the Coordinator Agent can try alternative approaches or provide partial results

## Extending the Agent System

To add a new agent type:

1. Create a new agent class that extends `BaseAgent`
2. Implement the `process` method
3. Update the Coordinator Agent to use the new agent when appropriate

Example:

```python
class NewAgent(BaseAgent):
    """
    A new agent type.
    """
    
    async def process(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the session data.
        """
        # Implement agent logic
        # ...
        
        return {"result": "..."}
```

## Agent Configuration

Agents can be configured through the application configuration:

```python
# app/core/config.py
class Settings(BaseSettings):
    # ...
    
    # Agent settings
    AGENT_TIMEOUT: int = 30  # seconds
    AGENT_MAX_RETRIES: int = 3
    AGENT_PARALLEL_EXECUTION: bool = True
```

## Monitoring and Debugging

The agent system includes monitoring and debugging capabilities:

- Each agent logs its actions and results
- The Coordinator Agent tracks the execution time of each agent
- Detailed logs can be enabled for debugging purposes

## Conclusion

The agent-based architecture provides AgentLogger with powerful, flexible debugging capabilities. By breaking down the debugging process into specialized tasks handled by different agents, the system can provide more accurate and helpful results than a monolithic approach. 