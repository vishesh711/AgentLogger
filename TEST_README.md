# Testing AgentLogger

This README explains how to test the AgentLogger's bug detection and automatic PR creation functionality.

## Prerequisites

1. AgentLogger must be running locally on port 8000
2. You need a valid API key
3. For GitHub PR creation, you need to have GitHub integration configured in your .env file

## Files

- `test_buggy_code.py`: A Python file with an intentional bug (division by zero)
- `test_agent_logger.py`: A script to test the AgentLogger API
- `test_github_pr.py`: A script to directly test the GitHub PR creation functionality

## Steps to Test

### 1. Generate an API Key

If you don't have an API key yet, generate one:

```bash
python scripts/generate_api_key.py
```

### 2. Update the Test Scripts

Edit both `test_agent_logger.py` and `test_github_pr.py` and replace `"your_api_key_here"` with your actual API key:

```python
API_KEY = "your_actual_api_key"
```

### 3. Test Code Analysis and Fix Generation

To test code analysis and fix generation:

```bash
python test_agent_logger.py test_buggy_code.py
```

This will:
- Submit the buggy code for analysis
- Get the analysis results (detected issues)
- Request a fix for the first issue
- Get the fix results (fixed code and explanation)

### 4. Test GitHub PR Creation (Full Flow)

To test the full flow including GitHub PR creation, provide your GitHub repository name:

```bash
python test_agent_logger.py test_buggy_code.py "yourusername/your-repo"
```

### 5. Test Direct GitHub PR Creation

To directly test just the GitHub PR creation functionality:

```bash
python test_github_pr.py "yourusername/your-repo" "fix-branch-name"
```

The branch name is optional and will default to "fix-division-by-zero" if not provided.

Note: For GitHub integration to work, you need to have the following in your .env file:

```
GITHUB_ACCESS_TOKEN=your-github-token
```

## Expected Output

The scripts will output:
1. Analysis ID
2. Detected issues
3. Fix ID
4. Fixed code
5. Explanation of the fix
6. PR URL (if GitHub integration is used)

## Troubleshooting

If you encounter errors:

1. Make sure AgentLogger is running (`uvicorn app.main:app --reload --port 8000`)
2. Check that your API key is valid
3. Verify that your .env file has the correct configuration
4. For GitHub PR creation, ensure your GitHub access token has the necessary permissions
5. Check the server logs for more detailed error information 