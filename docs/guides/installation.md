# Installation Guide

This guide covers the installation of AgentLogger in different environments.

## Local Development Installation

### Prerequisites

- Python 3.11 or later
- PostgreSQL 13 or later
- Docker (optional, for sandbox execution)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
cp setup_groq_key.txt .env
```

Edit the `.env` file to include your specific configuration, especially:

- Database connection details
- Groq API key
- GitHub access token (if using GitHub integration)
- Secret key (generate a secure random string)

### Step 5: Initialize the Database

Make sure PostgreSQL is running, then run:

```bash
# Run database migrations
alembic upgrade head

# Initialize the database with initial data
python scripts/init_db.py
```

### Step 6: Start the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API should now be accessible at http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## Docker Installation

### Prerequisites

- Docker
- Docker Compose

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
cp setup_groq_key.txt .env
```

Edit the `.env` file to include your specific configuration. For Docker, the database host should be set to the service name:

```
POSTGRES_SERVER=db
```

### Step 3: Build and Start the Docker Containers

```bash
docker-compose up -d
```

This will start:
- The AgentLogger API service
- PostgreSQL database
- Redis (for caching)

### Step 4: Initialize the Database

```bash
docker-compose exec app python scripts/init_db.py
```

The API should now be accessible at http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## Production Deployment

For production deployment, we recommend:

1. Using a production-ready ASGI server like Uvicorn behind Nginx
2. Setting up proper SSL/TLS certificates
3. Configuring a production database with proper backups
4. Setting up monitoring and logging

See the [Deployment Guide](deployment.md) for detailed instructions on production deployment.

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Make sure PostgreSQL is running
2. Verify the database connection details in your `.env` file
3. Check that the database exists and the user has appropriate permissions

```bash
# Create database manually if needed
createdb agentlogger
```

### Python Package Issues

If you encounter issues with Python packages:

```bash
# Update pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Docker Issues

If you encounter issues with Docker:

```bash
# Stop and remove containers
docker-compose down

# Remove volumes to start fresh
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
``` 