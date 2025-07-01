# Configuration Guide

This guide covers how to configure AgentLogger for different environments and use cases. AgentLogger is designed to work out-of-the-box with minimal configuration while providing extensive customization options.

## Environment Variables

AgentLogger uses environment variables for configuration. These can be set in several ways:

1. **Docker Compose** (recommended): Edit `docker-compose.yml`
2. **Environment file**: Create a `.env` file in the project root
3. **Shell export**: Export variables before running the application

### 🔑 Required Configuration

#### Groq API Key (Required)
**You must provide a Groq API key for AI functionality:**

```bash
# Option 1: Export in shell (recommended for development)
export GROQ_API_KEY="gsk_your_groq_api_key_here"

# Option 2: Set in docker-compose.yml
# Edit the GROQ_API_KEY line in docker-compose.yml

# Option 3: Create .env file
echo "GROQ_API_KEY=gsk_your_groq_api_key_here" > .env
```

Get your free Groq API key at [console.groq.com](https://console.groq.com).

### 🏗️ Core Application Settings

```bash
# Project Information
PROJECT_NAME="AgentLogger"
PROJECT_DESCRIPTION="AI-powered debugging service"
VERSION="0.1.0"

# API Configuration
API_V1_STR="/api/v1"

# Server Configuration
HOST="127.0.0.1"
PORT=8000
RELOAD=true
```

### 🌐 CORS Configuration

```bash
# Frontend Origins (automatically configured)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8080","http://localhost:8081","http://localhost:8082","http://127.0.0.1:5173","http://127.0.0.1:8080","http://127.0.0.1:8081","http://127.0.0.1:8082"]
```

The application automatically includes common development ports. For production, update this list.

### 🗄️ Database Configuration

```bash
# Development (SQLite - default)
DATABASE_URL="sqlite:///./agentlogger.db"

# Production (PostgreSQL - recommended)
DATABASE_URL="postgresql://postgres:postgres@db:5432/agentlogger"

# Custom PostgreSQL
DATABASE_URL="postgresql://username:password@host:port/database"
```

### 🤖 AI Configuration

```bash
# Groq API Settings
GROQ_API_KEY="gsk_your_api_key_here"          # Required
GROQ_MODEL="llama3-70b-8192"                   # Default model
GROQ_TEMPERATURE=0.1                           # Response randomness (0-1)
GROQ_MAX_TOKENS=4096                           # Maximum response length
```

### 🔐 Security Configuration

```bash
# API Key Settings
API_KEY_LENGTH=32                               # Generated key length
DEFAULT_API_KEY="QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU"  # For testing

# Security
SECRET_KEY="your-secret-key-here"               # For JWT tokens (if used)
```

### 🚦 Rate Limiting

```bash
# Rate Limiting
RATE_LIMIT_PER_MINUTE=60                        # Requests per minute per IP/API key
ENABLE_RATE_LIMITING=true                       # Enable/disable rate limiting
```

### 📊 Monitoring Configuration

```bash
# Sentry Error Tracking (optional)
SENTRY_DSN="your-sentry-dsn"                   # Sentry project DSN
SENTRY_ENVIRONMENT="development"                # Environment name
SENTRY_TRACES_SAMPLE_RATE=1.0                  # Performance monitoring rate

# Logging
LOG_LEVEL="INFO"                                # DEBUG, INFO, WARNING, ERROR
```

## Configuration Files

### docker-compose.yml
The main configuration file for Docker deployment:

```yaml
services:
  backend:
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/agentlogger
      - CORS_ORIGINS=["http://localhost:8082","http://localhost:3000"]
      - API_V1_STR=/api/v1
```

### .env File (Optional)
Create a `.env` file in the project root:

```bash
# Essential Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
DATABASE_URL=sqlite:///./agentlogger.db

# Optional Configuration
GROQ_MODEL=llama3-70b-8192
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
```

### app/core/config.py
The configuration is loaded using Pydantic Settings:

```python
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "AgentLogger"
    PROJECT_DESCRIPTION: str = "AI-powered debugging service"
    VERSION: str = "0.1.0"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./agentlogger.db"
    
    # Groq API
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8082",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8082"
    ]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True
```

## Environment-Specific Configuration

### Development Environment

```bash
# Development settings
DEBUG=true
RELOAD=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./agentlogger.db
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8082"]
```

### Production Environment

```bash
# Production settings
DEBUG=false
RELOAD=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@db:5432/agentlogger
CORS_ORIGINS=["https://yourdomain.com"]
SENTRY_DSN=your-production-sentry-dsn
SENTRY_ENVIRONMENT=production
```

### Testing Environment

```bash
# Testing settings
DATABASE_URL=sqlite:///./test.db
GROQ_API_KEY=test-key
RATE_LIMIT_PER_MINUTE=1000
LOG_LEVEL=WARNING
```

## Configuration Validation

AgentLogger validates configuration on startup:

### Required Variables
- `GROQ_API_KEY`: Must be a valid Groq API key

### Optional Variables with Defaults
- `GROQ_MODEL`: Defaults to `llama3-70b-8192`
- `DATABASE_URL`: Defaults to SQLite
- `RATE_LIMIT_PER_MINUTE`: Defaults to 60
- `LOG_LEVEL`: Defaults to INFO

### Configuration Errors
Common configuration issues:

```bash
# Missing Groq API Key
ValidationError: GROQ_API_KEY is required

# Invalid Database URL
ValidationError: DATABASE_URL must be a valid database URL

# Invalid CORS Origins
ValidationError: CORS_ORIGINS must be a list of valid URLs
```

## Configuration Best Practices

### 1. Environment Variables
```bash
# ✅ Good: Use environment variables for secrets
export GROQ_API_KEY="gsk_..."

# ❌ Bad: Hard-code secrets in files
GROQ_API_KEY=gsk_abc123...
```

### 2. Production Security
```bash
# ✅ Good: Strong secret keys
SECRET_KEY="$(openssl rand -hex 32)"

# ❌ Bad: Weak or default keys
SECRET_KEY="secret"
```

### 3. Database Configuration
```bash
# ✅ Good: Use PostgreSQL in production
DATABASE_URL=postgresql://user:pass@db:5432/agentlogger

# ❌ Bad: Use SQLite in production (single-user only)
DATABASE_URL=sqlite:///./agentlogger.db
```

### 4. CORS Configuration
```bash
# ✅ Good: Specific origins in production
CORS_ORIGINS=["https://app.yourdomain.com"]

# ❌ Bad: Wildcard in production
CORS_ORIGINS=["*"]
```

## Troubleshooting Configuration

### Check Current Configuration
```bash
# View environment variables
docker-compose exec backend env | grep -E "(GROQ|DATABASE|CORS)"

# Check configuration loading
docker-compose logs backend | grep -i config
```

### Common Issues

#### 1. Groq API Key Issues
```bash
# Check if key is set
echo $GROQ_API_KEY

# Validate key format (should start with gsk_)
if [[ $GROQ_API_KEY == gsk_* ]]; then echo "Valid format"; fi
```

#### 2. Database Connection Issues
```bash
# Test PostgreSQL connection
docker-compose exec db psql -U postgres -d agentlogger -c "SELECT 1;"

# Check SQLite file permissions
ls -la agentlogger.db
```

#### 3. CORS Issues
```bash
# Test CORS from browser console
fetch('http://localhost:8000/api/v1/health/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

## Advanced Configuration

### Custom AI Models
```bash
# Use different Groq models
GROQ_MODEL="llama3-8b-8192"      # Faster, less capable
GROQ_MODEL="mixtral-8x7b-32768"  # Balanced
GROQ_MODEL="llama3-70b-8192"     # Slower, more capable
```

### Performance Tuning
```bash
# Database connection pooling
DATABASE_MAX_CONNECTIONS=20
DATABASE_POOL_SIZE=5

# Rate limiting
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_BURST=10

# Request timeouts
REQUEST_TIMEOUT=30
AI_REQUEST_TIMEOUT=60
```

### Monitoring Configuration
```bash
# Health check endpoints
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_PATH="/health"

# Metrics collection
METRICS_ENABLED=true
METRICS_PATH="/metrics"

# Request logging
LOG_REQUESTS=true
LOG_RESPONSES=false
```

## Next Steps

- **[Getting Started](getting-started.md)**: Basic setup guide
- **[Development Setup](../development/development-setup.md)**: Local development configuration
- **[Deployment Guide](deployment.md)**: Production deployment
- **[API Documentation](../api/index.md)**: API endpoint reference 