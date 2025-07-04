#!/bin/bash

# AgentLogger Application Startup Script
# This script starts the entire AgentLogger application stack

set -e

echo "🚀 Starting AgentLogger Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp config/env.example .env
    echo "📝 Please edit .env file with your configuration and run again."
    exit 1
fi

# Load environment variables
source .env

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your-groq-api-key-here" ]; then
    echo "⚠️  GROQ_API_KEY not set in .env file."
    echo "📝 Please set your GROQ_API_KEY in the .env file and run again."
    exit 1
fi

echo "📦 Building and starting services..."

# Start the application stack
cd deployment
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."

# Wait for database to be ready
echo "🗄️  Waiting for database..."
until docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; do
    sleep 2
done

echo "✅ Database is ready!"

# Wait for backend to be ready
echo "🔧 Waiting for backend..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    sleep 2
done

echo "✅ Backend is ready!"

# Wait for frontend to be ready
echo "🎨 Waiting for frontend..."
until curl -f http://localhost:3000 > /dev/null 2>&1; do
    sleep 2
done

echo "✅ Frontend is ready!"

echo ""
echo "🎉 AgentLogger is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📋 To stop the application: cd deployment && docker-compose down"
echo "📋 To view logs: cd deployment && docker-compose logs -f" 