#!/bin/bash

# AgentLogger Startup Script

echo "🚀 Starting AgentLogger..."

# Check if .env has SECRET_KEY
if ! grep -q "SECRET_KEY=" .env 2>/dev/null; then
    echo "⚠️  Warning: SECRET_KEY not found in .env file"
    echo "Please add this line to your .env file:"
    echo "SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-at-least-64-characters-long"
    echo ""
fi

# Set default environment if not set
export ENVIRONMENT=${ENVIRONMENT:-development}

# Check if database needs initialization
if [ ! -f "agentlogger.db" ]; then
    echo "📊 Initializing database..."
    python scripts/init_db.py
fi

echo "🔧 Starting FastAPI server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API docs will be available at: http://localhost:8000/docs"
echo "❤️  Health check: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 