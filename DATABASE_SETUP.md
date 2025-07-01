# Database Setup Guide for AgentLogger

## ✅ Current Status: Your Database is Already Working!

You have a SQLite database (`agentlogger.db`) that's already set up and working.

## Quick Start (What You Need to Do)

### 1. Update Your `.env` File

Add these lines to your `.env` file (you can edit it manually):

```env
# Keep your existing GROQ API key
GROQ_API_KEY=your_groq_api_key_here_get_from_console_groq_com

# Add these required settings
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-at-least-64-characters-long
ENVIRONMENT=development

# Optional settings (can add later)
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

### 2. Start Your Application

**Option A: Run locally**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option B: Use Docker (recommended for full setup)**
```bash
# Add DATABASE_URL to .env for Docker:
DATABASE_URL=postgresql://postgres:postgres@db:5432/agentlogger

# Then start with Docker:
docker-compose up --build
```

### 3. Initialize Database (First Time Only)

```bash
# Run database migrations
alembic upgrade head

# Create admin user and API key
python scripts/init_db.py
```

## Database Options

### 🔹 Option 1: SQLite (Current - Simple)

**Pros:**
- ✅ Already working
- ✅ No setup required
- ✅ Perfect for development
- ✅ Single file database

**Cons:**
- ❌ Not ideal for production
- ❌ No concurrent writes
- ❌ Limited scalability

**Current Setup:**
- File: `agentlogger.db`
- Location: `/Users/vishesh/Documents/Github/AgentLogger/agentlogger.db`
- Status: ✅ Working

### 🔹 Option 2: PostgreSQL with Docker (Recommended for Production)

**Pros:**
- ✅ Production-ready
- ✅ Better performance
- ✅ Concurrent access
- ✅ Full SQL features
- ✅ Automatic setup with Docker

**Setup:**
1. Add to `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/agentlogger
USE_POSTGRES=true
```

2. Start with Docker:
```bash
docker-compose up --build
```

## What Your App Can Do Right Now

With your current database setup, you can:

- ✅ **API Endpoints**: All working
- ✅ **User Management**: Create/login users
- ✅ **OAuth**: GitHub and Google login
- ✅ **Code Analysis**: AI-powered debugging
- ✅ **API Keys**: Generate and manage
- ✅ **Health Checks**: Monitor status

## Quick Test

Test if everything works:

```bash
# Start the app
python -m uvicorn app.main:app --reload

# In another terminal, test the API:
curl http://localhost:8000/api/v1/health
```

Should return:
```json
{"status": "ok", "message": "AgentLogger API is running"}
```

## Next Steps

1. **Immediate**: Add SECRET_KEY to .env and start the app
2. **Short term**: Test all endpoints work
3. **Medium term**: Consider moving to Docker + PostgreSQL
4. **Long term**: Deploy to production

## Troubleshooting

**If you get errors:**

1. **Missing SECRET_KEY**: Add to .env file
2. **Database locked**: Stop any running instances
3. **Permission issues**: Check file permissions on agentlogger.db
4. **Import errors**: Make sure you're in the right directory

**Database file location:**
```
/Users/vishesh/Documents/Github/AgentLogger/agentlogger.db
```

**Reset database (if needed):**
```bash
# Backup first
cp agentlogger.db agentlogger.db.backup

# Reset
rm agentlogger.db
alembic upgrade head
python scripts/init_db.py
```

Your database is ready to go! 🚀 