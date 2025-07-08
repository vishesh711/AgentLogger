# AgentLogger

An AI-powered multi-agent debugging assistant that helps developers detect, analyze, and fix code bugs using advanced language models and intelligent code analysis.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AgentLogger.git
cd AgentLogger
```

### 2. Set Up Environment
```bash
cp config/env.example .env
# Edit .env with your configuration (especially GROQ_API_KEY)
```

### 3. Start the Application
```bash
chmod +x scripts/start_app.sh
./scripts/start_app.sh
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
AgentLogger/
├── app/                    # Backend application
│   ├── agents/            # Multi-agent system
│   ├── api/               # API endpoints and routing
│   ├── core/              # Core configuration and utilities
│   ├── models/            # Database models and schemas
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── frontend/              # React frontend application
├── deployment/            # Docker and deployment files
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
├── config/                # Configuration files
│   ├── env.example
│   ├── requirements-vercel.txt
│   └── vercel.json
├── scripts/               # Utility scripts
│   ├── start_app.sh
│   ├── run.sh
│   ├── setup.sh
│   └── test.sh
├── docs/                  # Documentation
│   ├── setup/            # Setup guides
│   ├── deployment/       # Deployment guides
│   └── development/      # Development docs
├── database/             # Database files
├── logs/                 # Application logs
├── assets/               # Static assets
├── tests/                # Test suite
├── alembic/              # Database migrations
├── nginx/                # Nginx configuration
└── cli/                  # Command-line interface
```

## 🏗️ Architecture

### Multi-Agent System
- **Coordinator Agent**: Orchestrates the debugging workflow
- **Analyzer Agent**: Performs static code analysis
- **Fix Generator Agent**: Generates code fixes and improvements

### Backend Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **Groq**: AI/LLM integration

### Frontend Stack
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Vite**: Fast build tool

## 🔧 Development

### Local Development Setup
```bash
# Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend tests
pytest tests/ -v

# Frontend tests
cd frontend
npm run test
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 🚀 Deployment

### Docker Deployment
```bash
cd deployment
docker-compose up -d
```

### Production Deployment
```bash
cd deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Vercel Deployment
```bash
./docs/deployment/deploy-vercel.sh
```

### Vercel Deployment Setup

To set up Vercel deployment for this project, you need to add the following secrets to your GitHub repository:

1. `VERCEL_TOKEN`: Your Vercel API token (get from Vercel account settings)
2. `VERCEL_ORG_ID`: Your Vercel organization ID
3. `VERCEL_PROJECT_ID`: Your Vercel project ID

You can find the organization and project IDs in your Vercel project settings or by running:

```bash
vercel link
```

The deployment uses a simplified API for Vercel in `api/vercel_app.py` to ensure compatibility with Vercel's serverless environment.

## 📚 API Documentation

The API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
- `GET /health` - Health check
- `POST /api/v1/analyze` - Analyze code
- `POST /api/v1/fix` - Generate fixes
- `POST /api/v1/explain` - Explain code
- `GET /api/v1/agent-debug` - Debug agent system

## 🔐 Authentication

The API uses API key authentication. Include your API key in the `X-API-Key` header:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/analyze
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join our GitHub Discussions

## 🗺️ Roadmap

- [ ] Enhanced code analysis
- [ ] Support for more programming languages
- [ ] Integration with more IDEs
- [ ] Advanced debugging features
- [ ] Performance optimizations

## CI/CD and Deployment

### GitHub Actions CI/CD

The project uses GitHub Actions for continuous integration and deployment:

- **CI/CD Pipeline**: Runs tests, linting, and builds Docker images on each push to main and pull requests
- **Vercel Deployment**: Automatically deploys the frontend and API to Vercel when CI passes

### Vercel Deployment

The project is set up for deployment on Vercel with the following configuration:

- **Frontend**: Built with Bun and deployed as a static site
- **API**: Deployed as a serverless function using the Python runtime
- **Environment**: Production environment variables are configured in Vercel

To set up Vercel deployment:

1. Create a Vercel project and link it to your GitHub repository
2. Add the `VERCEL_TOKEN` secret to your GitHub repository
3. Configure environment variables in Vercel dashboard

### CI/CD Frontend Notes

The CI/CD pipeline is configured to handle cases where the frontend directory might be missing or incomplete:

1. If the frontend directory doesn't exist in the repository, a minimal structure will be created during the CI/CD run
2. The pipeline uses Bun for frontend builds and will adapt based on whether bun.lockb exists
3. For Vercel deployments, a placeholder frontend is created if needed

This ensures that CI/CD runs successfully even if you're primarily working on the backend components.