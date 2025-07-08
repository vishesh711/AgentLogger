# Patch Generation API

The Patch Generation API creates patches in unified diff format to fix code issues.

## Endpoint

```
POST /v1/patch
```

## Authentication

This endpoint requires API key authentication. Include your API key in the `X-API-Key` header.

## Request

### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |
| `Content-Type` | Yes | Must be `application/json` |

### Body

```json
{
  "original_code": "string",
  "language": "string",
  "issue_description": "string",
  "context": "string"
}
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `original_code` | string | Yes | The original code with the issue |
| `language` | string | Yes | The programming language of the code (e.g., "python", "javascript") |
| `issue_description` | string | Yes | Description of the issue to fix |
| `context` | string | No | Additional context about the code or issue |

## Response

### Success Response

**Status Code**: `200 OK`

```json
{
  "patch": "string",
  "explanation": "string",
  "can_auto_apply": boolean
}
```

### Response Fields

| Name | Type | Description |
|------|------|-------------|
| `patch` | string | The generated patch in unified diff format |
| `explanation` | string | Explanation of what the patch does |
| `can_auto_apply` | boolean | Whether the patch can be automatically applied |

### Error Responses

**Status Code**: `400 Bad Request`

```json
{
  "detail": "string"
}
```

**Status Code**: `401 Unauthorized`

```json
{
  "detail": "Invalid API key"
}
```

**Status Code**: `500 Internal Server Error`

```json
{
  "detail": "An error occurred while generating the patch: string"
}
```

## Example

### Request

```bash
curl -X POST "https://api.agentlogger.ai/v1/patch" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "original_code": "def calculate_average(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total / len(numbers)\n\nresult = calculate_average([])",
    "language": "python",
    "issue_description": "The function crashes when given an empty list because it divides by zero",
    "context": "This function is used to calculate the average of a list of numbers"
  }'
```

### Response

```json
{
  "patch": "--- original.py\n+++ fixed.py\n@@ -1,6 +1,8 @@\n def calculate_average(numbers):\n+    if not numbers:\n+        return 0\n     total = 0\n     for num in numbers:\n         total += num\n     return total / len(numbers)\n \n result = calculate_average([])",
  "explanation": "This patch adds a check at the beginning of the function to handle the case of an empty list. If the list is empty, the function returns 0 instead of attempting to divide by zero. This prevents the ZeroDivisionError that would occur when trying to calculate the average of an empty list.",
  "can_auto_apply": true
}
``` 