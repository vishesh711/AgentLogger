# Getting Started with AgentLogger

This guide will help you get started with AgentLogger, an AI-powered debugging service that helps you identify and fix code issues quickly.

## Prerequisites

Before you begin, make sure you have:

- Installed AgentLogger (see the [Installation Guide](installation.md))
- Generated an API key (using `scripts/generate_api_key.py` or the API)
- Basic understanding of REST APIs

## Quick Start

### Using the API

1. **Analyze Code**

```bash
curl -X POST "http://localhost:8000/v1/analyze" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python"
  }'
```

2. **Fix Issues**

```bash
curl -X POST "http://localhost:8000/v1/fix" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "analysis-id-from-analyze-endpoint",
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python"
  }'
```

3. **Explain Errors**

```bash
curl -X POST "http://localhost:8000/v1/explain" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "error_trace": "ZeroDivisionError: division by zero",
    "code_context": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "user_level": "beginner"
  }'
```

4. **Generate Patches**

```bash
curl -X POST "http://localhost:8000/v1/patch" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "original_code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "issue_description": "Division by zero error"
  }'
```

### Using the CLI

1. **Configure the CLI**

```bash
agent-logger configure --api-key your-api-key
```

2. **Analyze Code**

```bash
agent-logger analyze path/to/file.py
```

3. **Fix Issues**

```bash
agent-logger fix path/to/file.py
```

4. **Explain Errors**

```bash
agent-logger explain "ZeroDivisionError: division by zero" --file path/to/file.py --level beginner
```

5. **Generate Patches**

```bash
agent-logger patch path/to/file.py --issue "Division by zero error"
```

## Core Concepts

### Code Analysis

The `/v1/analyze` endpoint analyzes code for issues such as:

- Syntax errors
- Logical bugs
- Security vulnerabilities
- Performance issues
- Code style issues

Example response:

```json
{
  "analysis_id": "a1b2c3d4",
  "issues": [
    {
      "id": "1",
      "type": "logical_error",
      "severity": "critical",
      "message": "Division by zero error",
      "line_start": 4,
      "line_end": 4,
      "code_snippet": "result = divide(10, 0)",
      "suggestions": [
        "Add a check to handle the case where the divisor is zero"
      ]
    }
  ],
  "language": "python",
  "summary": "The code contains a critical logical error: division by zero."
}
```

### Fix Generation

The `/v1/fix` endpoint generates fixes for identified issues. It can:

- Fix syntax errors
- Correct logical bugs
- Improve security vulnerabilities
- Optimize performance issues
- Fix code style issues

Example response:

```json
{
  "fix_id": "f1e2d3c4",
  "analysis_id": "a1b2c3d4",
  "fixed_code": "def divide(a, b):\n    if b == 0:\n        return \"Cannot divide by zero\"\n    return a / b\n\nresult = divide(10, 0)\nprint(result)",
  "changes": [
    {
      "issue_id": "1",
      "change_type": "add_condition",
      "line_start": 2,
      "line_end": 3,
      "original_code": "",
      "new_code": "    if b == 0:\n        return \"Cannot divide by zero\"",
      "explanation": "Added a check to handle division by zero"
    }
  ],
  "explanation": "The fix adds a check to handle the case where the divisor is zero, preventing the division by zero error."
}
```

### Error Explanation

The `/v1/explain` endpoint provides detailed explanations for error messages. It supports multiple explanation levels:

- **Beginner**: Simple, easy-to-understand explanations with examples
- **Intermediate**: More detailed explanations with technical context
- **Advanced**: In-depth explanations with implementation details

Example response:

```json
{
  "explanation_id": "e1f2g3h4",
  "error_trace": "ZeroDivisionError: division by zero",
  "user_level": "beginner",
  "explanation": {
    "summary": "You tried to divide a number by zero, which is not allowed in mathematics.",
    "detailed": "In your code, you're calling divide(10, 0) which tries to return 10 / 0. In mathematics, division by zero is undefined, so Python raises a ZeroDivisionError.",
    "solution": "You need to add a check to make sure the divisor is not zero before performing the division.",
    "code_example": "def divide(a, b):\n    if b == 0:\n        return \"Cannot divide by zero\"\n    return a / b"
  },
  "resources": [
    {
      "title": "Python ZeroDivisionError",
      "url": "https://docs.python.org/3/library/exceptions.html#ZeroDivisionError"
    }
  ]
}
```

### Patch Generation

The `/v1/patch` endpoint generates patches in unified diff format that can be easily applied to your code.

Example response:

```json
{
  "patch_id": "p1q2r3s4",
  "patch": "--- original.py\n+++ fixed.py\n@@ -1,4 +1,6 @@\n def divide(a, b):\n+    if b == 0:\n+        return \"Cannot divide by zero\"\n     return a / b\n \n result = divide(10, 0)",
  "explanation": "This patch adds a check to handle division by zero in the divide function.",
  "language": "python",
  "issue_description": "Division by zero error"
}
```

## Next Steps

- Explore the [API Documentation](../api/index.md) for detailed information about each endpoint
- Learn how to [Configure AgentLogger](configuration.md) for your specific needs
- Check out the [CLI Documentation](cli.md) for more details on using the command-line interface
- Learn how to [Deploy AgentLogger](deployment.md) to production

## Common Issues

- **API Key Invalid**: Make sure you're using the correct API key and including it in the `X-API-Key` header
- **Rate Limiting**: By default, the API is limited to 60 requests per minute
- **Unsupported Language**: Currently, AgentLogger supports Python and JavaScript. More languages will be added soon. 