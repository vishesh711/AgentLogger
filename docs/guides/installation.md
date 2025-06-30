# Installation Guide

This guide covers how to install AgentLogger for development and production use.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (recommended)
- Git

## Installation Options

There are several ways to install and run AgentLogger:

1. Using Docker (recommended)
2. Manual installation
3. CLI installation

## Using Docker

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

2. Create a `.env` file:

```bash
cp .env.sample .env
# Edit .env with your configuration
```

3. Start the services:

```bash
docker-compose up -d
```

4. Generate an API key:

```bash
docker-compose exec api python scripts/generate_api_key.py
```

The API will be available at http://localhost:8000.

### Production Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

2. Create a production `.env` file:

```bash
cp .env.sample .env.prod
# Edit .env.prod with your production configuration
```

3. Configure SSL certificates:

```bash
mkdir -p nginx/certs
# Copy your SSL certificates to nginx/certs
cp /path/to/your/fullchain.pem nginx/certs/
cp /path/to/your/privkey.pem nginx/certs/
```

4. Start the production services:

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

5. Generate an API key:

```bash
docker-compose -f docker-compose.prod.yml exec api python scripts/generate_api_key.py
```

The API will be available at https://your-domain.com.

## Manual Installation

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.sample .env
# Edit .env with your configuration
```

5. Run database migrations:

```bash
alembic upgrade head
```

6. Generate an API key:

```bash
python scripts/generate_api_key.py
```

7. Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## CLI Installation

The AgentLogger CLI provides a command-line interface for interacting with the AgentLogger API.

### Using pip

```bash
pip install agent-logger-cli
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Install the CLI
pip install -e cli/
```

### CLI Configuration

After installing the CLI, you need to configure it with your API key:

```bash
agent-logger configure --api-key YOUR_API_KEY
```

By default, the CLI will connect to the AgentLogger API at `http://localhost:8000/v1`. If you want to use a different API endpoint, you can specify it during configuration:

```bash
agent-logger configure --api-key YOUR_API_KEY --api-url https://api.yourdomain.com/v1
```

## Verifying the Installation

### API Verification

To verify that the API is running correctly, you can use the health check endpoint:

```bash
curl http://localhost:8000/v1/health
```

You should see a response like:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### CLI Verification

To verify that the CLI is installed correctly, you can use the version command:

```bash
agent-logger version
```

You should see a response like:

```
AgentLogger CLI v0.1.0
```

## Next Steps

After installing AgentLogger, you can:

- [Configure AgentLogger](configuration.md) for your specific needs
- [Get started with the API](../api/index.md)
- [Use the CLI](cli.md) to interact with the API
- [Deploy AgentLogger](deployment.md) to production

## Troubleshooting

### Docker Issues

If you're having trouble with Docker:

```bash
# Check the logs
docker-compose logs

# Rebuild the containers
docker-compose build --no-cache
```

### Database Issues

If you're having trouble with the database:

```bash
# Check the database connection
docker-compose exec db psql -U postgres -d agentlogger -c "SELECT 1"

# Run migrations manually
docker-compose exec api alembic upgrade head
```

### API Key Issues

If you're having trouble with API keys:

```bash
# Generate a new API key
docker-compose exec api python scripts/generate_api_key.py
```

### CLI Issues

If you're having trouble with the CLI:

```bash
# Check the CLI configuration
cat ~/.agentlogger/config.json

# Reset the CLI configuration
agent-logger configure --reset
``` 