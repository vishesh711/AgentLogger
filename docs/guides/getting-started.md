# Getting Started with AgentLogger

This guide will help you get started with using the AgentLogger API for code analysis and bug fixing.

## Prerequisites

Before you begin, make sure you have:

- An AgentLogger API key
- Python 3.11 or later (for running the examples)
- Basic knowledge of REST APIs

## Quick Start

### 1. Obtain an API Key

If you don't have an API key yet, you can generate one by running:

```bash
python scripts/generate_api_key.py
```

This will create an admin user and API key that you can use for testing.

### 2. Make Your First API Call

Here's a simple example of analyzing code for bugs:

```python
import requests

# Replace with your actual API key
api_key = "your_api_key_here"
headers = {"X-API-Key": api_key}

# Code to analyze
code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
print(f"Result: {result}")
"""

# Send analysis request
response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    headers=headers,
    json={"language": "python", "code": code}
)

# Get the analysis ID
analysis_id = response.json()["id"]
print(f"Analysis ID: {analysis_id}")

# Check analysis results
results = requests.get(
    f"http://localhost:8000/api/v1/analyze/{analysis_id}",
    headers=headers
)

# Print the issues found
issues = results.json().get("issues", [])
for issue in issues:
    print(f"Issue: {issue['message']}")
    print(f"Severity: {issue['severity']}")
    print(f"Line: {issue['line_start']}")
    print("---")
```

### 3. Request a Fix

Once you've identified an issue, you can request a fix:

```python
# Request a fix for the first issue
response = requests.post(
    "http://localhost:8000/api/v1/fix",
    headers=headers,
    json={
        "code": code,
        "language": "python",
        "error_message": "ZeroDivisionError: division by zero"
    }
)

fix_id = response.json()["id"]
print(f"Fix ID: {fix_id}")

# Get the fix results
fix_results = requests.get(
    f"http://localhost:8000/api/v1/fix/{fix_id}",
    headers=headers
)

fix = fix_results.json()
print(f"Fixed code:\n{fix['fixed_code']}")
print(f"Explanation:\n{fix['explanation']}")
```

## Using the Test Scripts

We've included several scripts to help you test the bug detection and automatic PR creation functionality:

### 1. Test Scripts

- `test_buggy_code.py`: A Python file with an intentional bug (division by zero)
- `test_agent_logger.py`: A script to test the full analysis and fix workflow
- `test_github_pr.py`: A script to directly test the GitHub PR creation

### 2. Update the API Key

Edit both `test_agent_logger.py` and `test_github_pr.py` and replace `"your_api_key_here"` with your actual API key:

```python
API_KEY = "your_actual_api_key"
```

### 3. Run the Test Scripts

To test code analysis and fix generation:

```bash
python test_agent_logger.py test_buggy_code.py
```

To test GitHub PR creation (requires GitHub integration):

```bash
python test_agent_logger.py test_buggy_code.py "yourusername/your-repo"
```

For more details on the test scripts, see the `TEST_README.md` file in the project root.

## Next Steps

- Explore the [API Reference](../api/index.md) to learn about all available endpoints
- Check out the [Configuration Guide](configuration.md) to customize AgentLogger
- See the [GitHub Integration Guide](github-integration.md) to set up automated PR creation

## Common Issues

- **API Key Invalid**: Make sure you're using the correct API key and including it in the `X-API-Key` header
- **Rate Limiting**: By default, the API is limited to 60 requests per minute
- **Unsupported Language**: Currently, AgentLogger supports Python and JavaScript. More languages will be added soon. 