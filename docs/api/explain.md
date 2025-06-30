# Error Explanation API

The Error Explanation API helps developers understand error messages by providing explanations at different levels of detail.

## Endpoint

```
POST /v1/explain
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
  "error_trace": "string",
  "code_context": "string",
  "language": "string",
  "user_level": "string"
}
```

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `error_trace` | string | Yes | The error message or stack trace |
| `code_context` | string | Yes | The code that generated the error |
| `language` | string | Yes | The programming language of the code (e.g., "python", "javascript") |
| `user_level` | string | No | User experience level: "beginner", "intermediate", or "advanced". Default: "intermediate" |

## Response

### Success Response

**Status Code**: `200 OK`

```json
{
  "explanation": {
    "simple": "string",
    "detailed": "string",
    "technical": "string"
  },
  "learning_resources": [
    {
      "title": "string",
      "url": "string",
      "description": "string",
      "resource_type": "string"
    }
  ],
  "related_concepts": [
    "string"
  ]
}
```

### Response Fields

| Name | Type | Description |
|------|------|-------------|
| `explanation.simple` | string | Simple explanation for beginners |
| `explanation.detailed` | string | Detailed explanation with more context |
| `explanation.technical` | string | Technical explanation with programming concepts |
| `learning_resources` | array | List of relevant learning resources |
| `learning_resources[].title` | string | Title of the resource |
| `learning_resources[].url` | string | URL of the resource |
| `learning_resources[].description` | string | Brief description of the resource |
| `learning_resources[].resource_type` | string | Type of resource (article, video, documentation) |
| `related_concepts` | array | List of related programming concepts |

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
  "detail": "An error occurred while generating the explanation: string"
}
```

## Example

### Request

```bash
curl -X POST "https://api.agentlogger.ai/v1/explain" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "error_trace": "TypeError: cannot unpack non-iterable int object",
    "code_context": "def process_data(data):\n    x, y = data\n    return x + y\n\nresult = process_data(42)",
    "language": "python",
    "user_level": "beginner"
  }'
```

### Response

```json
{
  "explanation": {
    "simple": "You're trying to split a single number into two parts, but that's not possible. The error happens because you can't unpack a single number (42) into two variables (x and y).",
    "detailed": "In Python, when you write 'x, y = data', you're trying to unpack the value in 'data' into two separate variables. This works with lists, tuples, and other collections that have multiple items, but not with single numbers like integers. In your code, you're passing the number 42 to the function, then trying to unpack it into x and y, which causes the error.",
    "technical": "The error 'TypeError: cannot unpack non-iterable int object' occurs when attempting to use iterable unpacking syntax on a non-iterable object. Integers in Python are atomic values and don't support the iteration protocol required for unpacking. The function expects an iterable with at least two elements that can be unpacked into the variables x and y, but instead receives an int (42), which cannot be unpacked."
  },
  "learning_resources": [
    {
      "title": "Python Unpacking Tutorial",
      "url": "https://realpython.com/python-unpacking-tutorial/",
      "description": "A comprehensive guide to unpacking in Python",
      "resource_type": "article"
    },
    {
      "title": "Python TypeError Documentation",
      "url": "https://docs.python.org/3/library/exceptions.html#TypeError",
      "description": "Official documentation on TypeError exceptions",
      "resource_type": "documentation"
    }
  ],
  "related_concepts": [
    "Iterable unpacking",
    "Python sequence types",
    "TypeError exceptions",
    "Function parameters"
  ]
}
``` 