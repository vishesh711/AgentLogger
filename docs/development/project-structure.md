# Project Structure

This document explains the structure of the AgentLogger project.

## Directory Structure

```
AgentLogger/
├── alembic/                  # Database migrations
│   ├── versions/             # Migration versions
│   ├── env.py                # Alembic environment configuration
│   └── script.py.mako        # Migration script template
├── app/                      # Main application package
│   ├── api/                  # API routes and endpoints
│   │   ├── middleware/       # API middleware
│   │   └── v1/               # API v1 endpoints
│   │       ├── endpoints/    # API endpoint modules
│   │       └── router.py     # API router
│   ├── core/                 # Core functionality
│   │   ├── ai/               # AI integration
│   │   ├── config.py         # Configuration settings
│   │   ├── db.py             # Database connection
│   │   ├── middleware.py     # Middleware
│   │   ├── parsers/          # Code parsers
│   │   └── sandbox/          # Code execution sandbox
│   ├── models/               # Data models
│   │   ├── db/               # SQLAlchemy database models
│   │   └── schemas/          # Pydantic schemas
│   ├── services/             # Business logic services
│   │   ├── ai/               # AI services
│   │   ├── analysis_service.py  # Analysis service
│   │   ├── api_key_service.py   # API key service
│   │   ├── fix_service.py       # Fix service
│   │   ├── github/              # GitHub integration services
│   │   ├── github_service.py    # GitHub service
│   │   └── user_service.py      # User service
│   ├── utils/                # Utility functions
│   │   ├── parsing/          # Code parsing utilities
│   │   └── sandbox/          # Code execution sandbox utilities
│   ├── __init__.py           # Package initialization
│   └── main.py               # Application entry point
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   ├── guides/               # User guides
│   └── development/          # Development guides
├── scripts/                  # Utility scripts
│   ├── generate_api_key.py   # Script to generate API keys
│   └── init_db.py            # Script to initialize the database
├── tests/                    # Test suite
│   ├── conftest.py           # Test configuration
│   └── test_*.py             # Test modules
├── .env.sample               # Sample environment variables
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
├── LICENSE                   # License file
├── Makefile                  # Makefile for common tasks
├── README.md                 # Project README
└── requirements.txt          # Python dependencies
```

## Key Components

### API Layer (`app/api/`)

The API layer handles HTTP requests and responses. It is organized as follows:

- `middleware/`: Contains middleware for authentication, rate limiting, etc.
- `v1/`: Contains API v1 endpoints
  - `endpoints/`: Contains endpoint modules for different features
  - `router.py`: Configures the API router

### Core Layer (`app/core/`)

The core layer contains core functionality used throughout the application:

- `ai/`: AI integration components
- `config.py`: Configuration settings loaded from environment variables
- `db.py`: Database connection and session management
- `middleware.py`: Application middleware
- `parsers/`: Code parsers for different programming languages
- `sandbox/`: Code execution sandbox

### Models Layer (`app/models/`)

The models layer defines data models and schemas:

- `db/`: SQLAlchemy database models
  - `analysis.py`: Analysis model
  - `api_key.py`: API key model
  - `base.py`: Base model with common fields
  - `fix.py`: Fix model
  - `github.py`: GitHub integration model
  - `user.py`: User model
- `schemas/`: Pydantic schemas for request/response validation
  - `analysis.py`: Analysis schemas
  - `api_key.py`: API key schemas
  - `fix.py`: Fix schemas
  - `user.py`: User schemas

### Services Layer (`app/services/`)

The services layer contains business logic:

- `ai/`: AI services
  - `groq_client.py`: Groq API client
- `analysis_service.py`: Code analysis service
- `api_key_service.py`: API key management service
- `fix_service.py`: Code fixing service
- `github/`: GitHub integration services
- `github_service.py`: GitHub service
- `user_service.py`: User management service

### Utils Layer (`app/utils/`)

The utils layer contains utility functions:

- `parsing/`: Code parsing utilities
  - `base_parser.py`: Base parser class
  - `javascript_parser.py`: JavaScript parser
  - `parser_factory.py`: Parser factory
  - `python_parser.py`: Python parser
- `sandbox/`: Code execution sandbox utilities
  - `code_runner.py`: Code execution runner

### Scripts (`scripts/`)

The scripts directory contains utility scripts:

- `generate_api_key.py`: Script to generate API keys
- `init_db.py`: Script to initialize the database

### Tests (`tests/`)

The tests directory contains the test suite:

- `conftest.py`: Test configuration and fixtures
- `test_*.py`: Test modules for different features

## Module Dependencies

The dependencies between modules are as follows:

1. API endpoints depend on services
2. Services depend on models and utils
3. Models depend on core components
4. Utils depend on core components

This layered architecture helps maintain separation of concerns and makes the codebase easier to understand and maintain. 