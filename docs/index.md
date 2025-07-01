# AgentLogger Documentation

Welcome to AgentLogger - an advanced, production-ready AI-powered debugging tool that helps you identify, analyze, and fix code issues automatically.

## 🚀 What is AgentLogger?

AgentLogger is a sophisticated debugging platform that combines:

- **Multi-Agent AI System**: Specialized AI agents that work together to analyze and fix code
- **Modern Web Interface**: Beautiful React frontend with real-time updates
- **Comprehensive API**: RESTful API for integration with IDEs and development tools
- **Multi-Language Support**: Currently supports Python and JavaScript (extensible architecture)
- **Database Integration**: Persistent storage of analysis results and user data

## 🎯 Key Features

✅ **Advanced Code Analysis**: Static analysis with syntax error detection  
✅ **AI-Powered Fixes**: Automatic generation of code fixes and improvements  
✅ **Multi-Level Explanations**: Error explanations for all skill levels  
✅ **API Key Management**: Secure authentication with full CRUD operations  
✅ **Real-Time Interface**: Interactive playground for immediate feedback  
✅ **Production Ready**: Docker deployment with PostgreSQL support  

## 📖 Documentation Structure

### 🏁 Getting Started
- **[Getting Started Guide](guides/getting-started.md)** - Quick setup and first steps
- **[Installation Guide](guides/installation.md)** - Detailed installation instructions
- **[Configuration Guide](guides/configuration.md)** - Environment configuration options

### 📚 User Guides
- **[Core Functionality](guides/core-functionality.md)** - How to use AgentLogger's features
- **[CLI Usage](guides/cli.md)** - Command-line interface guide
- **[FAQ](guides/faq.md)** - Frequently asked questions
- **[Deployment](guides/deployment.md)** - Production deployment guide

### 🔧 API Documentation
- **[API Overview](api/index.md)** - Complete API reference and examples
- **[Code Analysis](api/analyze.md)** - Code analysis endpoints
- **[Error Explanation](api/explain.md)** - Error explanation endpoints
- **[Fix Generation](api/fix.md)** - Code fixing endpoints
- **[Patch Creation](api/patch.md)** - Patch generation endpoints

### 🛠️ Development
- **[Development Setup](development/development-setup.md)** - Local development environment
- **[Agent Architecture](development/agent-architecture.md)** - System design and architecture
- **[Frontend Development](development/frontend.md)** - React frontend development
- **[Contributing Guide](development/contributing.md)** - How to contribute to the project
- **[Testing](development/testing.md)** - Testing guidelines and setup

## 🚀 Quick Start

### 1. Prerequisites
- Docker and Docker Compose
- Groq API key (get one free at [console.groq.com](https://console.groq.com))

### 2. Launch AgentLogger
```bash
# Clone the repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Set your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"

# Start all services
docker-compose up -d
```

### 3. Access the Application
- **Web Interface**: http://localhost
- **API Documentation**: http://localhost/docs

### 4. Test the System
Navigate to the Playground and paste some buggy code to see AgentLogger in action!

## 🏗️ System Architecture

AgentLogger uses a sophisticated multi-agent architecture:

```
Frontend (React/TypeScript)
    ↓ HTTP API
FastAPI Backend
    ↓ Message Passing
┌─────────────────┐    ┌─────────────────┐
│  Analyzer       │───►│  Fix Generator  │
│  Agent          │    │  Agent          │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────┐
│           Coordinator Agent             │
│         (Message Router)                │
└─────────┬───────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│         Database Layer                  │
│    (PostgreSQL/SQLite)                  │
└─────────────────────────────────────────┘
```

## 💡 Use Cases

### For Developers
- **Debug Complex Issues**: Get AI assistance with hard-to-understand errors
- **Learn from Fixes**: Understand why fixes work with detailed explanations
- **Code Review**: Identify potential issues before they reach production
- **IDE Integration**: Use the API to add AgentLogger to your development environment

### For Teams
- **Consistent Code Quality**: Standardized analysis across team members
- **Knowledge Sharing**: Multi-level explanations help team members learn
- **Automated Fixes**: Reduce time spent on common coding issues
- **API Integration**: Build custom workflows with the REST API

### For Educational Use
- **Teaching Tool**: Help students understand error messages and fixes
- **Code Examples**: Show correct implementations alongside explanations
- **Progressive Learning**: Explanations tailored to different skill levels

## 🛠️ Technology Stack

- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, shadcn/ui
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Alembic
- **AI**: Groq LLM Integration (Llama3-70B, Mixtral, etc.)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: API Key-based with secure middleware
- **Deployment**: Docker, Docker Compose, Nginx
- **Testing**: Pytest (backend), Jest (frontend)

## 🎮 Interactive Examples

### Web Interface
1. Visit http://localhost after setup
2. Go to the "Playground" page
3. Paste buggy code and see instant analysis

### API Usage
```bash
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

## 📊 Current Status

✅ **Fully Functional Features**
- Multi-agent analysis workflow
- Code analysis for Python and JavaScript
- Error explanation with multiple detail levels
- Automated fix generation
- API key management system
- Modern web interface
- Docker-based deployment
- Comprehensive API documentation

✅ **Recently Resolved Issues**
- UUID handling in database operations
- CORS configuration for frontend/backend communication
- API key authentication and management
- Frontend routing and navigation
- Database migration system

## 🔗 Quick Links

- **[🚀 Get Started](guides/getting-started.md)** - Start using AgentLogger in 5 minutes
- **[🔧 API Docs](api/index.md)** - Complete API reference with examples
- **[⚙️ Configuration](guides/configuration.md)** - Customize AgentLogger for your needs
- **[🏗️ Architecture](development/agent-architecture.md)** - Understand the system design
- **[🤝 Contributing](development/contributing.md)** - Help make AgentLogger better

## 🆘 Support & Community

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and API reference
- **Interactive API Docs**: Live testing at http://localhost/docs
- **FAQ**: Common questions and troubleshooting

---

**Ready to revolutionize your debugging workflow?** Start with our [Getting Started Guide](guides/getting-started.md) and experience the power of AI-assisted debugging! 