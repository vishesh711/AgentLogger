# Development Setup

This guide will help you set up the AgentLogger project for development.

## Prerequisites

- Python 3.11+
- PostgreSQL 13+ (optional, SQLite can be used for development)
- Docker (optional, for sandbox execution and containerized deployment)
- Git

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

### 2. Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### 4. Set Up Environment Variables

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit the .env file with your settings
# Particularly, you'll need to set:
# - GROQ_API_KEY: Your Groq API key for AI functionality
# - DATABASE_URL: Your database connection string (SQLite is fine for development)
```

### 5. Set Up the Database

```bash
# Run database migrations
alembic upgrade head

# Seed the database with initial data (optional)
python scripts/init_db.py
```

### 6. Generate an API Key for Testing

```bash
python scripts/generate_api_key.py
# This will output an API key that you can use for testing
```

### 7. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

The API documentation will be available at:
- Swagger UI: http://localhost:8000/v1/docs
- ReDoc: http://localhost:8000/v1/redoc

## Development Workflow

### Code Style and Linting

We use the following tools for code quality:

- Black for code formatting
- isort for import sorting
- Flake8 for linting
- mypy for type checking

Run these tools before committing:

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint code
flake8 app tests

# Type check
mypy app
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test files
pytest tests/test_health.py
```

### Working with the CLI Tool

To develop and test the CLI tool:

```bash
# Install the CLI in development mode
pip install -e cli/

# Run the CLI
agent-logger --help
```

### Docker Development

You can also use Docker for development:

```bash
# Build and start the containers
docker-compose up -d

# Run commands inside the container
docker-compose exec api python scripts/generate_api_key.py

# Stop the containers
docker-compose down
```

## Debugging

### Sentry Integration

For local development, you can set up Sentry by:

1. Creating a free Sentry account
2. Creating a new project in Sentry
3. Adding your DSN to the `.env` file:

```
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=development
```

### Monitoring API Calls

The API includes middleware for monitoring API calls. You can enable it by setting:

```
ENABLE_ANALYTICS=true
ANALYTICS_PROVIDER=segment|mixpanel|posthog
ANALYTICS_API_KEY=your-analytics-api-key
```

## Next Steps

Once you have your development environment set up, check out:

- [Project Structure](project-structure.md) for an overview of the codebase
- [Agent Architecture](agent-architecture.md) to understand the agent system
- [Testing Guide](testing.md) for more details on testing
- [Database Migrations](database-migrations.md) for working with database changes 