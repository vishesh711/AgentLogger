# Deploying AgentLogger to Vercel

This guide will help you deploy AgentLogger to Vercel with both the frontend and backend components.

## 🏗️ Architecture Overview

AgentLogger on Vercel uses a split deployment approach:

- **Frontend**: React app deployed as a static site
- **Backend**: FastAPI deployed as serverless functions
- **Database**: External PostgreSQL (Vercel Postgres or Supabase)

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your AgentLogger code to GitHub
3. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)
4. **Database**: Set up Vercel Postgres or external database

## 🚀 Method 1: Full-Stack Deployment (Recommended)

### Step 1: Database Setup

#### Option A: Vercel Postgres
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Create Postgres database
vercel postgres create agentlogger-db
```

#### Option B: External Database (Supabase)
1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project
3. Get your PostgreSQL connection string

### Step 2: Environment Variables

Set these environment variables in your Vercel project:

```bash
# Required
GROQ_API_KEY=gsk_your_groq_api_key_here
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_super_secret_key_here

# Optional
ENVIRONMENT=production
CORS_ORIGINS=["https://your-app.vercel.app"]
RATE_LIMIT_PER_MINUTE=60
```

### Step 3: Deploy via Vercel Dashboard

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Build Settings**:
   - **Framework Preset**: Other
   - **Root Directory**: Leave empty (uses root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`

3. **Add Environment Variables**:
   - Add all the environment variables listed above

4. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy your application

## 🔄 Method 2: Separate Frontend/Backend Deployment

### Deploy Backend Only

1. **Create Backend-Only Repository**:
```bash
# Create a new repository with just the backend
mkdir agentlogger-backend
cd agentlogger-backend

# Copy backend files
cp -r ../AgentLogger/app .
cp ../AgentLogger/requirements-vercel.txt ./requirements.txt
cp ../AgentLogger/alembic.ini .
cp -r ../AgentLogger/alembic .
```

2. **Create `vercel.json`**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app/main.py"
    }
  ]
}
```

3. **Deploy to Vercel**:
   - Import this repository to Vercel
   - Set environment variables
   - Deploy

### Deploy Frontend Only

1. **Update API URL**:
   - Edit `frontend/src/lib/api.ts`
   - Update `API_BASE_URL` to your backend Vercel URL

2. **Deploy Frontend**:
   - Import the `frontend` directory to Vercel
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

## ⚙️ Configuration Files

### Root `vercel.json` (Full-Stack)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "50mb" }
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "dist" }
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/app/main.py" },
    { "src": "/(.*)", "dest": "/frontend/$1" }
  ]
}
```

### Frontend-Only `vercel.json`
```json
{
  "version": 2,
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

## 🗄️ Database Migration

### Run Migrations on Vercel

1. **Create Migration Script** (`migrate.py`):
```python
import asyncio
from alembic.config import Config
from alembic import command
import os

def run_migrations():
    """Run database migrations"""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
```

2. **Add Build Hook** (in `vercel.json`):
```json
{
  "functions": {
    "app/main.py": {
      "maxDuration": 30
    }
  },
  "build": {
    "env": {
      "PYTHON_VERSION": "3.11"
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **Build Failures**
```bash
# Check build logs in Vercel dashboard
# Common fixes:
- Ensure all dependencies in requirements-vercel.txt
- Check Python version compatibility
- Verify environment variables are set
```

#### 2. **Database Connection Issues**
```bash
# Test connection string locally
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
print('Connection successful!')
"
```

#### 3. **CORS Issues**
```bash
# Update CORS_ORIGINS in environment variables
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

#### 4. **API Key Issues**
```bash
# Verify in Vercel dashboard > Project > Settings > Environment Variables
GROQ_API_KEY=gsk_...
```

### Performance Optimization

#### 1. **Cold Start Reduction**
```python
# In app/main.py, add:
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up connections
    yield

app = FastAPI(lifespan=lifespan)
```

#### 2. **Caching**
```json
{
  "headers": [
    {
      "source": "/(.*\\.(js|css|png|jpg|jpeg|gif|ico|svg))",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## 📊 Monitoring & Analytics

### Vercel Analytics
1. Enable Vercel Analytics in project settings
2. Add analytics code to frontend

### Error Tracking
```bash
# Add to environment variables
SENTRY_DSN=your_sentry_dsn
SENTRY_ENVIRONMENT=production
```

## 🔄 CI/CD with Vercel

### Automatic Deployments
- **Production**: Deploys on push to `main` branch
- **Preview**: Deploys on pull requests
- **Development**: Manual deployments

### Custom Deployment Hooks
```json
{
  "github": {
    "silent": true
  },
  "functions": {
    "app/main.py": {
      "maxDuration": 30
    }
  }
}
```

## 🚦 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.vercel.app/api/v1/health/health
```

### 2. API Test
```bash
curl -X POST https://your-app.vercel.app/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

### 3. Frontend Test
- Visit `https://your-app.vercel.app`
- Test navigation and functionality
- Check API key management

## 💡 Best Practices

### 1. **Environment Management**
- Use different Vercel projects for staging/production
- Keep sensitive data in environment variables
- Use Vercel's built-in secrets management

### 2. **Performance**
- Optimize bundle size
- Use CDN for static assets
- Implement proper caching headers

### 3. **Security**
- Enable Vercel's security headers
- Use HTTPS everywhere
- Implement proper CORS policies

### 4. **Monitoring**
- Set up error tracking with Sentry
- Monitor API usage and performance
- Use Vercel Analytics for insights

## 🆘 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **AgentLogger Issues**: Create GitHub issues
- **Community**: Vercel Discord or AgentLogger discussions

---

**Ready to deploy?** Start with Method 1 for the simplest full-stack deployment! 🚀 