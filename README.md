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