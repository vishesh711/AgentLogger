# Code Fixing API

The Code Fixing API allows you to request fixes for code issues and retrieve the results.

## Request a Fix

```
POST /api/v1/fix
```

Request a fix for a code issue.

### Request

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |
| `Content-Type` | Yes | Must be `application/json` |

#### Body

You can request a fix in one of two ways:

1. Using an analysis ID and issue ID:

```json
{
  "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "issue_id": "issue-1"
}
```

2. Directly providing the code and error message:

```json
{
  "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)\nprint(f\"Result: {result}\")",
  "language": "python",
  "error_message": "ZeroDivisionError: division by zero",
  "filename": "example.py"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `analysis_id` | string | For method 1 | The ID of the analysis containing the issue |
| `issue_id` | string | For method 1 | The ID of the issue to fix |
| `code` | string | For method 2 | The code containing the issue |
| `language` | string | For method 2 | The programming language of the code. Supported values: `python`, `javascript` |
| `error_message` | string | For method 2 | The error message or description of the issue |
| `filename` | string | No | The filename of the code (used for better error reporting) |

### Response

#### 200 OK

```json
{
  "success": true,
  "data": {
    "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T11:00:00Z"
  },
  "message": "Fix request submitted successfully"
}
```

#### 400 Bad Request

```json
{
  "success": false,
  "data": null,
  "message": "Invalid request",
  "errors": [
    {
      "code": "validation_error",
      "detail": "Either analysis_id and issue_id OR code, language, and error_message must be provided"
    }
  ]
}
```

## Get Fix Results

```
GET /api/v1/fix/{fix_id}
```

Retrieve the results of a previously submitted fix request.

### Request

#### Path Parameters

| Name | Required | Description |
|------|----------|-------------|
| `fix_id` | Yes | The ID of the fix request |

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |

### Response

#### 200 OK (Completed)

```json
{
  "success": true,
  "data": {
    "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
    "status": "completed",
    "created_at": "2023-06-15T11:00:00Z",
    "completed_at": "2023-06-15T11:00:10Z",
    "language": "python",
    "original_code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)\nprint(f\"Result: {result}\")",
    "fixed_code": "def divide(a, b):\n    if b == 0:\n        return \"Cannot divide by zero\"\n    return a / b\n\nresult = divide(10, 0)\nprint(f\"Result: {result}\")",
    "explanation": "The issue is a division by zero in the divide function. The fix adds a check for zero divisor and returns an error message instead of attempting the division when b is zero.",
    "diff": "@@ -1,5 +1,7 @@\n def divide(a, b):\n+    if b == 0:\n+        return \"Cannot divide by zero\"\n     return a / b\n \n result = divide(10, 0)\n",
    "execution_result": {
      "stdout": "Result: Cannot divide by zero\n",
      "stderr": "",
      "exit_code": 0,
      "execution_time": 0.05
    }
  },
  "message": "Fix completed successfully"
}
```

#### 200 OK (Pending)

```json
{
  "success": true,
  "data": {
    "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T11:00:00Z"
  },
  "message": "Fix is still in progress"
}
```

#### 404 Not Found

```json
{
  "success": false,
  "data": null,
  "message": "Fix not found",
  "errors": [
    {
      "code": "not_found",
      "detail": "Fix with ID f1e2d3c4-b5a6-7890-abcd-ef1234567890 not found"
    }
  ]
}
```

## Run/Re-run Fix

```
POST /api/v1/fix/{fix_id}/run
```

Run or re-run a fix. This is useful if the fix failed or if you want to update the fix with new parameters.

### Request

#### Path Parameters

| Name | Required | Description |
|------|----------|-------------|
| `fix_id` | Yes | The ID of the fix |

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |
| `Content-Type` | Yes | Must be `application/json` |

#### Body

```json
{
  "test_fix": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_fix` | boolean | No | Whether to run the fixed code in a sandbox to verify the fix (default: `true`) |

### Response

#### 200 OK

```json
{
  "success": true,
  "data": {
    "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T11:00:00Z",
    "updated_at": "2023-06-15T11:05:00Z"
  },
  "message": "Fix re-run initiated successfully"
}
```

#### 404 Not Found

```json
{
  "success": false,
  "data": null,
  "message": "Fix not found",
  "errors": [
    {
      "code": "not_found",
      "detail": "Fix with ID f1e2d3c4-b5a6-7890-abcd-ef1234567890 not found"
    }
  ]
}
```

## List Fixes

```
GET /api/v1/fix
```

List all fixes for the authenticated user.

### Request

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |

#### Query Parameters

| Name | Required | Description |
|------|----------|-------------|
| `page` | No | Page number (default: 1) |
| `limit` | No | Number of items per page (default: 10, max: 100) |
| `status` | No | Filter by status (`pending`, `completed`, `failed`) |
| `language` | No | Filter by language (`python`, `javascript`) |
| `analysis_id` | No | Filter by analysis ID |

### Response

#### 200 OK

```json
{
  "success": true,
  "data": [
    {
      "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
      "status": "completed",
      "language": "python",
      "created_at": "2023-06-15T11:00:00Z",
      "completed_at": "2023-06-15T11:00:10Z",
      "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    },
    {
      "id": "e2d3c4f1-a5b6-7890-abcd-ef1234567890",
      "status": "pending",
      "language": "javascript",
      "created_at": "2023-06-15T11:05:00Z",
      "completed_at": null,
      "analysis_id": null
    }
  ],
  "message": "Fixes retrieved successfully",
  "pagination": {
    "total": 2,
    "page": 1,
    "limit": 10,
    "pages": 1
  }
}
``` 