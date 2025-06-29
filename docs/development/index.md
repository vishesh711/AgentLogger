# Development Guide

This section contains information for developers who want to contribute to the AgentLogger project or understand its internal architecture.

## Table of Contents

- [Project Structure](project-structure.md)
- [Development Setup](development-setup.md)
- [Code Style Guide](code-style-guide.md)
- [Database Migrations](database-migrations.md)
- [Testing](testing.md)
- [API Design](api-design.md)
- [Contributing](contributing.md)

## Overview

AgentLogger is built using modern Python technologies:

- **FastAPI**: A modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Pydantic**: Data validation and settings management using Python type hints
- **Alembic**: Database migration tool
- **Groq API**: Large Language Model API for AI-powered code analysis and fixes

The application follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Contains business logic
3. **Model Layer**: Defines data models and schemas
4. **Infrastructure Layer**: Handles database connections, external APIs, etc.

## Key Components

### API Endpoints

API endpoints are defined in `app/api/v1/endpoints/` and are organized by feature:

- `analyze.py`: Code analysis endpoints
- `fix.py`: Code fixing endpoints
- `explain.py`: Error explanation endpoints
- `github.py`: GitHub integration endpoints
- `users.py`: User management endpoints
- `api_keys.py`: API key management endpoints
- `health.py`: Health check endpoint

### Services

Services contain the business logic and are defined in `app/services/`:

- `analysis_service.py`: Code analysis logic
- `fix_service.py`: Code fixing logic
- `github_service.py`: GitHub integration logic
- `user_service.py`: User management logic
- `api_key_service.py`: API key management logic

### Models

Models are defined in `app/models/`:

- `db/`: SQLAlchemy database models
- `schemas/`: Pydantic schemas for request/response validation

### Utilities

Utilities are defined in `app/utils/`:

- `parsing/`: Code parsing utilities
- `sandbox/`: Code execution sandbox

## Getting Started with Development

To get started with development, see the [Development Setup](development-setup.md) guide. 