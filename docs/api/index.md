# API Reference

Welcome to the AgentLogger API reference. This section provides detailed information about the available API endpoints, request/response formats, and authentication.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

All API endpoints (except for health check and documentation) require authentication using an API key. Include your API key in the `X-API-Key` header:

```
X-API-Key: your-api-key-here
```

## API Endpoints

### Health Check

- [Health Check](health.md): Check if the API is running

### Code Analysis

- [Code Analysis](analyze.md): Submit code for analysis and retrieve results

### Code Fixing

- [Code Fixing](fix.md): Request fixes for code issues and retrieve results

### Error Explanation

- [Error Explanation](explain.md): Get explanations for error messages

### GitHub Integration

- [GitHub Integration](github.md): Create pull requests with fixes

### User Management

- [User Management](users.md): Manage users

### API Key Management

- [API Key Management](api-keys.md): Manage API keys

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "errors": null
}
```

For error responses:

```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": [
    {
      "code": "error_code",
      "detail": "Detailed error message"
    }
  ]
}
```

## Rate Limiting

The API is rate-limited to protect the service. By default, the limit is 60 requests per minute per API key. Rate limit information is included in the response headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1620000000
```

## Pagination

List endpoints support pagination using the following query parameters:

- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 10, max: 100)

Pagination information is included in the response:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "pages": 10
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `authentication_error` | Invalid or missing API key |
| `validation_error` | Invalid request parameters |
| `not_found` | Resource not found |
| `rate_limit_exceeded` | Rate limit exceeded |
| `internal_error` | Internal server error |
| `bad_request` | Bad request |

## OpenAPI Documentation

The full OpenAPI documentation is available at `/docs` when running the API server. 