#!/bin/bash

# Print colored output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up AgentLogger...${NC}"

# Install backend dependencies
echo -e "${GREEN}Installing backend dependencies...${NC}"
pip install -r requirements.txt

# Database setup
echo -e "${GREEN}Setting up the database...${NC}"

# Check if PostgreSQL is requested
if [ "$1" == "--postgres" ] || [ "$1" == "-p" ]; then
    echo -e "${YELLOW}Setting up PostgreSQL database...${NC}"
    
    # Check if PostgreSQL URL is provided
    if [ -z "$2" ]; then
        echo -e "${YELLOW}No PostgreSQL URL provided. Using default: postgresql://postgres:postgres@localhost/agentlogger${NC}"
        export DATABASE_URL="postgresql://postgres:postgres@localhost/agentlogger"
    else
        echo -e "${YELLOW}Using provided PostgreSQL URL${NC}"
        export DATABASE_URL="$2"
    fi
    
    # Check if alembic is installed
    if ! command -v alembic &> /dev/null; then
        echo -e "${YELLOW}Installing alembic...${NC}"
        pip install alembic
    fi
    
    # Run migrations
    echo -e "${YELLOW}Running database migrations...${NC}"
    alembic upgrade head
else
    echo -e "${YELLOW}Setting up SQLite database (default)...${NC}"
    python scripts/init_db.py
    
    echo -e "${YELLOW}Note: For production use, consider using PostgreSQL:${NC}"
    echo -e "${YELLOW}./setup.sh --postgres \"postgresql://user:password@localhost/agentlogger\"${NC}"
fi

# Install frontend dependencies
echo -e "${GREEN}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..

# Generate API key if it doesn't exist
if [ ! -f ".api_key" ]; then
    echo -e "${GREEN}Generating API key...${NC}"
    python scripts/generate_api_key.py > .api_key
    echo -e "${YELLOW}API key saved to .api_key file${NC}"
fi

# Make the run script executable
chmod +x run.sh

echo -e "${BLUE}Setup complete! You can now run the application with ./run.sh${NC}"
echo -e "${YELLOW}API Key: $(cat .api_key)${NC}" 