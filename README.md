# AgentLogger API Platform

AgentLogger is an AI-powered debugging API service that helps developers detect, analyze, and fix code bugs using LLM agents.

## Features

- **Code Analysis**: Detect bugs and potential issues in code
- **Error Explanation**: Get detailed explanations of errors
- **Fix Generation**: Receive AI-generated fixes for detected bugs
- **GitHub Integration**: Create pull requests with fixes
- **Multi-language Support**: Works with Python, JavaScript, and more

## Project Structure

```
AgentLogger/
├── app/                    # Main application package
│   ├── api/                # API routes and endpoints
│   │   └── v1/             # API v1 endpoints
│   ├── core/               # Core functionality (config, db, middleware)
│   ├── models/             # Data models
│   │   ├── db/             # SQLAlchemy database models
│   │   └── schemas/        # Pydantic schemas for request/response
│   ├── services/           # Business logic services
│   │   ├── ai/             # AI services (LLM integration)
│   │   └── github/         # GitHub integration services
│   └── utils/              # Utility functions and helpers
│       ├── parsing/        # Code parsing utilities
│       └── sandbox/        # Code execution sandbox
├── tests/                  # Test suite
├── alembic/                # Database migrations
├── .env.sample             # Sample environment variables
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## API Endpoints

### Code Analysis

- `POST /api/v1/analyze`: Submit code for analysis
- `GET /api/v1/analyze/{analysis_id}`: Get analysis results
- `POST /api/v1/analyze/{analysis_id}/run`: Run/re-run analysis

### Code Fixing

- `POST /api/v1/fix`: Request a fix for a detected issue
- `GET /api/v1/fix/{fix_id}`: Get fix results
- `POST /api/v1/fix/{fix_id}/run`: Run/re-run fix generation

### Error Explanation

- `POST /api/v1/explain`: Get a simple explanation of an error message

### GitHub Integration

- `GET /api/v1/github/pr/{pr_id}/status`: Check PR status

### User Management

- `POST /api/v1/users`: Create a new user
- `GET /api/v1/users/{user_id}`: Get user details
- `PUT /api/v1/users/{user_id}`: Update user details
- `DELETE /api/v1/users/{user_id}`: Delete a user

### API Key Management

- `POST /api/v1/api-keys`: Create a new API key
- `GET /api/v1/api-keys/{api_key_id}`: Get API key details
- `PUT /api/v1/api-keys/{api_key_id}`: Update API key
- `DELETE /api/v1/api-keys/{api_key_id}`: Delete an API key

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (for sandbox execution)
- PostgreSQL
- Redis (optional, for caching)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/agentlogger-api
cd agentlogger-api
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.sample .env
# Edit .env with your API keys and configuration
```

5. Initialize the database
```bash
alembic upgrade head
```

6. Start the development server
```bash
uvicorn app.main:app --reload --port 8000
```

7. Visit the API documentation at http://localhost:8000/docs

## Usage Example

### Analyze Code for Issues

```python
import requests

api_key = "your_api_key"
headers = {"X-API-Key": api_key}

code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
print(f"Result: {result}")
"""

response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    headers=headers,
    json={"language": "python", "code": code}
)

analysis_id = response.json()["id"]
```

### Get Analysis Results

```python
response = requests.get(
    f"http://localhost:8000/api/v1/analyze/{analysis_id}",
    headers=headers
)

issues = response.json()["issues"]
for issue in issues:
    print(f"Issue: {issue['message']}")
```

### Request a Fix

```python
response = requests.post(
    "http://localhost:8000/api/v1/fix",
    headers=headers,
    json={
        "analysis_id": analysis_id,
        "issue_id": issues[0]["id"]
    }
)

fix_id = response.json()["id"]
```

### Get Fix Results

```python
response = requests.get(
    f"http://localhost:8000/api/v1/fix/{fix_id}",
    headers=headers
)

fix = response.json()
print(f"Fixed code:\n{fix['fixed_code']}")
print(f"Explanation:\n{fix['explanation']}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.