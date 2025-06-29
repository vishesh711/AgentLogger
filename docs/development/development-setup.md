# Development Setup

This guide will help you set up your development environment for working on the AgentLogger project.

## Prerequisites

- Python 3.11 or later
- PostgreSQL 13 or later
- Docker (for sandbox execution)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

## Step 2: Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 3: Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp setup_groq_key.txt .env
```

Edit the `.env` file to include your development configuration:

```
# Project settings
PROJECT_NAME=AgentLogger API (Dev)
PROJECT_DESCRIPTION=AI-powered debugging API service
VERSION=0.1.0

# API settings
API_V1_STR=/api/v1

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Database settings
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=agentlogger_dev

# Redis settings (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
USE_REDIS=false

# Security settings
SECRET_KEY=dev-secret-key-change-in-production

# LLM settings
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192

# GitHub integration (optional)
GITHUB_ACCESS_TOKEN=your-github-token

# Sandbox execution
USE_DOCKER_SANDBOX=true
EXECUTION_TIMEOUT=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=60
```

## Step 5: Set Up the Database

Make sure PostgreSQL is running, then create the development database:

```bash
createdb agentlogger_dev
```

Run the database migrations:

```bash
alembic upgrade head
```

Initialize the database with test data:

```bash
python scripts/init_db.py
```

## Step 6: Generate an API Key for Development

```bash
python scripts/generate_api_key.py
```

This will create an admin user and API key that you can use for development.

## Step 7: Start the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API should now be accessible at http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## Development Workflow

### Code Style

We use Black for code formatting, Flake8 for linting, and MyPy for type checking:

```bash
# Format code
black app tests

# Lint code
flake8 app tests

# Type check code
mypy app
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run a specific test file
pytest tests/test_health.py
```

### Database Migrations

If you make changes to the database models, you need to create a new migration:

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply the migration
alembic upgrade head

# Downgrade to a specific revision
alembic downgrade revision_id
```

### Working with Docker

For development with Docker:

```bash
# Build the Docker image
docker-compose build

# Start the services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the services
docker-compose down
```

## Debugging

### FastAPI Debug Mode

FastAPI's debug mode is enabled by default when using `--reload` with Uvicorn.

### Database Debugging

You can connect to the PostgreSQL database using psql:

```bash
psql -U postgres -d agentlogger_dev
```

### API Debugging

You can use the Swagger UI at http://localhost:8000/docs to test API endpoints.

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Make sure PostgreSQL is running
2. Verify the database connection details in your `.env` file
3. Check that the database exists and the user has appropriate permissions

### API Key Authentication Issues

If you encounter API key authentication issues:

1. Make sure you've generated an API key using `scripts/generate_api_key.py`
2. Make sure you're including the API key in the `X-API-Key` header
3. Check that the API key is valid in the database

### Docker Issues

If you encounter Docker issues:

1. Make sure Docker is running
2. Try rebuilding the Docker image: `docker-compose build --no-cache`
3. Check Docker logs: `docker-compose logs -f` 