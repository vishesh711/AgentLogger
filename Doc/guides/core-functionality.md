# Using AgentLogger's Core Functionality

This guide explains how to use the core functionality of AgentLogger - an AI-powered debugging tool that uses a multi-agent system to analyze, explain, and fix code issues.

## Understanding the Agent System

AgentLogger's core functionality is built around a multi-agent system:

1. **Analyzer Agent**: Examines code to identify bugs, issues, and potential improvements
2. **Fix Generator Agent**: Creates fixes for the identified issues
3. **Coordinator Agent**: Orchestrates the workflow between agents and manages the debugging process

These agents communicate through a message-passing system, working together to provide a comprehensive debugging experience.

## Using the Code Analysis Feature

The code analysis feature examines your code for bugs, issues, and potential improvements.

### Via the Web Interface

1. Navigate to the Playground page at `http://localhost`
2. Enter your code in the editor
3. Select the language from the dropdown
4. Click "Analyze Code"
5. View the analysis results showing identified issues

### Via the API

```bash
curl -X POST "http://localhost/api/v1/analyze" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python"
  }'
```

## Getting Error Explanations

When you encounter an error message, AgentLogger can provide multi-level explanations.

### Via the Web Interface

1. Navigate to the Playground page
2. Enter your code and the error message
3. Select your experience level (beginner, intermediate, advanced)
4. Click "Explain Error"
5. View the explanations at different detail levels

### Via the API

```bash
curl -X POST "http://localhost/api/v1/explain" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "error_trace": "ZeroDivisionError: division by zero",
    "code_context": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "user_level": "beginner"
  }'
```

## Generating Fixes

After analyzing code, AgentLogger can generate fixes for the identified issues.

### Via the Web Interface

1. After analyzing code in the Playground, view the identified issues
2. Click "Generate Fix" next to an issue
3. Review the proposed fix and explanation
4. Apply the fix if desired

### Via the API

```bash
curl -X POST "http://localhost/api/v1/fix" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "analysis-id-from-analyze-endpoint",
    "issue_index": 0
  }'
```

## Creating Patches

For more complex fixes, AgentLogger can generate patches in a standard format.

### Via the Web Interface

1. After generating a fix in the Playground
2. Click "Create Patch"
3. Download the patch file or copy the patch content

### Via the API

```bash
curl -X POST "http://localhost/api/v1/patch" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "original_code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "issue_description": "Division by zero error"
  }'
```

## GitHub Integration

AgentLogger can analyze and fix issues directly from GitHub repositories.

### Via the Web Interface

1. Navigate to the GitHub Integration page
2. Connect your GitHub account
3. Select a repository and PR/issue to analyze
4. View analysis results and proposed fixes
5. Create a PR with the fixes if desired

### Via the API

```bash
curl -X POST "http://localhost/api/v1/github/analyze" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "username/repository",
    "pr_number": 123
  }'
```

## Sandbox Execution

AgentLogger can execute code in a secure sandbox to verify issues and fixes.

### Via the Web Interface

1. In the Playground, enter your code
2. Click "Execute in Sandbox"
3. View the execution results and any errors

## Advanced Features

### Agent Debugging

For advanced users, AgentLogger provides insights into the agent system:

```bash
curl -X GET "http://localhost/api/v1/agent-debug/status" \
  -H "X-API-Key: your-api-key"
```

This returns information about the current state of the agent system, including active agents and pending messages.

## Next Steps

- Learn about [API Key Management](api-keys.md)
- Explore [GitHub Integration](github-integration.md)
- Set up [Custom Configurations](configuration.md) 