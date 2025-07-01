# AgentLogger - AI-Powered Debugging Tool

AgentLogger is an advanced, production-ready debugging tool that uses AI-powered agents to analyze, explain, and fix code issues automatically. The system features a modern React frontend, robust FastAPI backend, and sophisticated multi-agent architecture for comprehensive debugging assistance.

## 🚀 Core Features

✅ **Multi-Agent Architecture**: Specialized AI agents working together  
✅ **Code Analysis**: Advanced static analysis with syntax error detection  
✅ **Error Explanation**: Multi-level explanations (simple, detailed, technical)  
✅ **Automated Fixes**: Generate patches and fixes for common code issues  
✅ **API Key Management**: Secure authentication with full CRUD operations  
✅ **Modern Web Interface**: Beautiful React frontend with real-time updates  
✅ **Multi-language Support**: Python and JavaScript (extensible architecture)  
✅ **Database Integration**: Persistent storage with PostgreSQL/SQLite support  
✅ **Docker Support**: Easy deployment with Docker Compose  

## 🏗️ Architecture

The system uses a sophisticated multi-agent architecture where specialized AI agents communicate through a message-passing system:

```
Frontend (React/Vite)
    ↓ HTTP API Calls
FastAPI Backend
    ↓ Agent System
┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │
│  Analyzer Agent ├─────►│ Fix Generator   │
│                 │      │                 │
└────────┬────────┘      └────────┬────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────────────────────────────┐
│                                         │
│           Coordinator Agent             │
│           (Message Router)              │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│                                         │
│         Database Layer                  │
│      (Analysis Results & API Keys)      │
└─────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, shadcn/ui
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Alembic
- **AI**: Groq LLM Integration (Llama3-70B)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: API Key-based with middleware
- **Deployment**: Docker, Docker Compose, Nginx

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### 1. Get Your Groq API Key
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up/login and create a new API key
3. Copy your API key (starts with `gsk_...`)

### 2. Set Up the Environment
```bash
# Clone the repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Set your Groq API key in docker-compose.yml
# Replace the placeholder in GROQ_API_KEY= with your actual key
# OR export it in your shell:
export GROQ_API_KEY="your_groq_key_here"
```

### 3. Launch the Application
```bash
# Start all services (frontend, backend, database)
docker-compose up -d

# Check that services are running
docker-compose ps
```

### 4. Access the Application
- **Web Interface**: http://localhost (served by nginx)
- **API Documentation**: http://localhost/docs  
- **Backend Direct**: http://localhost:8000 (if needed)
- **Frontend Direct**: http://localhost:8082 (development)

## 🔑 API Key Management

AgentLogger includes a full API key management system:

1. **Access API Keys Page**: Click "API Keys" in the navigation
2. **Create New Keys**: Use the "Create API Key" button
3. **Copy Keys**: Click the copy button to copy keys to clipboard
4. **Delete Keys**: Remove unused keys for security

**Default API Key** (for testing): `QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU`

## 📖 Usage Examples

### Analyze Code via Web Interface
1. Navigate to http://localhost
2. Go to "Playground" 
3. Paste your code
4. Click "Analyze" to get AI-powered analysis

### API Usage
```bash
# Analyze code with syntax errors
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "language": "python"
  }'

# Get explanations for errors
curl -X POST http://localhost/api/v1/explain \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python"
  }'
```

## 🔧 Configuration

Key environment variables (see `docs/guides/configuration.md` for complete reference):

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Your Groq LLM API key | - | ✅ Yes |
| `GROQ_MODEL` | LLM model to use | `llama3-70b-8192` | No |
| `DATABASE_URL` | Database connection | `sqlite:///./agentlogger.db` | No |
| `API_V1_STR` | API version prefix | `/api/v1` | No |
| `CORS_ORIGINS` | Allowed origins | `["http://localhost:8082"]` | No |

## 📚 Documentation

- **[Getting Started Guide](docs/guides/getting-started.md)** - Detailed setup instructions
- **[API Documentation](docs/api/index.md)** - Complete API reference
- **[Configuration Guide](docs/guides/configuration.md)** - All configuration options
- **[Development Setup](docs/development/development-setup.md)** - Local development
- **[Agent Architecture](docs/development/agent-architecture.md)** - System design

## 🐛 Development

### Local Development Setup
```bash
# Backend setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend setup  
cd frontend
npm install
npm run dev

# Run backend
cd ..
python -m uvicorn app.main:app --reload
```

See [Development Setup](docs/development/development-setup.md) for detailed instructions.

### Testing
```bash
# Run backend tests
pytest

# Run frontend tests  
cd frontend && npm test
```

## 🔍 Current Status

✅ **Fully Functional**
- Multi-agent workflow system
- Code analysis and fixing
- API key authentication  
- Web interface with all pages
- Database operations
- CORS configuration
- Error handling

✅ **Recently Fixed Issues**
- UUID handling in database queries
- API keys CRUD operations
- Frontend routing and navigation
- CORS configuration for all ports
- Authentication middleware

## 🤝 Contributing

See [Contributing Guide](docs/development/contributing.md) for:
- Code style guidelines
- Development workflow
- Testing requirements
- Pull request process

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Documentation**: Check the `docs/` directory for detailed guides
- **FAQ**: See [docs/guides/faq.md](docs/guides/faq.md) for common questions