# Code Analysis API

The Code Analysis API allows you to submit code for analysis and retrieve the results.

## Submit Code for Analysis

```
POST /api/v1/analyze
```

Submit code for analysis to detect potential bugs and issues.

### Request

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |
| `Content-Type` | Yes | Must be `application/json` |

#### Body

```json
{
  "code": "def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)\nprint(f\"Result: {result}\")",
  "language": "python",
  "filename": "example.py",
  "run_code": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | Yes | The code to analyze |
| `language` | string | Yes | The programming language of the code. Supported values: `python`, `javascript` |
| `filename` | string | No | The filename of the code (used for better error reporting) |
| `run_code` | boolean | No | Whether to run the code in a sandbox to detect runtime errors (default: `true`) |

### Response

#### 200 OK

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T10:30:00Z"
  },
  "message": "Analysis submitted successfully"
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
      "detail": "language must be one of: python, javascript"
    }
  ]
}
```

## Get Analysis Results

```
GET /api/v1/analyze/{analysis_id}
```

Retrieve the results of a previously submitted analysis.

### Request

#### Path Parameters

| Name | Required | Description |
|------|----------|-------------|
| `analysis_id` | Yes | The ID of the analysis |

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
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "completed",
    "created_at": "2023-06-15T10:30:00Z",
    "completed_at": "2023-06-15T10:30:05Z",
    "language": "python",
    "issues": [
      {
        "id": "issue-1",
        "type": "error",
        "message": "Division by zero",
        "severity": "high",
        "line_start": 4,
        "line_end": 4,
        "column_start": 15,
        "column_end": 23,
        "code_snippet": "result = divide(10, 0)",
        "fix_suggestions": [
          {
            "description": "Add a check for zero divisor",
            "code": "def divide(a, b):\n    if b == 0:\n        return \"Cannot divide by zero\"\n    return a / b"
          }
        ]
      }
    ],
    "execution_result": {
      "stdout": "",
      "stderr": "Traceback (most recent call last):\n  File \"example.py\", line 4, in <module>\n    result = divide(10, 0)\n  File \"example.py\", line 2, in divide\n    return a / b\nZeroDivisionError: division by zero\n",
      "exit_code": 1,
      "execution_time": 0.05
    }
  },
  "message": "Analysis completed successfully"
}
```

#### 200 OK (Pending)

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T10:30:00Z"
  },
  "message": "Analysis is still in progress"
}
```

#### 404 Not Found

```json
{
  "success": false,
  "data": null,
  "message": "Analysis not found",
  "errors": [
    {
      "code": "not_found",
      "detail": "Analysis with ID a1b2c3d4-e5f6-7890-abcd-ef1234567890 not found"
    }
  ]
}
```

## Run/Re-run Analysis

```
POST /api/v1/analyze/{analysis_id}/run
```

Run or re-run an analysis. This is useful if the analysis failed or if you want to update the analysis with new parameters.

### Request

#### Path Parameters

| Name | Required | Description |
|------|----------|-------------|
| `analysis_id` | Yes | The ID of the analysis |

#### Headers

| Name | Required | Description |
|------|----------|-------------|
| `X-API-Key` | Yes | Your API key |
| `Content-Type` | Yes | Must be `application/json` |

#### Body

```json
{
  "run_code": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `run_code` | boolean | No | Whether to run the code in a sandbox to detect runtime errors (default: `true`) |

### Response

#### 200 OK

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "pending",
    "created_at": "2023-06-15T10:30:00Z",
    "updated_at": "2023-06-15T10:35:00Z"
  },
  "message": "Analysis re-run initiated successfully"
}
```

#### 404 Not Found

```json
{
  "success": false,
  "data": null,
  "message": "Analysis not found",
  "errors": [
    {
      "code": "not_found",
      "detail": "Analysis with ID a1b2c3d4-e5f6-7890-abcd-ef1234567890 not found"
    }
  ]
}
```

## List Analyses

```
GET /api/v1/analyze
```

List all analyses for the authenticated user.

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

### Response

#### 200 OK

```json
{
  "success": true,
  "data": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "completed",
      "language": "python",
      "created_at": "2023-06-15T10:30:00Z",
      "completed_at": "2023-06-15T10:30:05Z",
      "issues_count": 1
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "status": "pending",
      "language": "javascript",
      "created_at": "2023-06-15T10:35:00Z",
      "completed_at": null,
      "issues_count": null
    }
  ],
  "message": "Analyses retrieved successfully",
  "pagination": {
    "total": 2,
    "page": 1,
    "limit": 10,
    "pages": 1
  }
}
``` 