# Configuration Guide

This guide covers how to configure the AgentLogger API for different environments and use cases.

## Environment Variables

AgentLogger uses environment variables for configuration. You can set these variables in a `.env` file or directly in your environment.

### Basic Configuration

```
# Project settings
PROJECT_NAME=AgentLogger API
PROJECT_DESCRIPTION=AI-powered debugging API service
VERSION=0.1.0

# API settings
API_V1_STR=/v1

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Database settings
DATABASE_URL=sqlite:///./app.db
```

### AI Configuration

> **Important**: A valid `GROQ_API_KEY` is required for all AI-powered features. You can provide it in **one** of the following ways:
>
> 1. Add `GROQ_API_KEY=<your-key>` to a `.env` or `.env.prod` file (recommended for production)
> 2. Export it in your shell before running Docker Compose: `export GROQ_API_KEY=<your-key>`
> 3. Hard-code it in `docker-compose.yml` under the `backend` service's `environment` section (useful for local testing)

```
# Groq API settings
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192
```

### Security Configuration

```
# Security settings
SECRET_KEY=your-secret-key
API_KEY_LENGTH=32
```

### GitHub Integration

```
# GitHub integration
GITHUB_TOKEN=your-github-token
```

### Sandbox Execution

```
# Sandbox execution
USE_SANDBOX=true
EXECUTION_TIMEOUT=30
```

### Rate Limiting

```
# Rate limiting
RATE_LIMIT_PER_MINUTE=60
```

### Monitoring and Analytics

```
# Sentry integration
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=development

# Analytics
ENABLE_ANALYTICS=true
ANALYTICS_PROVIDER=segment
ANALYTICS_API_KEY=your-analytics-api-key
```

## Configuration Files

### .env File

The `.env` file is the primary configuration file for AgentLogger. It should be placed in the root directory of the project.

Example `.env` file:

```
# Project settings
PROJECT_NAME=AgentLogger API
PROJECT_DESCRIPTION=AI-powered debugging API service
VERSION=0.1.0

# API settings
API_V1_STR=/v1

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Database settings
DATABASE_URL=sqlite:///./app.db

# Groq API settings
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192

# Security settings
SECRET_KEY=your-secret-key
API_KEY_LENGTH=32

# GitHub integration
GITHUB_TOKEN=your-github-token

# Sandbox execution
USE_SANDBOX=true
EXECUTION_TIMEOUT=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=60

# Sentry integration
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=development

# Analytics
ENABLE_ANALYTICS=true
ANALYTICS_PROVIDER=segment
ANALYTICS_API_KEY=your-analytics-api-key
```

### .env.sample

The `.env.sample` file is a template for the `.env` file. It contains all the required environment variables with placeholder values.

### .env.prod

For production environments, you can create a `.env.prod` file with production-specific settings:

```
# Project settings
PROJECT_NAME=AgentLogger API
PROJECT_DESCRIPTION=AI-powered debugging API service
VERSION=0.1.0

# API settings
API_V1_STR=/v1

# CORS settings
CORS_ORIGINS=https://your-domain.com

# Database settings
DATABASE_URL=postgresql://postgres:password@db:5432/agentlogger

# Groq API settings
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192

# Security settings
SECRET_KEY=your-production-secret-key
API_KEY_LENGTH=32

# GitHub integration
GITHUB_TOKEN=your-github-token

# Sandbox execution
USE_SANDBOX=true
EXECUTION_TIMEOUT=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=60

# Sentry integration
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production

# Analytics
ENABLE_ANALYTICS=true
ANALYTICS_PROVIDER=segment
ANALYTICS_API_KEY=your-analytics-api-key
```

## Configuration in Code

The configuration is loaded in `app/core/config.py` using Pydantic's `BaseSettings` class:

```python
from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator
from typing import List, Optional, Union
import os

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "AgentLogger API"
    PROJECT_DESCRIPTION: str = "AI-powered debugging API service"
    VERSION: str = "0.1.0"
    
    # API settings
    API_V1_STR: str = "/v1"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Groq API settings
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"
    
    # Security settings
    SECRET_KEY: str = "development-secret-key"
    API_KEY_LENGTH: int = 32
    
    # GitHub integration
    GITHUB_TOKEN: Optional[str] = None
    
    # Sandbox execution
    USE_SANDBOX: bool = True
    EXECUTION_TIMEOUT: int = 30
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Sentry integration
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "development"
    
    # Analytics
    ENABLE_ANALYTICS: bool = False
    ANALYTICS_PROVIDER: Optional[str] = None
    ANALYTICS_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Configuration Precedence

The configuration is loaded in the following order of precedence:

1. Environment variables
2. `.env` file
3. Default values in the `Settings` class

## Configuration for Different Environments

### Development

For development, you can use the default `.env` file with development-specific settings.

### Testing

For testing, you can create a `.env.test` file with test-specific settings:

```
# Database settings
DATABASE_URL=sqlite:///./test.db

# Disable sandbox execution
USE_SANDBOX=false

# Disable rate limiting
RATE_LIMIT_PER_MINUTE=0

# Disable Sentry
SENTRY_DSN=

# Disable analytics
ENABLE_ANALYTICS=false
```

### Production

For production, you can create a `.env.prod` file with production-specific settings, as shown above.

## CLI Configuration

The AgentLogger CLI uses a separate configuration file at `~/.agentlogger/config.json`:

```json
{
  "api_key": "your-api-key",
  "api_url": "http://localhost:8000/v1",
  "output_format": "text"
}
```

You can configure the CLI using the `agent-logger configure` command:

```bash
agent-logger configure --api-key YOUR_API_KEY --api-url https://api.yourdomain.com
```

## Docker Configuration

When using Docker, you can pass environment variables to the containers using the `--env-file` option:

```bash
docker-compose --env-file .env.prod up -d
```

## Kubernetes Configuration

When using Kubernetes, you can create a ConfigMap and Secret from your `.env.prod` file:

```bash
kubectl create configmap agentlogger-config --from-env-file=.env.prod -n agentlogger
kubectl create secret generic agentlogger-secrets --from-literal=postgres-password=YOUR_PASSWORD --from-literal=groq-api-key=YOUR_GROQ_API_KEY -n agentlogger
```

## Conclusion

This guide covered how to configure AgentLogger for different environments and use cases. For more information, see the [Deployment Guide](deployment.md) and the [API Documentation](../api/index.md). 