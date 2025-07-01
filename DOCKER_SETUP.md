# AgentLogger Docker Setup Guide

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- `.env` file configured (copy from `env.example`)

### Development Setup

1. **Clone and configure**:
```bash
git clone <repository-url>
cd AgentLogger
cp env.example .env
# Edit .env with your configuration
```

2. **Start development environment**:
```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432
- Redis: localhost:6379

### Production Setup

1. **Configure environment**:
```bash
cp env.example .env.prod
# Edit .env.prod with production values
```

2. **Start production environment**:
```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## Environment Configuration

### Required Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=agentlogger

# Security
SECRET_KEY=your-super-secret-key-64-characters-minimum
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI/LLM
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192
```

### Optional Variables

```env
# OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Redis
USE_REDIS=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# Monitoring
SENTRY_DSN=your-sentry-dsn
ENABLE_ANALYTICS=false
```

## Docker Commands

### Development

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Production

```bash
# Start production stack
docker-compose -f docker-compose.prod.yml up -d

# Scale backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production stack
docker-compose -f docker-compose.prod.yml down
```

### Maintenance

```bash
# Database backup
docker-compose exec db /backup.sh

# Database shell
docker-compose exec db psql -U postgres -d agentlogger

# Backend shell
docker-compose exec backend bash

# Run migrations
docker-compose exec backend alembic upgrade head

# Initialize database
docker-compose exec backend python scripts/init_db.py
```

## Health Checks

All services include health checks:

```bash
# Check service health
docker-compose ps

# Individual service health
curl http://localhost:8000/api/v1/health
```

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check if DATABASE_URL is correct
   - Ensure database service is healthy: `docker-compose ps`
   - Check logs: `docker-compose logs db`

2. **Migration errors**:
   - Run manually: `docker-compose exec backend alembic upgrade head`
   - Check database permissions

3. **API key issues**:
   - Generate new API key: `docker-compose exec backend python scripts/generate_api_key.py`
   - Check X-API-Key header in requests

4. **Frontend not loading**:
   - Check VITE_API_URL in frontend environment
   - Verify nginx proxy configuration

### Performance Optimization

1. **Resource limits** (production):
```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
```

2. **Database optimization**:
   - Increase shared_buffers
   - Configure connection pooling
   - Regular VACUUM and ANALYZE

3. **Redis caching**:
   - Enable Redis for session storage
   - Cache API responses
   - Rate limiting with Redis

## Security Considerations

### Production Security

1. **Environment variables**:
   - Use strong, unique SECRET_KEY
   - Secure database passwords
   - Never commit .env files

2. **Network security**:
   - Use internal Docker networks
   - Limit exposed ports
   - Configure firewall rules

3. **SSL/TLS**:
   - Configure SSL certificates
   - Use HTTPS redirects
   - Set security headers

4. **Rate limiting**:
   - API rate limits configured
   - Authentication rate limits
   - DDoS protection

## Monitoring

### Logs

```bash
# Application logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f db

# All logs
docker-compose logs -f
```

### Metrics

- Health check endpoints
- Database connection monitoring
- Resource usage tracking
- Error rate monitoring

## Backup and Recovery

### Automated Backups

1. **Database backups**:
   - Automated daily backups
   - 7-day retention policy
   - Compressed storage

2. **Volume backups**:
```bash
# Backup volumes
docker run --rm -v agentlogger_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### Recovery

```bash
# Restore database
docker-compose exec db psql -U postgres -d agentlogger < backup.sql

# Restore volumes
docker run --rm -v agentlogger_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
``` 