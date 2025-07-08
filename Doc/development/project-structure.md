# Project Structure

This document provides an overview of the AgentLogger project structure.

## Directory Structure

```
AgentLogger/
├── alembic/                  # Database migration scripts
│   └── versions/             # Migration versions
├── app/                      # Main application package
│   ├── agents/               # Agent-based architecture components
│   │   ├── base_agent.py     # Base agent class
│   │   ├── coordinator_agent.py  # Orchestration agent
│   │   ├── analyzer_agent.py # Code analysis agent
│   │   └── fix_generator_agent.py # Fix generation agent
│   ├── api/                  # API routes and endpoints
│   │   └── v1/               # API v1 endpoints
│   │       ├── endpoints/    # API endpoint modules
│   │       └── router.py     # API router configuration
│   ├── core/                 # Core functionality
│   │   ├── ai/               # AI-related core functionality
│   │   ├── config.py         # Application configuration
│   │   ├── db.py             # Database connection and session management
│   │   ├── middleware.py     # Middleware components
│   │   ├── parsers/          # Code parsing functionality
│   │   └── sandbox/          # Code execution sandbox
│   ├── models/               # Data models
│   │   ├── db/               # SQLAlchemy database models
│   │   └── schemas/          # Pydantic schemas for request/response
│   ├── services/             # Business logic services
│   │   ├── ai/               # AI services (LLM integration)
│   │   ├── analysis_service.py # Code analysis service
│   │   ├── api_key_service.py  # API key management
│   │   ├── fix_service.py      # Fix generation service
│   │   ├── github/           # GitHub integration services
│   │   ├── github_service.py   # GitHub service
│   │   ├── monitoring_service.py # Analytics and monitoring service
│   │   └── user_service.py     # User management service
│   ├── utils/                # Utility functions and helpers
│   │   ├── parsing/          # Code parsing utilities
│   │   └── sandbox/          # Code execution sandbox utilities
│   └── main.py               # Application entry point
├── cli/                      # Command-line interface
│   ├── agent_logger_cli.py   # CLI implementation
│   ├── setup.py              # CLI package setup
│   └── __init__.py           # CLI package initialization
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   ├── assets/               # Documentation assets
│   ├── development/          # Development guides
│   └── guides/               # User guides
├── nginx/                    # Nginx configuration for production
│   └── conf.d/               # Nginx site configurations
├── tests/                    # Test suite
│   ├── integration/          # Integration tests
│   └── unit/                 # Unit tests
├── .github/                  # GitHub configuration
│   └── workflows/            # GitHub Actions workflows
├── alembic.ini               # Alembic configuration
├── docker-compose.yml        # Docker Compose configuration for development
├── docker-compose.prod.yml   # Docker Compose configuration for production
├── Dockerfile                # Docker configuration for development
├── Dockerfile.prod           # Docker configuration for production
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Key Components

### Agents

The `app/agents/` directory contains the agent-based architecture components:

- `base_agent.py`: Abstract base class for all agents
- `coordinator_agent.py`: Orchestrates the debugging process
- `analyzer_agent.py`: Analyzes code for issues
- `fix_generator_agent.py`: Generates fixes for identified issues

### API

The `app/api/` directory contains the API routes and endpoints:

- `v1/endpoints/`: API endpoint modules
  - `analyze.py`: Code analysis endpoints
  - `fix.py`: Fix generation endpoints
  - `explain.py`: Error explanation endpoints
  - `patch.py`: Patch generation endpoints
  - `github.py`: GitHub integration endpoints
  - `users.py`: User management endpoints
  - `api_keys.py`: API key management endpoints
  - `health.py`: Health check endpoint
  - `agent_debug.py`: Agent-based debugging endpoints
- `v1/router.py`: API router configuration

### Core

The `app/core/` directory contains core functionality:

- `config.py`: Application configuration
- `db.py`: Database connection and session management
- `middleware.py`: Middleware components (authentication, rate limiting, analytics)

### Models

The `app/models/` directory contains data models:

- `db/`: SQLAlchemy database models
  - `base.py`: Base model class
  - `user.py`: User model
  - `api_key.py`: API key model
  - `analysis.py`: Analysis model
  - `fix.py`: Fix model
  - `github.py`: GitHub integration model
- `schemas/`: Pydantic schemas for request/response validation
  - `user.py`: User schemas
  - `api_key.py`: API key schemas
  - `analysis.py`: Analysis schemas
  - `fix.py`: Fix schemas
  - `explain.py`: Error explanation schemas
  - `patch.py`: Patch generation schemas

### Services

The `app/services/` directory contains business logic services:

- `ai/`: AI services (LLM integration)
  - `groq_client.py`: Client for interacting with Groq LLM API
- `analysis_service.py`: Code analysis service
- `api_key_service.py`: API key management service
- `fix_service.py`: Fix generation service
- `github_service.py`: GitHub integration service
- `monitoring_service.py`: Analytics and monitoring service
- `user_service.py`: User management service

### Utils

The `app/utils/` directory contains utility functions and helpers:

- `parsing/`: Code parsing utilities
  - `base_parser.py`: Base parser class
  - `python_parser.py`: Python code parser
  - `javascript_parser.py`: JavaScript code parser
  - `parser_factory.py`: Factory for creating parsers
- `sandbox/`: Code execution sandbox utilities
  - `code_runner.py`: Code execution utilities

### CLI

The `cli/` directory contains the command-line interface:

- `agent_logger_cli.py`: CLI implementation
- `setup.py`: CLI package setup
- `__init__.py`: CLI package initialization

### Tests

The `tests/` directory contains the test suite:

- `integration/`: Integration tests
- `unit/`: Unit tests
- `conftest.py`: Test fixtures and configuration

### Documentation

The `docs/` directory contains documentation:

- `api/`: API documentation
- `development/`: Development guides
- `guides/`: User guides

### Deployment

- `docker-compose.yml`: Docker Compose configuration for development
- `docker-compose.prod.yml`: Docker Compose configuration for production
- `Dockerfile`: Docker configuration for development
- `Dockerfile.prod`: Docker configuration for production
- `nginx/`: Nginx configuration for production

## Design Patterns

### Dependency Injection

The application uses FastAPI's dependency injection system for:
- Database sessions
- Authentication
- Service dependencies

### Repository Pattern

The application uses the repository pattern for data access:
- Service layers handle business logic
- Database models handle data persistence
- Pydantic schemas handle data validation

### Factory Pattern

The application uses the factory pattern for:
- Parser creation based on language
- Agent creation based on task

### Agent-Based Architecture

The application uses an agent-based architecture for debugging:
- Coordinator agent orchestrates the debugging process
- Analyzer agent analyzes code for issues
- Fix generator agent generates fixes for identified issues

## Key Workflows

### Code Analysis Workflow

1. User submits code for analysis
2. Code is parsed and analyzed
3. Issues are identified and stored
4. Analysis results are returned to the user

### Fix Generation Workflow

1. User requests a fix for an identified issue
2. Fix generator agent creates a fix
3. Fix is validated and stored
4. Fix is returned to the user

### Error Explanation Workflow

1. User submits an error message and code context
2. Error is analyzed by the AI
3. Multi-level explanations are generated
4. Explanations are returned to the user

### Patch Generation Workflow

1. User submits code and issue description
2. Patch generator creates a unified diff patch
3. Patch is validated
4. Patch is returned to the user

### GitHub Integration Workflow

1. User requests a GitHub PR for a fix
2. GitHub service creates a branch and commits the fix
3. GitHub service creates a PR
4. PR details are returned to the user 