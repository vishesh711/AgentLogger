# Deployment Guide

This guide covers how to deploy the AgentLogger API in various environments, from development to production.

## Prerequisites

Before deploying AgentLogger, make sure you have:

- A server with at least 2GB RAM and 1 CPU core
- Docker and Docker Compose installed
- A domain name (for production deployments)
- SSL certificates (for production deployments)

## Development Deployment

For development purposes, you can use the included Docker Compose configuration:

```bash
# Clone the repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Create a .env file with your configuration
cp .env.sample .env
# Edit the .env file with your configuration

# Start the services
docker-compose up -d
```

This will start:
- The AgentLogger API on port 8000
- A PostgreSQL database
- A Redis instance (if enabled in .env)

## Production Deployment

For production deployments, we recommend using the production Docker Compose configuration, which includes:

- PostgreSQL database with proper persistence
- Redis for caching
- Nginx as a reverse proxy with SSL
- Proper resource limits and health checks

### Using Docker Compose (Recommended)

1. Clone the repository:

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
```

2. Create a .env file with your production configuration:

```bash
cp .env.sample .env.prod
# Edit the .env.prod file with your production configuration
```

3. Configure SSL certificates:

Place your SSL certificates in the `nginx/certs` directory:

```bash
mkdir -p nginx/certs
# Copy your SSL certificates to nginx/certs
cp /path/to/your/fullchain.pem nginx/certs/
cp /path/to/your/privkey.pem nginx/certs/
```

4. Update the Nginx configuration:

Edit `nginx/conf.d/default.conf` to match your domain name and SSL certificate paths.

5. Start the production services:

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

This will start:
- The AgentLogger API behind Nginx
- PostgreSQL database with volume persistence
- Redis for caching
- Nginx as a reverse proxy with SSL

### Using Kubernetes

For larger deployments, you can use Kubernetes:

1. Create Kubernetes manifests:

```bash
# Create namespace
kubectl create namespace agentlogger

# Create config map and secrets
kubectl create configmap agentlogger-config --from-env-file=.env.prod -n agentlogger
kubectl create secret generic agentlogger-secrets --from-literal=postgres-password=YOUR_PASSWORD --from-literal=groq-api-key=YOUR_GROQ_API_KEY -n agentlogger

# Apply manifests
kubectl apply -f kubernetes/
```

2. Verify the deployment:

```bash
kubectl get pods -n agentlogger
```

## Scaling

### Horizontal Scaling

You can scale the API horizontally by increasing the number of replicas:

```bash
# With Docker Compose
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# With Kubernetes
kubectl scale deployment agentlogger-api --replicas=3 -n agentlogger
```

### Vertical Scaling

You can also scale the API vertically by adjusting the resource limits in `docker-compose.prod.yml` or your Kubernetes manifests.

## Monitoring

### Health Checks

The API includes a health check endpoint at `/v1/health`. You can use this to monitor the health of the API:

```bash
curl https://your-domain.com/v1/health
```

### Sentry Integration

AgentLogger includes Sentry integration for error tracking. To enable it, set the following environment variables:

```
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production
```

### Custom Analytics

AgentLogger includes a custom analytics system. To enable it, set the following environment variables:

```
ENABLE_ANALYTICS=true
ANALYTICS_PROVIDER=segment|mixpanel|posthog
ANALYTICS_API_KEY=your-analytics-api-key
```

## Backup and Recovery

### Database Backup

To backup the PostgreSQL database:

```bash
# With Docker Compose
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres agentlogger > backup.sql

# With Kubernetes
kubectl exec -it $(kubectl get pods -l app=postgres -n agentlogger -o jsonpath="{.items[0].metadata.name}") -n agentlogger -- pg_dump -U postgres agentlogger > backup.sql
```

### Database Recovery

To restore the PostgreSQL database:

```bash
# With Docker Compose
cat backup.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres agentlogger

# With Kubernetes
cat backup.sql | kubectl exec -it $(kubectl get pods -l app=postgres -n agentlogger -o jsonpath="{.items[0].metadata.name}") -n agentlogger -- psql -U postgres agentlogger
```

## CI/CD Integration

AgentLogger includes GitHub Actions workflows for CI/CD:

- `.github/workflows/ci-cd.yml`: Runs tests, builds Docker images, and deploys to production
- `.github/workflows/cli-package.yml`: Builds and publishes the CLI package

To use these workflows, you need to set up the following secrets in your GitHub repository:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password
- `SSH_PRIVATE_KEY`: SSH private key for deploying to your server
- `SSH_HOST`: SSH host for deploying to your server
- `SSH_USER`: SSH user for deploying to your server
- `PYPI_API_TOKEN`: PyPI API token for publishing the CLI package

## Security Considerations

### API Keys

API keys are used for authentication. Make sure to keep them secure and rotate them regularly.

### SSL/TLS

Always use SSL/TLS in production. The included Nginx configuration includes SSL/TLS support.

### Rate Limiting

The API includes rate limiting to prevent abuse. You can configure the rate limits in the `.env` file:

```
RATE_LIMIT_PER_MINUTE=60
```

### Environment Variables

Never commit sensitive environment variables to your repository. Use `.env` files or secrets management systems.

## Troubleshooting

### API Not Starting

If the API is not starting, check the logs:

```bash
# With Docker Compose
docker-compose -f docker-compose.prod.yml logs api

# With Kubernetes
kubectl logs -l app=agentlogger-api -n agentlogger
```

### Database Connection Issues

If the API cannot connect to the database, check the database logs and make sure the database is running:

```bash
# With Docker Compose
docker-compose -f docker-compose.prod.yml logs db

# With Kubernetes
kubectl logs -l app=postgres -n agentlogger
```

### Nginx Issues

If Nginx is not working, check the Nginx logs:

```bash
# With Docker Compose
docker-compose -f docker-compose.prod.yml logs nginx

# With Kubernetes
kubectl logs -l app=nginx -n agentlogger
```

## Conclusion

This guide covered how to deploy AgentLogger in various environments, from development to production. For more information, see the [Configuration Guide](configuration.md) and the [API Documentation](../api/index.md).