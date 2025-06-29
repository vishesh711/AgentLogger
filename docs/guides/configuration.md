# Configuration Guide

This guide explains how to configure AgentLogger for different environments and use cases.

## Environment Variables

AgentLogger uses environment variables for configuration. These can be set in a `.env` file in the project root or directly in your environment.

### Core Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PROJECT_NAME` | Name of the project | AgentLogger API | No |
| `PROJECT_DESCRIPTION` | Description of the project | AI-powered debugging API service | No |
| `VERSION` | API version | 0.1.0 | No |
| `API_V1_STR` | API v1 prefix | /api/v1 | No |
| `SECRET_KEY` | Secret key for JWT tokens | None | Yes |

### Database Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_SERVER` | PostgreSQL server hostname | localhost | Yes |
| `POSTGRES_USER` | PostgreSQL username | postgres | Yes |
| `POSTGRES_PASSWORD` | PostgreSQL password | postgres | Yes |
| `POSTGRES_DB` | PostgreSQL database name | agentlogger | Yes |

### Redis Settings (Optional)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `USE_REDIS` | Whether to use Redis for caching | false | No |
| `REDIS_HOST` | Redis server hostname | localhost | If `USE_REDIS=true` |
| `REDIS_PORT` | Redis server port | 6379 | If `USE_REDIS=true` |
| `REDIS_PASSWORD` | Redis password | None | No |

### AI Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Groq API key | None | Yes |
| `GROQ_MODEL` | Groq model to use | llama3-70b-8192 | Yes |

### GitHub Integration Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GITHUB_ACCESS_TOKEN` | GitHub personal access token | None | For GitHub integration |

### Sandbox Execution Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `USE_DOCKER_SANDBOX` | Whether to use Docker for code execution | true | No |
| `EXECUTION_TIMEOUT` | Timeout for code execution in seconds | 30 | No |

### Rate Limiting

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `RATE_LIMIT_PER_MINUTE` | API rate limit per minute | 60 | No |

### CORS Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CORS_ORIGINS` | Comma-separated list of allowed origins | http://localhost:3000,http://localhost:8000 | No |

## Example Configuration

Here's a complete example of a `.env` file:

```
# Project settings
PROJECT_NAME=AgentLogger API
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
POSTGRES_DB=agentlogger

# Redis settings (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
USE_REDIS=false

# Security settings
SECRET_KEY=your-secret-key-here

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

## Configuration File Locations

The configuration is loaded from the following locations, in order of precedence:

1. Environment variables
2. `.env` file in the project root
3. Default values in `app/core/config.py`

## Advanced Configuration

### Database Connection Pool

You can configure the database connection pool by modifying `app/core/db.py`. By default, the connection pool is configured with:

- Maximum size: 20 connections
- Overflow: 10 connections
- Timeout: 30 seconds

### Middleware Configuration

The middleware stack is configured in `app/main.py`. You can modify this file to:

- Add or remove middleware
- Change middleware order
- Configure middleware options

### API Key Authentication

API key authentication is enabled by default. You can configure it in `app/core/middleware.py`. Options include:

- Changing the header name (default: `X-API-Key`)
- Excluding paths from authentication
- Changing the authentication scheme

### Logging Configuration

Logging is configured in `app/main.py`. You can modify the logging configuration to:

- Change log levels
- Add log handlers
- Configure log formatting

## Environment-Specific Configuration

### Development

For development, we recommend:

```
USE_REDIS=false
USE_DOCKER_SANDBOX=true
```

### Testing

For testing, we recommend:

```
POSTGRES_DB=agentlogger_test
USE_REDIS=false
USE_DOCKER_SANDBOX=false
```

### Production

For production, we recommend:

```
USE_REDIS=true
USE_DOCKER_SANDBOX=true
RATE_LIMIT_PER_MINUTE=30
```

Make sure to set a strong `SECRET_KEY` in production. 