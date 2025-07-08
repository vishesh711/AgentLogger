# AgentLogger Installation & Deployment Guide

This comprehensive guide covers all the different ways to install and run AgentLogger, from quick testing to production deployment.

## 🚀 Quick Start (Recommended)

The fastest way to get AgentLogger running:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# 2. Set your Groq API key
export GROQ_API_KEY="your_groq_key_here"

# 3. Launch with Docker
docker-compose up -d

# 4. Access the application
# Web Interface: http://localhost
# API Documentation: http://localhost/docs
```

## 📋 Prerequisites

### Required
- **Git** - For cloning the repository
- **Groq API Key** - Get free at [console.groq.com](https://console.groq.com)

### Choose Your Method
- **Docker** (Recommended) - Docker & Docker Compose
- **Manual Setup** - Python 3.11+, Node.js 18+
- **Development** - All of the above + IDE

## 🐳 Method 1: Docker Deployment (Recommended)

### Option A: Simple Docker Compose

**Best for**: Quick testing, development, small deployments

```bash
# Clone repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Configure environment
cp env.example .env
# Edit .env and set your GROQ_API_KEY

# Launch all services
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f
```

**Services Started:**
- ✅ Backend API (FastAPI) - Port 8000
- ✅ Frontend (React/Vite) - Port 8080  
- ✅ Database (SQLite in development)
- ✅ Nginx Proxy - Port 80

### Option B: Production Docker

**Best for**: Production deployments, staging environments

```bash
# Clone repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Configure production environment
cp env.example .env.prod
# Edit .env.prod with production settings

# Launch production stack
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

**Production Features:**
- ✅ Optimized builds
- ✅ SSL/HTTPS support
- ✅ Production database (PostgreSQL)
- ✅ Nginx with production config
- ✅ Health checks
- ✅ Restart policies

### Option C: Individual Docker Containers

**Best for**: Custom deployments, microservices architecture

```bash
# Build images
docker build -t agentlogger-backend .
docker build -t agentlogger-frontend ./frontend

# Run backend
docker run -d \
  --name agentlogger-api \
  -p 8000:8000 \
  -e GROQ_API_KEY=your_key_here \
  agentlogger-backend

# Run frontend  
docker run -d \
  --name agentlogger-frontend \
  -p 8080:8080 \
  agentlogger-frontend
```

## 💻 Method 2: Manual Installation

### Option A: Full Manual Setup

**Best for**: Development, customization, learning the system

```bash
# 1. Clone repository
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# 2. Backend Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Environment Configuration
cp env.example .env
# Edit .env file with your configuration

# 4. Database Setup
python scripts/init_db.py

# 5. Start Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Frontend Setup (New Terminal)
cd frontend
npm install
npm run dev

# 7. Access Application
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

### Option B: Backend Only

**Best for**: API-only usage, custom frontend

```bash
# Setup backend
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp env.example .env
# Edit .env with your GROQ_API_KEY

# Initialize database
python scripts/init_db.py

# Start API server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test API
curl http://localhost:8000/api/v1/health/
```

### Option C: Development Setup

**Best for**: Contributing, development, debugging

```bash
# Full development setup
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Backend with hot reload
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Database setup
python scripts/init_db.py

# Start backend with reload
uvicorn app.main:app --reload --host 0.0.0.0

# Frontend with hot reload (new terminal)
cd frontend
npm install
npm run dev

# Run tests
pytest  # Backend tests
cd frontend && npm test  # Frontend tests
```

## ☁️ Method 3: Cloud Deployment

### Option A: Vercel (Frontend + Serverless Backend)

**Best for**: Quick cloud deployment, serverless

```bash
# Deploy to Vercel
npm install -g vercel
vercel --prod

# Or use the deploy script
./deploy-vercel.sh
```

### Option B: VPS/Server Deployment

**Best for**: Full control, custom domains

```bash
# On your server
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger

# Configure for production
cp env.example .env
# Set production environment variables

# Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# Setup reverse proxy (nginx example)
sudo nginx -t
sudo systemctl reload nginx
```

### Option C: Container Platforms (AWS ECS, Google Cloud Run, etc.)

**Best for**: Scalable cloud deployment

```bash
# Build and tag for registry
docker build -t your-registry/agentlogger:latest .
docker push your-registry/agentlogger:latest

# Deploy to your container platform
# (Commands vary by platform)
```

## 🔧 Method 4: CLI Installation

### Install AgentLogger CLI

```bash
# From PyPI (when available)
pip install agent-logger-cli

# From source
cd cli
pip install -e .

# Configure CLI
agent-logger configure --api-key YOUR_API_KEY --api-url http://localhost:8000/api/v1
```

### CLI Usage Examples

```bash
# Analyze code
agent-logger analyze --file buggy_code.py

# Get explanations
agent-logger explain --code "print(hello world)" --language python

# Generate fixes
agent-logger fix --file broken_script.js
```

## 🚀 Quick Access URLs

Once running, access AgentLogger at:

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Main App** | http://localhost | Beautiful web interface |
| 🎮 **Playground** | http://localhost/playground | Interactive testing |
| 📊 **Dashboard** | http://localhost/dashboard | Analytics & management |
| 🔑 **API Keys** | http://localhost/api-keys | Key management |
| 📚 **API Docs** | http://localhost/docs | Complete API reference |
| 🔧 **Backend** | http://localhost:8000 | Direct API access |

## ✅ Verification Steps

### 1. Check Services
```bash
# Docker method
docker-compose ps

# Manual method
curl http://localhost:8000/api/v1/health/
curl http://localhost:8080  # Frontend
```

### 2. Test API
```bash
# Get API key from web interface, then test:
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"code": "print(hello)", "language": "python"}'
```

### 3. Test Web Interface
1. Open http://localhost in browser
2. Navigate to Playground
3. Test code analysis functionality
4. Check API Keys page

## 🛠️ Troubleshooting

### Common Issues

**Port Conflicts:**
```bash
# Check what's using ports
lsof -i :8000  # Backend
lsof -i :8080  # Frontend
lsof -i :80    # Nginx

# Kill processes if needed
sudo kill -9 PID
```

**Docker Issues:**
```bash
# Reset Docker state
docker-compose down
docker system prune -f
docker-compose up -d --build
```

**Environment Variables:**
```bash
# Check if variables are set
echo $GROQ_API_KEY
cat .env
```

**Database Issues:**
```bash
# Reset database
rm -f agentlogger.db  # SQLite
python scripts/init_db.py
```

## 📚 Next Steps

1. **📖 Read the [Configuration Guide](configuration.md)** - Detailed settings
2. **🎯 Try the [Getting Started Tutorial](getting-started.md)** - Step-by-step usage
3. **📊 Explore the [API Documentation](../api/index.md)** - Complete API reference
4. **🔧 Set up [Development Environment](../development/development-setup.md)** - For contributors

## 🆘 Need Help?

- **📚 Documentation**: Check other guides in this directory
- **🐛 Issues**: Open an issue on GitHub
- **💬 Discussions**: Join our GitHub Discussions
- **📧 Support**: Contact the development team

Choose the method that best fits your needs and get started with AgentLogger! 🚀 