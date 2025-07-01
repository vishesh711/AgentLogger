# AgentLogger API Documentation

AgentLogger provides a comprehensive REST API for AI-powered code analysis, debugging, and fix generation. This documentation covers all available endpoints, authentication, and usage examples.

## 🚀 Quick Start

### Base URL
```
# Production/Docker
http://localhost/api/v1

# Development
http://localhost:8000/api/v1
```

### Authentication
All API endpoints require an API key in the `X-API-Key` header:

```bash
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

### Default API Key (Testing)
For immediate testing, use this pre-configured key:
```
QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU
```

## 📊 Interactive Documentation

AgentLogger provides interactive API documentation:

- **Swagger UI**: http://localhost/docs
- **ReDoc**: http://localhost/redoc
- **OpenAPI Schema**: http://localhost/api/v1/openapi.json

## 🔑 API Endpoints Overview

### Core Analysis Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Analyze code for issues and bugs |
| `/explain` | POST | Get detailed explanations of errors |
| `/fix` | POST | Generate fixes for code issues |
| `/patch` | POST | Create unified diff patches |

### API Key Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-keys` | GET | List user's API keys |
| `/api-keys` | POST | Create new API key |
| `/api-keys/{id}` | GET | Get specific API key |
| `/api-keys/{id}` | PUT | Update API key |
| `/api-keys/{id}` | DELETE | Delete API key |

### System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health/health` | GET | Health check endpoint |
| `/agent-debug/test-full-workflow` | POST | Test agent workflow |

## 🔧 Core Analysis API

### 1. Code Analysis

**POST** `/api/v1/analyze`

Analyze code for syntax errors, logical bugs, and potential improvements.

```bash
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2",
    "language": "python"
  }'
```

**Response:**
```json
{
  "id": "analysis-uuid",
  "status": "completed",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:05Z",
  "issues": [
    {
      "type": "syntax",
      "message": "unmatched '(' (line 4)",
      "line_number": 4,
      "code_snippet": "return fibonacci(n-1) + fibonacci(n-2",
      "severity": "high"
    }
  ]
}
```

### 2. Error Explanation

**POST** `/api/v1/explain`

Get detailed, multi-level explanations of error messages.

```bash
curl -X POST http://localhost/api/v1/explain \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python"
  }'
```

**Response:**
```json
{
  "id": "explanation-uuid",
  "explanation": "The syntax error occurs because 'hello world' is not enclosed in quotes. In Python, strings must be surrounded by quotes to be recognized as text.",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### 3. Code Fixing

**POST** `/api/v1/fix`

Generate fixes for identified code issues.

```bash
curl -X POST http://localhost/api/v1/fix \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python",
    "analysis_id": "optional-analysis-id"
  }'
```

**Response:**
```json
{
  "id": "fix-uuid",
  "status": "completed",
  "fixed_code": "print(\"hello world\")",
  "explanation": "Added quotes around the string to fix the syntax error.",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:03Z"
}
```

### 4. Patch Generation

**POST** `/api/v1/patch`

Generate unified diff patches for code fixes.

```bash
curl -X POST http://localhost/api/v1/patch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python"
  }'
```

## 🔑 API Key Management

### 1. List API Keys

**GET** `/api/v1/api-keys`

Get all API keys for the current user.

```bash
curl -X GET http://localhost/api/v1/api-keys \
  -H "X-API-Key: YOUR_API_KEY"
```

**Response:**
```json
[
  {
    "id": "key-uuid",
    "name": "My Development Key",
    "description": "Key for local development",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "expires_at": null,
    "user_id": "user-uuid"
  }
]
```

### 2. Create API Key

**POST** `/api/v1/api-keys`

Create a new API key.

```bash
curl -X POST http://localhost/api/v1/api-keys \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "name": "Production Key",
    "description": "Key for production deployment",
    "expires_in_days": 365
  }'
```

**Response:**
```json
{
  "key": "newly-generated-api-key",
  "id": "key-uuid",
  "name": "Production Key",
  "expires_at": "2026-01-01T00:00:00Z",
  "created_at": "2025-01-01T00:00:00Z"
}
```

⚠️ **Important**: The `key` field is only returned once during creation.

### 3. Delete API Key

**DELETE** `/api/v1/api-keys/{id}`

Delete an API key.

```bash
curl -X DELETE http://localhost/api/v1/api-keys/key-uuid \
  -H "X-API-Key: YOUR_API_KEY"
```

## 🏥 System Endpoints

### Health Check

**GET** `/api/v1/health/health`

Check system health and status.

```bash
curl -X GET http://localhost/api/v1/health/health \
  -H "X-API-Key: YOUR_API_KEY"
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-01-01T00:00:00Z",
  "version": "0.1.0",
  "environment": "development"
}
```

### Agent Debug

**POST** `/api/v1/agent-debug/test-full-workflow`

Test the complete agent workflow system.

```bash
curl -X POST http://localhost/api/v1/agent-debug/test-full-workflow \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "language": "python"
  }'
```

## 📝 Request/Response Schemas

### Common Request Fields

```json
{
  "code": "string",           // Required: Code to analyze
  "language": "string",       // Required: python, javascript
  "traceback": "string",      // Optional: Error traceback
  "analysis_id": "string"     // Optional: Reference to analysis
}
```

### Common Response Fields

```json
{
  "id": "string",             // Unique identifier
  "status": "string",         // completed, failed, processing
  "created_at": "datetime",   // ISO 8601 timestamp
  "updated_at": "datetime"    // ISO 8601 timestamp
}
```

### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

## 🔒 Authentication & Security

### API Key Requirements
- All endpoints require `X-API-Key` header
- API keys are user-specific and can be managed via the web interface
- Default testing key: `QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU`

### Rate Limiting
- Default: 60 requests per minute per API key
- Rate limit headers included in responses:
  ```
  X-RateLimit-Limit: 60
  X-RateLimit-Remaining: 59
  X-RateLimit-Reset: 1609459200
  ```

### CORS Support
- Configured for common development ports
- Production deployments should update CORS origins

## 🚦 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid API key |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |

## 💡 Usage Examples

### Complete Workflow Example

```python
import requests

# Configuration
API_BASE = "http://localhost/api/v1"
API_KEY = "your-api-key"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# 1. Analyze code
code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
print(result)
"""

response = requests.post(
    f"{API_BASE}/analyze",
    headers=headers,
    json={"code": code, "language": "python"}
)
analysis = response.json()
print("Analysis:", analysis)

# 2. Get explanation for error
response = requests.post(
    f"{API_BASE}/explain",
    headers=headers,
    json={
        "code": code,
        "traceback": "ZeroDivisionError: division by zero",
        "language": "python"
    }
)
explanation = response.json()
print("Explanation:", explanation)

# 3. Generate fix
response = requests.post(
    f"{API_BASE}/fix",
    headers=headers,
    json={
        "code": code,
        "traceback": "ZeroDivisionError: division by zero",
        "language": "python"
    }
)
fix = response.json()
print("Fixed code:", fix["fixed_code"])
```

### JavaScript/Frontend Example

```javascript
const API_BASE = 'http://localhost/api/v1';
const API_KEY = 'your-api-key';

async function analyzeCode(code, language) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify({ code, language })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}

// Usage
analyzeCode('print(hello world)', 'python')
  .then(result => console.log('Analysis result:', result))
  .catch(error => console.error('Error:', error));
```

## 🔗 Related Documentation

- **[Getting Started Guide](../guides/getting-started.md)** - Setup and basic usage
- **[Configuration Guide](../guides/configuration.md)** - Environment configuration
- **[Agent Architecture](../development/agent-architecture.md)** - System design details
- **[Development Setup](../development/development-setup.md)** - Local development

## 🆘 Support

- **Interactive Docs**: http://localhost/docs for live API testing
- **Issues**: Create GitHub issues for bugs or feature requests
- **FAQ**: See [FAQ](../guides/faq.md) for common questions 