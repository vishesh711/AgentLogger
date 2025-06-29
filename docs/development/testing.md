# Testing Guide

This document provides information on how to run tests for the AgentLogger project and how to add new tests.

## Test Structure

The test suite is organized as follows:

- `tests/conftest.py`: Contains test fixtures and setup code
- `tests/test_health.py`: Tests for the health endpoint
- `tests/test_auth.py`: Tests for API key authentication
- `tests/test_api_keys.py`: Tests for API key generation

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

For more verbose output, use:

```bash
pytest -v
```

## Test Coverage

To run tests with coverage reporting, first install pytest-cov:

```bash
pip install pytest-cov
```

Then run:

```bash
pytest --cov=app
```

For a specific module:

```bash
pytest --cov=app.api.v1.endpoints.health tests/test_health.py
```

## Test Database

The tests use an in-memory SQLite database instead of the production PostgreSQL database. The test database is configured in `tests/conftest.py`.

Key features of the test database:

- Uses SQLite with in-memory storage for fast tests
- Creates simplified test models that use String types instead of UUID types (which SQLite doesn't support)
- Automatically creates and drops tables for each test

## Adding New Tests

When adding new tests:

1. Create a new test file in the `tests` directory
2. Use the fixtures defined in `conftest.py` (e.g., `client` and `db`)
3. Follow the existing test patterns

Example test:

```python
def test_example(client):
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
```

## Mocking External Services

For tests that require mocking external services (like AI providers or GitHub API), use pytest's monkeypatch fixture:

```python
def test_with_mock(client, monkeypatch):
    # Mock the external service
    def mock_service(*args, **kwargs):
        return {"result": "mocked_result"}
    
    monkeypatch.setattr("app.services.external_service.call_api", mock_service)
    
    # Test with the mocked service
    response = client.post("/api/v1/endpoint", json={"query": "test"})
    assert response.status_code == 200
```

## Testing Bug Detection and PR Creation

We've included several scripts in the root directory to help you test the bug detection and automatic PR creation functionality:

### Test Scripts

- `test_buggy_code.py`: A Python file with an intentional bug (division by zero)
- `test_agent_logger.py`: A script to test the full analysis and fix workflow
- `test_github_pr.py`: A script to directly test the GitHub PR creation

### Prerequisites for Testing

1. AgentLogger must be running locally on port 8000
2. You need a valid API key
3. For GitHub PR creation, you need to have GitHub integration configured in your .env file

### Using the Test Scripts

1. **Generate an API Key**

   If you don't have an API key yet, generate one:

   ```bash
   python scripts/generate_api_key.py
   ```

2. **Update the Test Scripts**

   Edit both `test_agent_logger.py` and `test_github_pr.py` and replace `"your_api_key_here"` with your actual API key:

   ```python
   API_KEY = "your_actual_api_key"
   ```

3. **Test Code Analysis and Fix Generation**

   To test code analysis and fix generation:

   ```bash
   python test_agent_logger.py test_buggy_code.py
   ```

   This will:
   - Submit the buggy code for analysis
   - Get the analysis results (detected issues)
   - Request a fix for the first issue
   - Get the fix results (fixed code and explanation)

4. **Test GitHub PR Creation (Full Flow)**

   To test the full flow including GitHub PR creation, provide your GitHub repository name:

   ```bash
   python test_agent_logger.py test_buggy_code.py "yourusername/your-repo"
   ```

5. **Test Direct GitHub PR Creation**

   To directly test just the GitHub PR creation functionality:

   ```bash
   python test_github_pr.py "yourusername/your-repo" "fix-branch-name"
   ```

   The branch name is optional and will default to "fix-division-by-zero" if not provided.

### GitHub Integration Requirements

For GitHub integration to work, you need to have the following in your .env file:

```
GITHUB_ACCESS_TOKEN=your-github-token
```

The GitHub token needs to have permissions to create branches and pull requests in the specified repository.

For more details on the test scripts, see the `TEST_README.md` file in the project root.

## Continuous Integration

Tests are automatically run on pull requests and commits to the main branch. Ensure all tests pass before submitting a pull request. 