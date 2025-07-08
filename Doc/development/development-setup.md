# AgentLogger Development Setup Guide

This guide covers setting up AgentLogger for development, including all the different ways to run the system for development and contribution.

## 🎯 Development Environment Options

| Method | Setup Time | Best For | Isolation | Hot Reload |
|--------|------------|----------|-----------|------------|
| **🐳 Docker Dev** | 2 minutes | Quick start, consistent env | ✅ High | ✅ Yes |
| **💻 Native** | 5 minutes | Performance, debugging | ❌ Low | ✅ Yes |
| **🔀 Hybrid** | 3 minutes | Backend dev, frontend stable | ⭐ Medium | ✅ Backend |
| **☁️ Codespaces** | 1 minute | Cloud development | ✅ High | ✅ Yes |

## 🐳 Method 1: Full Docker Development

**Best for**: Consistent environment, easy setup, testing deployment

```bash
# Clone and setup
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Create development environment file
cp env.example .env.dev
# Edit .env.dev with your development settings:
# GROQ_API_KEY=your_groq_key
# ENVIRONMENT=development
# DEBUG=true

# Start development stack
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f

# Access services
# Frontend: http://localhost:8080 (with hot reload)
# Backend: http://localhost:8000 (with auto-reload)
# Database: localhost:5432
```

**Development Features:**
- ✅ Hot reload for frontend changes
- ✅ Auto-reload for backend changes
- ✅ Volume mounts for live code editing
- ✅ Development database with test data
- ✅ Debug logging enabled
- ✅ Development CORS settings

### Docker Development Commands

```bash
# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# View service logs
docker-compose logs backend
docker-compose logs frontend

# Execute commands in containers
docker-compose exec backend python scripts/init_db.py
docker-compose exec backend pytest
docker-compose exec frontend npm test

# Rebuild after dependency changes
docker-compose build --no-cache backend
docker-compose build --no-cache frontend
```

## 💻 Method 2: Native Development

**Best for**: Maximum performance, detailed debugging, custom tooling

### Prerequisites

```bash
# System requirements
python --version  # 3.11+
node --version    # 18+
npm --version     # 9+

# Install system dependencies
# macOS
brew install postgresql redis

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm postgresql redis-server

# Windows (use WSL2 recommended)
# Install Python 3.11, Node.js 18+, PostgreSQL, Redis
```

### Backend Setup

```bash
# Clone repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Create environment file
cp env.example .env
# Edit .env with your settings:
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=dev_secret_key_for_development
DATABASE_URL=sqlite:///./agentlogger_dev.db
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:8080","http://localhost:3000"]
LOG_LEVEL=DEBUG
EOF

# Initialize database
python scripts/init_db.py

# Run database migrations (if any)
alembic upgrade head

# Start backend with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend Setup

```bash
# In new terminal, navigate to frontend
cd AgentLogger/frontend

# Install dependencies
npm install

# Install development dependencies
npm install --save-dev

# Create environment file for frontend
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=AgentLogger Dev
VITE_ENVIRONMENT=development
EOF

# Start development server
npm run dev

# Frontend will be available at http://localhost:8080
# Hot reload enabled for all changes
```

### Database Setup (PostgreSQL)

```bash
# Start PostgreSQL
# macOS
brew services start postgresql

# Ubuntu/Debian
sudo systemctl start postgresql

# Create development database
sudo -u postgres createdb agentlogger_dev
sudo -u postgres createuser agentlogger_user --createdb

# Update .env with PostgreSQL connection
DATABASE_URL=postgresql://agentlogger_user@localhost/agentlogger_dev

# Initialize database
python scripts/init_db.py
```

## 🔀 Method 3: Hybrid Development

**Best for**: Backend development with stable frontend, debugging specific components

### Option A: Backend Native + Frontend Docker

```bash
# Start only frontend with Docker
docker-compose up -d frontend database

# Run backend natively
cd AgentLogger
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access:
# Backend: http://localhost:8000 (native, debuggable)
# Frontend: http://localhost:8080 (Docker, stable)
```

### Option B: Frontend Native + Backend Docker

```bash
# Start only backend with Docker
docker-compose up -d backend database

# Run frontend natively
cd frontend
npm run dev

# Access:
# Backend: http://localhost:8000 (Docker, stable)
# Frontend: http://localhost:8080 (native, debuggable)
```

## ☁️ Method 4: GitHub Codespaces

**Best for**: Cloud development, team collaboration, quick contribution

```bash
# Open in Codespaces (click button in GitHub repo)
# Or create manually:

# In Codespace terminal
cp env.example .env
# Edit .env with your GROQ_API_KEY

# Quick Docker setup
docker-compose up -d

# Or native setup
source setup-codespace.sh  # We'll create this script
```

### Codespace Configuration (`.devcontainer/devcontainer.json`)

```json
{
  "name": "AgentLogger Development",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "backend",
  "workspaceFolder": "/app",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },
  "forwardPorts": [8000, 8080, 3000],
  "postCreateCommand": "scripts/setup-dev.sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode"
      ]
    }
  }
}
```

## 🛠️ Development Tools & Scripts

### Essential Development Scripts

Create these helpful scripts for development:

```bash
# scripts/dev-setup.sh - Complete development setup
#!/bin/bash
echo "Setting up AgentLogger development environment..."

# Backend setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Environment setup
cp env.example .env
echo "Please edit .env with your GROQ_API_KEY"

# Database setup
python scripts/init_db.py

# Frontend setup
cd frontend
npm install
cd ..

echo "Development setup complete!"
echo "Run: scripts/dev-start.sh to start all services"
```

```bash
# scripts/dev-start.sh - Start all development services
#!/bin/bash
echo "Starting AgentLogger development servers..."

# Start backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8080"
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID" INT
wait
```

```bash
# scripts/dev-test.sh - Run all tests
#!/bin/bash
echo "Running AgentLogger test suite..."

# Backend tests
source venv/bin/activate
echo "Running backend tests..."
pytest tests/ -v

# Frontend tests
echo "Running frontend tests..."
cd frontend
npm test
cd ..

echo "All tests completed!"
```

### Code Quality Tools

```bash
# Install development tools
pip install black isort flake8 mypy pytest-cov
npm install -g prettier eslint

# Backend formatting
black app/ tests/
isort app/ tests/
flake8 app/ tests/

# Frontend formatting
cd frontend
prettier --write src/
eslint src/ --fix
cd ..

# Type checking
mypy app/

# Test coverage
pytest tests/ --cov=app --cov-report=html
```

## 🐛 Debugging Setup

### Backend Debugging (VS Code)

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug FastAPI",
      "type": "python",
      "request": "launch",
      "program": "venv/bin/uvicorn",
      "args": ["app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Debug Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Frontend Debugging

```javascript
// frontend/vite.config.ts - Development configuration
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    sourcemap: true  // Enable source maps for debugging
  }
})
```

## 🧪 Testing Setup

### Backend Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api_keys.py -v

# Run specific test
pytest tests/test_api_keys.py::test_create_api_key -v

# Run integration tests
pytest tests/integration/ -v
```

### Frontend Testing

```bash
cd frontend

# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- Navigation.test.tsx
```

### End-to-End Testing

```bash
# Install Playwright
cd frontend
npx playwright install

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e:ui
```

## 📊 Development Monitoring

### Backend Monitoring

```bash
# View API logs
tail -f logs/agentlogger.log

# Monitor API performance
curl http://localhost:8000/api/v1/health/

# Database monitoring
python scripts/db-status.py
```

### Frontend Monitoring

```bash
# Bundle analysis
cd frontend
npm run build:analyze

# Performance monitoring
npm run lighthouse
```

## 🔄 Development Workflow

### 1. Daily Development

```bash
# Start your day
git pull origin main
scripts/dev-start.sh

# Make changes, test frequently
scripts/dev-test.sh

# Check code quality
black app/ && isort app/
cd frontend && prettier --write src/

# Commit changes
git add .
git commit -m "feat: add new feature"
git push origin feature-branch
```

### 2. Database Changes

```bash
# Create new migration
alembic revision --autogenerate -m "add new table"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### 3. Adding Dependencies

```bash
# Backend dependencies
pip install new-package
pip freeze | grep new-package >> requirements.txt

# Frontend dependencies
cd frontend
npm install new-package
# package.json is automatically updated
```

## 🚀 Deployment Testing

### Local Production Testing

```bash
# Test production build
docker-compose -f docker-compose.prod.yml up -d

# Test production frontend
cd frontend
npm run build
npm run preview

# Load testing
scripts/load-test.sh
```

### CI/CD Testing

```bash
# Simulate CI pipeline
scripts/ci-test.sh

# Test Docker builds
docker build -t agentlogger-backend .
docker build -t agentlogger-frontend ./frontend
```

## 🆘 Troubleshooting Development Issues

### Common Issues

**Port conflicts:**
```bash
# Kill processes on ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:8080 | xargs kill -9
```

**Database issues:**
```bash
# Reset development database
rm -f agentlogger_dev.db
python scripts/init_db.py
```

**Docker issues:**
```bash
# Clean Docker development
docker-compose down
docker system prune -f
docker-compose up -d --build
```

**Frontend build issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Getting Help

1. **Check logs**: Always check both backend and frontend logs
2. **Verify environment**: Ensure all environment variables are set
3. **Test API**: Use http://localhost:8000/docs to test backend
4. **Check database**: Verify database connection and data
5. **Ask community**: Open an issue or discussion on GitHub

## 📚 Next Steps

After setting up development:

1. **📖 Read Architecture Docs** - Understand the codebase structure
2. **🧪 Write Tests** - Add tests for your changes
3. **📝 Update Docs** - Keep documentation current
4. **🚀 Submit PR** - Follow the contribution guidelines
5. **🎉 Celebrate** - You're now a AgentLogger contributor!

Choose the development method that works best for your workflow and start contributing to AgentLogger! 🚀 