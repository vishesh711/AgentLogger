#!/bin/bash

# Print colored output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing AgentLogger setup...${NC}"

# Check backend dependencies
echo -e "${GREEN}Checking backend dependencies...${NC}"
if ! pip list | grep -q "fastapi"; then
    echo -e "${RED}Backend dependencies not installed. Run ./setup.sh first.${NC}"
    exit 1
fi

# Check frontend dependencies
echo -e "${GREEN}Checking frontend dependencies...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}Frontend dependencies not installed. Run ./setup.sh first.${NC}"
    exit 1
fi

# Check database
echo -e "${GREEN}Checking database...${NC}"
if [ ! -f "app.db" ]; then
    echo -e "${RED}Database not set up. Run ./setup.sh first.${NC}"
    exit 1
fi

# Check if the backend server responds
echo -e "${GREEN}Testing backend server...${NC}"
curl -s http://localhost:8000/health > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Backend server not responding. Run ./run.sh first.${NC}"
    exit 1
fi

# Check if the frontend server responds
echo -e "${GREEN}Testing frontend server...${NC}"
curl -s http://localhost:3000 > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Frontend server not responding. Run ./run.sh first.${NC}"
    exit 1
fi

echo -e "${BLUE}All tests passed! AgentLogger is set up correctly.${NC}" 