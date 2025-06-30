# API Documentation

Welcome to the AgentLogger API documentation. This guide provides information on how to use the AgentLogger API to analyze code, fix issues, explain errors, and generate patches.

## API Endpoints

The API is organized into the following endpoints:

- [Analyze](analyze.md): Analyze code for issues
- [Fix](fix.md): Generate fixes for identified issues
- [Explain](explain.md): Get multi-level explanations for error messages
- [Patch](patch.md): Generate patches in unified diff format
- [GitHub Integration](github.md): Create pull requests with fixes
- [API Keys](api-keys.md): Manage API keys
- [Health](health.md): Check API health

## Base URL

When running with Docker Compose (the recommended setup) nginx proxies the backend, so the base URL is:

```
http://localhost/api/v1
```

If you decide to bypass nginx and hit the backend container directly, use `http://localhost:8000/api/v1` and **remember to include the `X-API-Key` header** even for the `/docs` Swagger UI.

## Authentication

All API requests require an API key. You can generate an API key using the `/api/v1/api-keys` endpoint or the `scripts/generate_api_key.py` script.

To authenticate your requests, include your API key in the `X-API-Key` header:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code here",
    "language": "python"
  }'
```

## Rate Limiting

The API has rate limiting to prevent abuse. By default, each API key is limited to 60 requests per minute. If you exceed this limit, you will receive a 429 Too Many Requests response.

## Error Handling

The API uses standard HTTP status codes to indicate success or failure:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: The API key is invalid or missing
- `404 Not Found`: The requested resource was not found
- `429 Too Many Requests`: The rate limit was exceeded
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON object with a `detail` field that provides more information about the error:

```json
{
  "detail": "Invalid API key"
}
```

## Versioning

The API is versioned to ensure backward compatibility. The current version is `v1`. All endpoints are prefixed with `/api/v1/`.

## Monitoring and Analytics

The API includes monitoring and analytics to track usage and performance. This information is used to improve the API and identify issues.

## Sandbox Execution

Some endpoints may execute code in a secure sandbox to validate fixes or reproduce issues. The sandbox is isolated from the rest of the system and has limited resources.

## Examples

### Analyze Code

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python"
  }'
```

### Fix Issues

```bash
curl -X POST "http://localhost:8000/api/v1/fix" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "analysis-id-from-analyze-endpoint",
    "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python"
  }'
```

### Explain Errors

```bash
curl -X POST "http://localhost:8000/api/v1/explain" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "error_trace": "ZeroDivisionError: division by zero",
    "code_context": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "user_level": "beginner"
  }'
```

### Generate Patches

```bash
curl -X POST "http://localhost:8000/api/v1/patch" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "original_code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)",
    "language": "python",
    "issue_description": "Division by zero error"
  }'
```

### Manage API Keys

```bash
# List all API keys
curl -X GET "http://localhost:8000/api/v1/api-keys" \
  -H "X-API-Key: your-api-key"

# Create a new API key
curl -X POST "http://localhost:8000/api/v1/api-keys" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key"
  }'

# Delete an API key
curl -X DELETE "http://localhost:8000/api/v1/api-keys/{key_id}" \
  -H "X-API-Key: your-api-key"
```

### Check API Health

```bash
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "X-API-Key: your-api-key"
```

## Next Steps

- [Getting Started Guide](../guides/getting-started.md): Learn how to get started with the AgentLogger API
- [CLI Tool](../guides/cli.md): Learn how to use the AgentLogger CLI tool
- [Configuration Guide](../guides/configuration.md): Learn how to configure the AgentLogger API 