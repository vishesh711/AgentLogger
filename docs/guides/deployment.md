# AgentLogger Deployment Guide

This guide covers deploying AgentLogger in various environments, from development to production, using different methods and platforms.

## 🚀 Deployment Methods Overview

| Method | Best For | Difficulty | Scalability | Cost |
|--------|----------|------------|-------------|------|
| **Docker Compose** | Quick setup, small teams | ⭐ Easy | ⭐⭐ Medium | 💰 Low |
| **VPS/Server** | Full control, custom setup | ⭐⭐ Medium | ⭐⭐⭐ High | 💰💰 Medium |
| **Cloud Platform** | Scalability, managed services | ⭐⭐⭐ Advanced | ⭐⭐⭐⭐ Very High | 💰💰💰 Variable |
| **Kubernetes** | Enterprise, high availability | ⭐⭐⭐⭐ Expert | ⭐⭐⭐⭐⭐ Maximum | 💰💰💰💰 High |

## 🐳 Method 1: Docker Compose Deployment

### Development Deployment

**Perfect for**: Local development, testing, small teams

```bash
# Clone and setup
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Configure environment
cp env.example .env
# Edit .env file with your settings:
# GROQ_API_KEY=your_actual_groq_key
# SECRET_KEY=your_secret_key

# Start all services
docker-compose up -d

# Verify deployment
docker-compose ps
curl http://localhost/api/v1/health/
```

**Services:**
- ✅ Frontend (React) - http://localhost:8082
- ✅ Backend (FastAPI) - http://localhost:8000
- ✅ Database (SQLite/PostgreSQL)
- ✅ Nginx Proxy - http://localhost

### Production Docker Deployment

**Perfect for**: Production servers, staging environments

```bash
# Production configuration
cp env.example .env.prod

# Edit .env.prod with production values
cat > .env.prod << EOF
# Production Environment
NODE_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/agentlogger
GROQ_API_KEY=your_production_groq_key
SECRET_KEY=your_long_random_secret_key
CORS_ORIGINS=["https://yourdomain.com"]
RATE_LIMIT_PER_MINUTE=100
EOF

# Deploy production stack
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Setup SSL (if using custom domain)
# Copy SSL certificates to nginx/certs/
mkdir -p nginx/certs
cp /path/to/your/fullchain.pem nginx/certs/
cp /path/to/your/privkey.pem nginx/certs/

# Restart with SSL
docker-compose -f docker-compose.prod.yml restart nginx
```

**Production Features:**
- ✅ Optimized Docker images
- ✅ PostgreSQL database
- ✅ SSL/HTTPS support
- ✅ Production nginx config
- ✅ Health checks
- ✅ Auto-restart policies
- ✅ Resource limits

## 🖥️ Method 2: VPS/Server Deployment

### Traditional Server Setup

**Perfect for**: Full control, custom configurations, on-premise

#### Option A: Using Docker on VPS

```bash
# On your server (Ubuntu/Debian example)
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 2. Clone and deploy
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# 3. Configure for production
cp env.example .env
# Edit .env with your production settings

# 4. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 5. Setup reverse proxy (nginx)
sudo apt install nginx
sudo cp nginx/prod/default.conf /etc/nginx/sites-available/agentlogger
sudo ln -s /etc/nginx/sites-available/agentlogger /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Option B: Manual Installation on VPS

```bash
# Backend setup
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm postgresql

# Clone repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database setup
sudo -u postgres createdb agentlogger
python scripts/init_db.py

# Frontend
cd frontend
npm install
npm run build

# Setup systemd services
sudo cp scripts/agentlogger-backend.service /etc/systemd/system/
sudo cp scripts/agentlogger-frontend.service /etc/systemd/system/
sudo systemctl enable agentlogger-backend agentlogger-frontend
sudo systemctl start agentlogger-backend agentlogger-frontend
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/agentlogger
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# SSL configuration (add after getting SSL certificates)
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/privkey.pem;
    
    # Include locations from above
}
```

## ☁️ Method 3: Cloud Platform Deployment

### AWS Deployment

#### Option A: AWS ECS (Container Service)

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build images
docker build -t agentlogger-backend .
docker build -t agentlogger-frontend ./frontend

# Tag and push
docker tag agentlogger-backend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/agentlogger-backend:latest
docker tag agentlogger-frontend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/agentlogger-frontend:latest

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/agentlogger-backend:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/agentlogger-frontend:latest

# 2. Create ECS task definition and service
# Use AWS Console or Infrastructure as Code (Terraform/CloudFormation)
```

#### Option B: AWS Lambda + API Gateway (Serverless)

```bash
# Install Serverless Framework
npm install -g serverless

# Deploy serverless backend
cd backend
npm install
serverless deploy

# Deploy frontend to S3 + CloudFront
cd ../frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name
```

### Google Cloud Platform

#### Cloud Run Deployment

```bash
# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/agentlogger-backend
gcloud builds submit --tag gcr.io/PROJECT_ID/agentlogger-frontend ./frontend

# Deploy services
gcloud run deploy agentlogger-backend \
  --image gcr.io/PROJECT_ID/agentlogger-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy agentlogger-frontend \
  --image gcr.io/PROJECT_ID/agentlogger-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Vercel Deployment (Frontend)

**Perfect for**: Frontend-only deployment with serverless functions

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod

# Or use the deployment script
cd ..
./deploy-vercel.sh
```

**Vercel Configuration** (`vercel.json`):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-url.com/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

## 🏢 Method 4: Enterprise/Kubernetes Deployment

### Kubernetes Deployment

**Perfect for**: Large-scale, high-availability deployments

#### Namespace and ConfigMap

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: agentlogger

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agentlogger-config
  namespace: agentlogger
data:
  DATABASE_URL: "postgresql://user:password@postgres:5432/agentlogger"
  API_V1_STR: "/api/v1"
  CORS_ORIGINS: '["https://yourdomain.com"]'
```

#### Backend Deployment

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentlogger-backend
  namespace: agentlogger
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentlogger-backend
  template:
    metadata:
      labels:
        app: agentlogger-backend
    spec:
      containers:
      - name: backend
        image: agentlogger-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: agentlogger-config
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: agentlogger-secrets
              key: groq-api-key
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: agentlogger-backend-service
  namespace: agentlogger
spec:
  selector:
    app: agentlogger-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

#### Frontend Deployment

```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentlogger-frontend
  namespace: agentlogger
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agentlogger-frontend
  template:
    metadata:
      labels:
        app: agentlogger-frontend
    spec:
      containers:
      - name: frontend
        image: agentlogger-frontend:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 50m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi

---
apiVersion: v1
kind: Service
metadata:
  name: agentlogger-frontend-service
  namespace: agentlogger
spec:
  selector:
    app: agentlogger-frontend
  ports:
  - port: 8080
    targetPort: 8080
  type: ClusterIP
```

#### Ingress Configuration

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agentlogger-ingress
  namespace: agentlogger
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - yourdomain.com
    secretName: agentlogger-tls
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: agentlogger-backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: agentlogger-frontend-service
            port:
              number: 8080
```

#### Deploy to Kubernetes

```bash
# Apply all configurations
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n agentlogger
kubectl get services -n agentlogger
kubectl get ingress -n agentlogger

# View logs
kubectl logs -f deployment/agentlogger-backend -n agentlogger
```

## 🔧 Production Configuration

### Environment Variables

**Essential Production Settings:**

```bash
# Security
SECRET_KEY=your_very_long_random_secret_key_here
JWT_SECRET_KEY=another_random_secret_for_jwt_tokens

# API Configuration
GROQ_API_KEY=your_production_groq_api_key
GROQ_MODEL=llama3-70b-8192

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# CORS and Security
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com","www.yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
MAX_REQUEST_SIZE=10485760

# Monitoring
SENTRY_DSN=your_sentry_dsn_for_error_tracking
LOG_LEVEL=INFO

# Performance
WORKERS=4
MAX_CONNECTIONS=100
```

### Health Monitoring

```bash
# Health check endpoints
curl https://yourdomain.com/api/v1/health/
curl https://yourdomain.com/api/v1/health/db
curl https://yourdomain.com/api/v1/health/ai

# Monitor with scripts
#!/bin/bash
# health-monitor.sh
while true; do
  if ! curl -f https://yourdomain.com/api/v1/health/ > /dev/null 2>&1; then
    echo "$(date): Health check failed"
    # Send alert
  fi
  sleep 60
done
```

### Backup Strategy

```bash
# Database backup script
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://your-backup-bucket/
```

## 🔒 Security Considerations

### SSL/TLS Configuration

```nginx
# Strong SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Firewall Rules

```bash
# Ubuntu UFW example
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### API Security

```python
# Rate limiting in production
RATE_LIMIT_PER_MINUTE=60  # Adjust based on needs
MAX_REQUEST_SIZE=10485760  # 10MB

# API key validation
API_KEY_MIN_LENGTH=32
API_KEY_ALGORITHM=HS256
```

## 📊 Monitoring and Logging

### Log Aggregation

```yaml
# docker-compose.logging.yml
version: '3.8'
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        
  nginx:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Metrics Collection

```bash
# Prometheus monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Grafana dashboards  
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana
```

## 🚀 Performance Optimization

### Caching Strategy

```python
# Redis caching
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600  # 1 hour

# CDN configuration
# Use CloudFlare, AWS CloudFront, or similar
```

### Database Optimization

```sql
-- PostgreSQL optimizations
CREATE INDEX CONCURRENTLY idx_analysis_user_id ON analysis(user_id);
CREATE INDEX CONCURRENTLY idx_analysis_created_at ON analysis(created_at);
```

## 🧪 Testing Deployment

### Smoke Tests

```bash
#!/bin/bash
# smoke-test.sh

BASE_URL=${1:-"https://yourdomain.com"}
API_KEY=${2:-"your_test_api_key"}

echo "Testing $BASE_URL..."

# Test health endpoint
curl -f "$BASE_URL/api/v1/health/" || exit 1

# Test API with authentication
curl -f -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"code":"print(\"hello\")", "language":"python"}' || exit 1

echo "All tests passed!"
```

### Load Testing

```bash
# Apache Bench example
ab -n 1000 -c 10 -H "X-API-Key: your_api_key" \
  -p test-payload.json \
  -T application/json \
  https://yourdomain.com/api/v1/analyze

# K6 load testing
k6 run load-test.js
```

## 🆘 Troubleshooting

### Common Deployment Issues

**Docker Issues:**
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
docker system prune -f
```

**Database Connection:**
```bash
# Test database connectivity
docker-compose exec backend python -c "from app.core.db import engine; print(engine.execute('SELECT 1').scalar())"
```

**Network Issues:**
```bash
# Check port availability
netstat -tlnp | grep :8000
netstat -tlnp | grep :80

# Test internal connectivity
docker-compose exec backend curl http://localhost:8000/api/v1/health/
```

### Performance Issues

```bash
# Monitor resource usage
docker stats
htop
iotop

# Check application logs
tail -f /var/log/agentlogger/backend.log
tail -f /var/log/nginx/access.log
```

## 📚 Next Steps

After successful deployment:

1. **🔐 Set up monitoring** - Configure alerts for uptime and errors
2. **📊 Analytics** - Set up usage tracking and performance monitoring  
3. **🔒 Security** - Regular security updates and vulnerability scanning
4. **📈 Scaling** - Plan for horizontal scaling as usage grows
5. **🔄 CI/CD** - Automate deployments with GitHub Actions or similar

Choose the deployment method that best fits your needs, infrastructure, and expertise level! 🚀