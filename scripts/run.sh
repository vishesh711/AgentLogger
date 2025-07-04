#!/bin/bash

# Print colored output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check for production mode flag
PRODUCTION=false
if [ "$1" == "--prod" ] || [ "$1" == "-p" ]; then
    PRODUCTION=true
    echo -e "${BLUE}Starting AgentLogger in PRODUCTION mode...${NC}"
else
    echo -e "${BLUE}Starting AgentLogger in DEVELOPMENT mode...${NC}"
fi

# Check if Docker Compose is installed
if command -v docker-compose &> /dev/null; then
    if [ "$PRODUCTION" = true ]; then
        echo -e "${GREEN}Starting with Docker Compose in PRODUCTION mode...${NC}"
        
        # Check if .env file exists, if not create it with default values
        if [ ! -f ".env" ]; then
            echo -e "${YELLOW}Creating .env file with default values...${NC}"
            echo "POSTGRES_PASSWORD=postgres" > .env
            echo "REDIS_PASSWORD=redis" >> .env
            echo -e "${YELLOW}Created .env file. Please update with secure passwords for production.${NC}"
        fi
        
        docker-compose -f docker-compose.prod.yml up
    else
        echo -e "${GREEN}Starting with Docker Compose in DEVELOPMENT mode...${NC}"
        docker-compose up
    fi
    exit 0
fi

# If Docker Compose is not available, start services manually
if [ "$PRODUCTION" = true ]; then
    echo -e "${YELLOW}Production mode requires Docker Compose. Please install Docker Compose and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}Starting backend server...${NC}"
# Start backend in the background
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${GREEN}Waiting for backend to start...${NC}"
sleep 3

echo -e "${GREEN}Starting frontend server...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo -e "${BLUE}Shutting down servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when script receives SIGINT (Ctrl+C)
trap cleanup SIGINT

# Keep the script running
echo -e "${BLUE}AgentLogger is running. Press Ctrl+C to stop.${NC}"
wait 