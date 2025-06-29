# Deployment Guide

This guide covers the deployment of AgentLogger in production environments.

## Deployment Options

AgentLogger can be deployed in several ways:

1. **Docker Deployment**: Using Docker and Docker Compose
2. **Traditional Deployment**: Using a WSGI/ASGI server behind a reverse proxy
3. **Cloud Deployment**: Using cloud services like AWS, GCP, or Azure

## Docker Deployment

### Prerequisites

- Docker and Docker Compose installed on the host machine
- Domain name (optional, but recommended)
- SSL certificate (optional, but recommended)

### Step 1: Prepare Environment Variables

Create a `.env` file with production settings:

```
# Project settings
PROJECT_NAME=AgentLogger API
PROJECT_DESCRIPTION=AI-powered debugging API service
VERSION=0.1.0

# API settings
API_V1_STR=/api/v1

# CORS settings
CORS_ORIGINS=https://your-frontend-domain.com

# Database settings
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=agentlogger

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
USE_REDIS=true

# Security settings
SECRET_KEY=your-very-secure-secret-key

# LLM settings
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192

# GitHub integration
GITHUB_ACCESS_TOKEN=your-github-token

# Sandbox execution
USE_DOCKER_SANDBOX=true
EXECUTION_TIMEOUT=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=30
```

### Step 2: Configure Docker Compose for Production

Create a `docker-compose.prod.yml` file:

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: agentlogger-api
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./app:/app/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    networks:
      - agentlogger-network
    restart: always

  db:
    image: postgres:15
    container_name: agentlogger-db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    networks:
      - agentlogger-network
    restart: always

  redis:
    image: redis:7
    container_name: agentlogger-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - agentlogger-network
    restart: always

  nginx:
    image: nginx:latest
    container_name: agentlogger-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - ./nginx/www:/var/www/html
    depends_on:
      - app
    networks:
      - agentlogger-network
    restart: always

networks:
  agentlogger-network:

volumes:
  postgres_data:
  redis_data:
```

### Step 3: Configure Nginx

Create an Nginx configuration file at `nginx/conf.d/default.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
    # Proxy API requests to the FastAPI application
    location /api {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Proxy documentation requests to the FastAPI application
    location /docs {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /redoc {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /openapi.json {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Serve static files
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

### Step 4: Deploy the Application

```bash
# Build and start the containers
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec app alembic upgrade head

# Initialize the database (if needed)
docker-compose -f docker-compose.prod.yml exec app python scripts/init_db.py
```

### Step 5: Generate an API Key

```bash
docker-compose -f docker-compose.prod.yml exec app python scripts/generate_api_key.py
```

## Traditional Deployment

### Prerequisites

- Python 3.11 or later
- PostgreSQL 13 or later
- Redis (optional, for caching)
- Nginx or another reverse proxy
- Systemd or another process manager

### Step 1: Set Up the Server

Install required packages:

```bash
# Update package lists
sudo apt update

# Install Python, PostgreSQL, and other dependencies
sudo apt install -y python3.11 python3.11-venv python3.11-dev postgresql postgresql-contrib nginx redis-server
```

### Step 2: Create a User for the Application

```bash
sudo useradd -m -s /bin/bash agentlogger
sudo su - agentlogger
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

### Step 4: Set Up a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Configure Environment Variables

Create a `.env` file with production settings (similar to the Docker example above).

### Step 6: Set Up the Database

```bash
# Create a database user
sudo -u postgres createuser agentlogger

# Create a database
sudo -u postgres createdb -O agentlogger agentlogger

# Set a password for the user
sudo -u postgres psql -c "ALTER USER agentlogger WITH PASSWORD 'your-secure-password';"

# Run migrations
alembic upgrade head

# Initialize the database
python scripts/init_db.py
```

### Step 7: Create a Systemd Service

Create a file at `/etc/systemd/system/agentlogger.service`:

```ini
[Unit]
Description=AgentLogger API
After=network.target

[Service]
User=agentlogger
Group=agentlogger
WorkingDirectory=/home/agentlogger/agentlogger
Environment="PATH=/home/agentlogger/agentlogger/venv/bin"
EnvironmentFile=/home/agentlogger/agentlogger/.env
ExecStart=/home/agentlogger/agentlogger/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 8: Configure Nginx

Create a file at `/etc/nginx/sites-available/agentlogger`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-domain.com.pem;
    ssl_certificate_key /etc/ssl/private/your-domain.com.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
    # Proxy API requests to the FastAPI application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/agentlogger /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Start the Service

```bash
sudo systemctl enable agentlogger
sudo systemctl start agentlogger
```

### Step 10: Generate an API Key

```bash
sudo su - agentlogger
cd agentlogger
source venv/bin/activate
python scripts/generate_api_key.py
```

## Cloud Deployment

### AWS Deployment with Elastic Beanstalk

#### Step 1: Prepare the Application

Create a `Procfile` in the project root:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Create a `.ebextensions` directory with configuration files:

```
# .ebextensions/01_packages.config
packages:
  yum:
    git: []
    postgresql-devel: []
```

```
# .ebextensions/02_python.config
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current"
  aws:elasticbeanstalk:container:python:
    WSGIPath: app.main:app
```

#### Step 2: Deploy to Elastic Beanstalk

```bash
# Install the EB CLI
pip install awsebcli

# Initialize EB
eb init

# Create an environment
eb create agentlogger-production

# Set environment variables
eb setenv \
  PROJECT_NAME="AgentLogger API" \
  PROJECT_DESCRIPTION="AI-powered debugging API service" \
  VERSION="0.1.0" \
  API_V1_STR="/api/v1" \
  CORS_ORIGINS="https://your-frontend-domain.com" \
  POSTGRES_SERVER="your-rds-endpoint.amazonaws.com" \
  POSTGRES_USER="postgres" \
  POSTGRES_PASSWORD="your-secure-password" \
  POSTGRES_DB="agentlogger" \
  REDIS_HOST="your-elasticache-endpoint.amazonaws.com" \
  REDIS_PORT="6379" \
  REDIS_PASSWORD="your-redis-password" \
  USE_REDIS="true" \
  SECRET_KEY="your-very-secure-secret-key" \
  GROQ_API_KEY="your-groq-api-key" \
  GROQ_MODEL="llama3-70b-8192" \
  GITHUB_ACCESS_TOKEN="your-github-token" \
  USE_DOCKER_SANDBOX="true" \
  EXECUTION_TIMEOUT="30" \
  RATE_LIMIT_PER_MINUTE="30"

# Deploy the application
eb deploy
```

#### Step 3: Run Migrations

```bash
eb ssh

# Inside the EC2 instance
cd /var/app/current
source /var/app/venv/staging-LQM1lest/bin/activate
alembic upgrade head
python scripts/init_db.py
python scripts/generate_api_key.py
```

## Monitoring and Logging

### Setting Up Monitoring

For production deployments, it's important to set up monitoring:

1. **Sentry**: For error tracking and performance monitoring
2. **Prometheus and Grafana**: For metrics and dashboards
3. **ELK Stack**: For centralized logging

#### Sentry Integration

Add Sentry to your application in `app/main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment="production",
)
```

### Backup Strategy

Set up regular backups for your database:

```bash
# Create a backup script
cat > /home/agentlogger/backup.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_DIR="/home/agentlogger/backups"
mkdir -p $BACKUP_DIR
pg_dump -U agentlogger -d agentlogger -f "$BACKUP_DIR/agentlogger_$TIMESTAMP.sql"
find $BACKUP_DIR -type f -mtime +7 -delete
EOF

# Make it executable
chmod +x /home/agentlogger/backup.sh

# Add it to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /home/agentlogger/backup.sh") | crontab -
```

## Security Considerations

1. **API Key Management**: Rotate API keys regularly
2. **Database Security**: Use strong passwords and restrict access
3. **Network Security**: Use a firewall to restrict access to the server
4. **SSL/TLS**: Use HTTPS for all connections
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **Input Validation**: Validate all user input to prevent injection attacks
7. **Dependency Management**: Keep dependencies up to date to prevent vulnerabilities

## Scaling Considerations

As your application grows, you may need to scale:

1. **Horizontal Scaling**: Add more application instances behind a load balancer
2. **Database Scaling**: Use database replication and sharding
3. **Caching**: Use Redis for caching frequently accessed data
4. **Asynchronous Processing**: Use a task queue like Celery for long-running tasks

## Maintenance

Regular maintenance tasks include:

1. **Updating Dependencies**: Regularly update dependencies to get security fixes
2. **Database Maintenance**: Regularly vacuum and analyze the database
3. **Log Rotation**: Set up log rotation to prevent disk space issues
4. **Monitoring**: Regularly check monitoring dashboards for issues
5. **Backups**: Regularly test backup restoration