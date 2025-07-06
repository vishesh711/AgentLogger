# AgentLogger API Documentation

AgentLogger provides a comprehensive REST API for AI-powered code analysis, debugging, and fix generation. This documentation covers all available endpoints, authentication, and usage examples.

## 🏗️ Architecture Overview

AgentLogger uses a clear separation between **server-side** (FastAPI backend) and **client-side** (React frontend) with well-defined API contracts and authentication flows.

### Quick Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT SIDE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  React App (Port 5173/80)                                                  │
│  ├── Authentication Context (JWT Management)                               │
│  ├── API Client (lib/api.ts)                                              │
│  ├── Protected Routes                                                      │
│  └── UI Components                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                  HTTP API Calls
                                       │
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER SIDE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  FastAPI Backend (Port 8000)                                              │
│  ├── API Endpoints (/api/v1/*)                                           │
│  ├── Authentication Middleware                                            │
│  ├── Agent System (AI Processing)                                         │
│  ├── Database Services                                                    │
│  └── Background Tasks                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**📚 For detailed architecture information, see:**
- **[Server-Client Architecture](SERVER_CLIENT_ARCHITECTURE.md)** - Complete architectural overview
- **[API Usage Examples](API_USAGE_EXAMPLES.md)** - Practical implementation examples

## 🚀 Quick Start

### Base URL
```
# Production/Docker
http://localhost/api/v1

# Development
http://localhost:8000/api/v1
```

### Authentication Methods

AgentLogger supports two authentication methods:

1. **JWT Tokens** (Web Interface)
   - Used by the React frontend
   - Header: `Authorization: Bearer {token}`
   - Obtained via `/auth/login` endpoint

2. **API Keys** (Programmatic Access)
   - Used for external integrations
   - Header: `X-API-Key: {api_key}`
   - Managed via `/api-keys` endpoints

### Quick Test with Default API Key
For immediate testing, use this pre-configured key:
```bash
curl -X POST http://localhost/api/v1/analyze/quick \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

## 📊 Interactive Documentation

AgentLogger provides interactive API documentation:

- **Swagger UI**: http://localhost/docs (or http://localhost:8000/docs in dev)
- **ReDoc**: http://localhost/redoc
- **OpenAPI Schema**: http://localhost/api/v1/openapi.json

## 🔑 Complete API Endpoints Reference

### Authentication & User Management

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|---------------|
| `/auth/login` | POST | User login | None |
| `/auth/register` | POST | User registration | None |
| `/auth/github/authorize` | GET | GitHub OAuth URL | None |
| `/auth/google/authorize` | GET | Google OAuth URL | None |
| `/users/me` | GET | Get current user | JWT |
| `/users/` | GET | List users (admin) | JWT |

### API Key Management

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|---------------|
| `/api-keys/` | GET | List user's API keys | JWT |
| `/api-keys/` | POST | Create new API key | JWT |
| `/api-keys/{id}` | GET | Get specific API key | JWT |
| `/api-keys/{id}` | PUT | Update API key | JWT |
| `/api-keys/{id}` | DELETE | Delete API key | JWT |

### Core Analysis Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|---------------|
| `/analyze/quick` | POST | Quick code analysis | JWT/API Key |
| `/analyze/` | POST | Create analysis request | JWT/API Key |
| `/analyze/{id}` | GET | Get analysis result | JWT/API Key |
| `/analyze/{id}/run` | POST | Run/re-run analysis | JWT/API Key |
| `/fix/` | POST | Generate code fix | JWT/API Key |
| `/fix/{id}` | GET | Get fix result | JWT/API Key |
| `/explain/` | POST | Explain error message | JWT/API Key |

### System & Monitoring

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|---------------|
| `/health/` | GET | System health status | None |
| `/agent-debug/test-full-workflow` | POST | Test agent workflow | JWT/API Key |
| `/github/pr/{id}/status` | GET | Check PR status | JWT/API Key |

## 🔧 Core Analysis API

### 1. Quick Code Analysis

**POST** `/api/v1/analyze/quick`

Perform immediate code analysis with real-time results.

**Request:**
```json
{
  "code": "print(hello world)",
  "language": "python",
  "traceback": "SyntaxError: invalid syntax"
}
```

**Response:**
```json
{
  "request_id": "uuid-here",
  "status": "completed",
  "issues": [
    {
      "type": "syntax_error",
      "severity": "high",
      "message": "Missing quotes around string literal",
      "line_start": 1,
      "code_snippet": "print(hello world)"
    }
  ]
}
```

**Frontend Implementation:**
```typescript
// From: frontend/src/pages/Playground.tsx
const handleAnalyze = async () => {
  const result = await quickAnalyzeCode({
    code: codeInput,
    language: selectedLanguage,
    traceback: tracebackInput
  });
  setAnalysisResult(result);
};
```

### 2. Fix Generation

**POST** `/api/v1/fix`

Generate AI-powered fixes for code issues.

**Request:**
```json
{
  "code": "print(hello world)",
  "language": "python",
  "error_message": "SyntaxError: invalid syntax",
  "context": "Function should print greeting"
}
```

**Response:**
```json
{
  "id": "fix-uuid-here",
  "status": "pending",
  "code": "print(hello world)",
  "language": "python",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 3. Error Explanation

**POST** `/api/v1/explain`

Get detailed, level-appropriate explanations of errors.

**Request:**
```json
{
  "error_trace": "SyntaxError: invalid syntax",
  "code_context": "print(hello world)",
  "language": "python",
  "user_level": "beginner"
}
```

**Response:**
```json
{
  "explanation": {
    "simple": "You forgot to put quotes around your text",
    "detailed": "In Python, text strings must be enclosed in quotes...",
    "technical": "The parser expected a string literal..."
  },
  "learning_resources": ["python-strings-tutorial"],
  "related_concepts": ["string literals", "syntax errors"]
}
```

## 🔐 Authentication Examples

### JWT Authentication (Web Interface)

```typescript
// Frontend login flow
const response = await login({ email, password });
localStorage.setItem('jwt_token', response.access_token);

// Subsequent API calls
const user = await getCurrentUser(); // Automatically includes JWT token
```

### API Key Authentication (Programmatic)

```bash
# Create API key (requires JWT)
curl -X POST http://localhost/api/v1/api-keys \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Development Key"}'

# Use API key for analysis
curl -X POST http://localhost/api/v1/analyze/quick \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(hello)", "language": "python"}'
```

## 📝 Request/Response Schemas

### Common Request Fields

```typescript
interface AnalysisRequestCreate {
  code: string;           // Required: Code to analyze
  language: string;       // Required: python, javascript
  traceback?: string;     // Optional: Error traceback
}

interface FixRequestCreate {
  code: string;
  language: string;
  error_message?: string;
  context?: string;
  analysis_id?: string;
}
```

### Common Response Fields

```typescript
interface AnalysisResult {
  request_id: string;
  status: "pending" | "completed" | "failed";
  issues?: CodeIssue[];
  error?: string;
  analysis_summary?: string;
}

interface CodeIssue {
  type: string;
  severity: "low" | "medium" | "high" | "critical";
  message: string;
  line_start?: number;
  line_end?: number;
  code_snippet?: string;
}
```

## 🔒 Authentication & Security

### JWT Token Management
- **Lifetime**: 24 hours (configurable)
- **Storage**: localStorage (frontend)
- **Renewal**: Automatic refresh on valid requests
- **Scope**: User-specific access control

### API Key Features
- **User-Specific**: Each key belongs to one user
- **Naming**: Custom names for organization
- **Revocation**: Instant key deletion
- **Security**: One-time display after creation
- **Tracking**: Last used timestamp

### Rate Limiting
- **Default**: 60 requests per minute per key
- **Headers**: Rate limit info in responses
- **Enforcement**: Middleware-level protection

## 🔄 Data Flow Patterns

### Frontend → Backend Flow

1. **User Action** (e.g., click "Analyze")
2. **Client Validation** (check inputs)
3. **API Request** (with authentication)
4. **Server Processing** (agent system)
5. **Database Storage** (results)
6. **Response** (to frontend)
7. **UI Update** (display results)

### Agent System Integration

```python
# Server-side processing flow
@router.post("/analyze/quick")
async def quick_analyze(
    data: AnalysisRequestCreate,
    request: Request,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    # 1. Validate authentication
    user_id = getattr(request.state, 'user_id', None)
    
    # 2. Process with agent system
    result = await agent_system.process_analysis(data, user_id)
    
    # 3. Return structured response
    return result
```

## 🚦 HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | Success | Successful operation |
| 201 | Created | Resource created (API key, user) |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Pydantic validation failed |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Internal server error |

## 🔧 Development & Testing

### Local Development Setup

```bash
# Backend (Terminal 1)
python -m uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend && npm run dev

# Test API
curl http://localhost:8000/health
```

### Integration Testing

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Create API key (use JWT from login)
curl -X POST http://localhost:8000/api/v1/api-keys \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Key"}'

# Analyze code
curl -X POST http://localhost:8000/api/v1/analyze/quick \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(hello)", "language": "python"}'
```

## 📚 Additional Resources

### Comprehensive Documentation
- **[Server-Client Architecture](SERVER_CLIENT_ARCHITECTURE.md)** - Detailed architectural overview
- **[API Usage Examples](API_USAGE_EXAMPLES.md)** - Real-world implementation examples
- **[Getting Started Guide](../guides/getting-started.md)** - Setup and basic usage
- **[Configuration Guide](../guides/configuration.md)** - Environment configuration
- **[Agent Architecture](../development/agent-architecture.md)** - System design details
- **[Development Setup](../development/development-setup.md)** - Local development

### Interactive Tools
- **Swagger UI**: http://localhost/docs - Live API testing
- **ReDoc**: http://localhost/redoc - Beautiful API documentation
- **Playground**: http://localhost/playground - Web interface for testing

## 🆘 Support

- **Interactive Docs**: http://localhost/docs for live API testing
- **GitHub Issues**: Report bugs or request features
- **Architecture Docs**: [SERVER_CLIENT_ARCHITECTURE.md](SERVER_CLIENT_ARCHITECTURE.md) for detailed system design
- **Usage Examples**: [API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md) for practical implementations

This comprehensive API documentation ensures clear understanding of both server-side and client-side integration patterns for AgentLogger. 