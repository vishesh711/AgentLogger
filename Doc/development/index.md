# Development Guide

This section contains information for developers who want to contribute to the AgentLogger project or understand its internal architecture.

## Table of Contents

- [Project Structure](project-structure.md)
- [Development Setup](development-setup.md)
- [Agent Architecture](agent-architecture.md)
- [Agent Architecture Implementation](agent-architecture-implementation.md)
- [Frontend Documentation](frontend.md)
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
- **Sentry**: Error tracking and performance monitoring
- **Docker & Docker Compose**: Containerization and orchestration

The frontend is built with:

- **React**: A JavaScript library for building user interfaces
- **TypeScript**: Typed JavaScript for better developer experience
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Component library built on Radix UI

The application follows an agent-based architecture with a layered design:

1. **API Layer**: Handles HTTP requests and responses
2. **Agent Layer**: Specialized AI agents that work together to analyze code, identify issues, and generate fixes
3. **Service Layer**: Contains business logic
4. **Model Layer**: Defines data models and schemas
5. **Infrastructure Layer**: Handles database connections, external APIs, etc.

## Key Components

### API Endpoints

API endpoints are defined in `app/api/v1/endpoints/` and are organized by feature:

- `analyze.py`: Code analysis endpoints
- `fix.py`: Code fixing endpoints
- `explain.py`: Error explanation endpoints
- `patch.py`: Patch generation endpoints
- `github.py`: GitHub integration endpoints
- `users.py`: User management endpoints
- `api_keys.py`: API key management endpoints
- `health.py`: Health check endpoint
- `agent_debug.py`: Agent-based debugging endpoints

### Agents

Agents are defined in `app/agents/`:

- `base_agent.py`: Base agent class
- `coordinator_agent.py`: Orchestrates the debugging process
- `analyzer_agent.py`: Analyzes code for issues
- `fix_generator_agent.py`: Generates fixes for identified issues

### Services

Services contain the business logic and are defined in `app/services/`:

- `analysis_service.py`: Code analysis logic
- `fix_service.py`: Code fixing logic
- `github_service.py`: GitHub integration logic
- `user_service.py`: User management logic
- `api_key_service.py`: API key management logic
- `monitoring_service.py`: Analytics and monitoring logic
- `ai/groq_client.py`: Client for interacting with the Groq API

### Models

Models are defined in `app/models/`:

- `db/`: SQLAlchemy database models
- `schemas/`: Pydantic schemas for request/response validation

### Frontend

The frontend is organized in `frontend/src/`:

- `components/`: Reusable UI components
- `pages/`: Page components
- `lib/`: Utility functions and API client
- `hooks/`: Custom React hooks

### Utilities

Utilities are defined in `app/utils/`:

- `parsing/`: Code parsing utilities
- `sandbox/`: Code execution sandbox

### CLI Tool

The CLI tool is defined in `cli/`:

- `agent_logger_cli.py`: CLI implementation
- `setup.py`: CLI package setup

## Getting Started with Development

To get started with development, see the [Development Setup](development-setup.md) guide. 