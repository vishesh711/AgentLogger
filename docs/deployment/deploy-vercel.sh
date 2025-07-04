#!/bin/bash
# AgentLogger Vercel Deployment Script

set -e

echo "🚀 AgentLogger Vercel Deployment Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Vercel CLI is installed
check_vercel_cli() {
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI not found. Installing..."
        npm install -g vercel
        print_success "Vercel CLI installed"
    else
        print_success "Vercel CLI found"
    fi
}

# Check if user is logged into Vercel
check_vercel_auth() {
    if ! vercel whoami &> /dev/null; then
        print_warning "Not logged into Vercel. Please login:"
        vercel login
    else
        print_success "Logged into Vercel as $(vercel whoami)"
    fi
}

# Check required environment variables
check_env_vars() {
    print_status "Checking required environment variables..."
    
    if [ -z "$GROQ_API_KEY" ]; then
        print_warning "GROQ_API_KEY not set in environment"
        read -p "Enter your Groq API key: " GROQ_API_KEY
        export GROQ_API_KEY
    fi
    
    if [ -z "$DATABASE_URL" ]; then
        print_warning "DATABASE_URL not set"
        echo "You'll need to set this in Vercel dashboard or use Vercel Postgres"
    fi
    
    print_success "Environment variables checked"
}

# Build frontend
build_frontend() {
    print_status "Building frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    print_status "Building frontend..."
    npm run build
    
    if [ $? -eq 0 ]; then
        print_success "Frontend build completed"
    else
        print_error "Frontend build failed"
        exit 1
    fi
    
    cd ..
}

# Test backend dependencies
test_backend() {
    print_status "Testing backend dependencies..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    if [ -f "requirements-vercel.txt" ]; then
        pip install -r requirements-vercel.txt
    else
        pip install -r requirements.txt
    fi
    
    python -c "import app.main; print('Backend imports successful')"
    
    if [ $? -eq 0 ]; then
        print_success "Backend test completed"
    else
        print_error "Backend test failed"
        exit 1
    fi
}

# Deploy to Vercel
deploy_to_vercel() {
    print_status "Deploying to Vercel..."
    
    # Set environment variables for deployment
    vercel env add GROQ_API_KEY "$GROQ_API_KEY" production
    
    if [ ! -z "$DATABASE_URL" ]; then
        vercel env add DATABASE_URL "$DATABASE_URL" production
    fi
    
    if [ ! -z "$SECRET_KEY" ]; then
        vercel env add SECRET_KEY "$SECRET_KEY" production
    else
        print_warning "SECRET_KEY not set. Using default for demo."
        vercel env add SECRET_KEY "your-super-secret-key-change-in-production" production
    fi
    
    # Deploy
    vercel --prod
    
    if [ $? -eq 0 ]; then
        print_success "Deployment completed successfully!"
        print_status "Your app should be available at the URL shown above"
    else
        print_error "Deployment failed"
        exit 1
    fi
}

# Setup Vercel Postgres (optional)
setup_vercel_postgres() {
    read -p "Do you want to set up Vercel Postgres? (y/n): " setup_db
    
    if [ "$setup_db" = "y" ] || [ "$setup_db" = "Y" ]; then
        print_status "Setting up Vercel Postgres..."
        vercel postgres create agentlogger-db
        
        print_status "Getting database URL..."
        DATABASE_URL=$(vercel env ls | grep DATABASE_URL | awk '{print $2}')
        
        if [ ! -z "$DATABASE_URL" ]; then
            print_success "Vercel Postgres setup completed"
            export DATABASE_URL
        else
            print_warning "Could not retrieve DATABASE_URL automatically"
            print_status "Please set it manually in Vercel dashboard"
        fi
    fi
}

# Run database migrations
run_migrations() {
    read -p "Do you want to run database migrations? (y/n): " run_migrate
    
    if [ "$run_migrate" = "y" ] || [ "$run_migrate" = "Y" ]; then
        if [ -z "$DATABASE_URL" ]; then
            print_error "DATABASE_URL not set. Cannot run migrations."
            return 1
        fi
        
        print_status "Running database migrations..."
        source venv/bin/activate
        alembic upgrade head
        
        if [ $? -eq 0 ]; then
            print_success "Database migrations completed"
        else
            print_error "Database migrations failed"
        fi
    fi
}

# Main deployment flow
main() {
    echo "Select deployment option:"
    echo "1. Full deployment (recommended)"
    echo "2. Frontend only"
    echo "3. Backend only"
    echo "4. Setup only (no deployment)"
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            print_status "Starting full deployment..."
            check_vercel_cli
            check_vercel_auth
            check_env_vars
            setup_vercel_postgres
            build_frontend
            test_backend
            run_migrations
            deploy_to_vercel
            ;;
        2)
            print_status "Starting frontend-only deployment..."
            check_vercel_cli
            check_vercel_auth
            build_frontend
            cd frontend
            vercel --prod
            cd ..
            ;;
        3)
            print_status "Starting backend-only deployment..."
            check_vercel_cli
            check_vercel_auth
            check_env_vars
            test_backend
            # Deploy backend only (requires backend-specific vercel.json)
            vercel --prod
            ;;
        4)
            print_status "Setup only..."
            check_vercel_cli
            check_vercel_auth
            check_env_vars
            setup_vercel_postgres
            print_success "Setup completed. Run script again to deploy."
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    print_success "Deployment process completed!"
    echo ""
    echo "🎉 Next Steps:"
    echo "1. Check your deployment at the URL provided"
    echo "2. Test the API endpoints"
    echo "3. Configure domain (optional)"
    echo "4. Set up monitoring and analytics"
    echo ""
    echo "📚 For more help, see: docs/guides/vercel-deployment.md"
}

# Run main function
main "$@" 