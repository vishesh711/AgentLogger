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

## 🏗️ System Architecture

AgentLogger features a sophisticated **server-side / client-side** architecture with clear separation of concerns:

### **Client-Side (React Frontend)**
- **Port**: 5173 (development) / 80 (production)
- **Technology**: React 18, TypeScript, Vite, TailwindCSS
- **Responsibilities**: UI/UX, authentication context, API communication, state management
- **Authentication**: JWT token management, protected routes

### **Server-Side (FastAPI Backend)**  
- **Port**: 8000
- **Technology**: Python, FastAPI, PostgreSQL, Agent System
- **Responsibilities**: Business logic, AI processing, database operations, authentication
- **Authentication**: JWT validation, API key management

### **Communication Flow**
```
Frontend (React) ←→ HTTP API Calls ←→ Backend (FastAPI) ←→ Agent System ←→ Database
```

**📚 For complete architectural details, see:**
- **[🏗️ Architecture Guide](ARCHITECTURE_GUIDE.md)** - **Complete architectural navigation hub**
- **[Server-Client Architecture](api/SERVER_CLIENT_ARCHITECTURE.md)** - Complete architectural overview
- **[API Usage Examples](api/API_USAGE_EXAMPLES.md)** - Practical implementation examples
- **[Agent Architecture](development/agent-architecture.md)** - AI agent system design

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
- **[Server-Client Architecture](api/SERVER_CLIENT_ARCHITECTURE.md)** - 🆕 **Detailed system architecture**
- **[API Usage Examples](api/API_USAGE_EXAMPLES.md)** - 🆕 **Real-world implementation examples**
- **[Code Analysis](api/analyze.md)** - Code analysis endpoints
- **[Error Explanation](api/explain.md)** - Error explanation endpoints
- **[Fix Generation](api/fix.md)** - Code fixing endpoints
- **[Patch Creation](api/patch.md)** - Patch generation endpoints

### 🛠️ Development
- **[Development Setup](development/development-setup.md)** - Local development environment
- **[Agent Architecture](development/agent-architecture.md)** - System design and architecture
- **[Frontend Development](development/frontend.md)** - React frontend development
- **[Project Structure](development/project-structure.md)** - Codebase organization
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
- **Backend API**: http://localhost:8000 (development)
- **Frontend Dev Server**: http://localhost:5173 (development)

### 4. Test the System
Navigate to the Playground and paste some buggy code to see AgentLogger in action!

## 🔐 Authentication & API Access

### **Web Interface Authentication**
- **Method**: JWT tokens
- **Flow**: Login → Store token → Include in API requests
- **Management**: Built-in user registration/login system

### **Programmatic API Access**
- **Method**: API keys
- **Management**: Create/delete via web interface or API
- **Usage**: Include `Authorization: Bearer {jwt_token}` header

### **Quick API Test**
```bash
# Health check (no auth required)
curl http://localhost:8000/health

# Quick code analysis (requires JWT token)
curl -X POST http://localhost:8000/api/v1/analyze/quick \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

## 🏗️ System Architecture Details

AgentLogger uses a sophisticated multi-agent architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT SIDE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  React App (Port 5173/80)                                                  │
│  ├── Authentication Context (JWT Management)                               │
│  ├── API Client (lib/api.ts)                                              │
│  ├── Protected Routes                                                      │
│  └── UI Components (Dashboard, Playground, API Keys)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                  HTTP API Calls
                                       │
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER SIDE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  FastAPI Backend (Port 8000)                                              │
│  ├── API Endpoints (/api/v1/*)                                           │
│  ├── Authentication Middleware (JWT + API Key)                            │
│  ├── Agent System (Coordinator, Analyzer, Fix Generator)                  │
│  ├── Database Services (PostgreSQL)                                       │
│  └── Background Tasks (Async Processing)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **Key Components**

1. **Frontend (React/TypeScript)**
   - Authentication management
   - Real-time UI updates
   - Protected route navigation
   - API request handling

2. **Backend (FastAPI/Python)**
   - JWT token validation
   - API key management
   - Agent system coordination
   - Database operations

3. **Agent System**
   - **Coordinator Agent**: Orchestrates workflows
   - **Analyzer Agent**: Code analysis and issue detection
   - **Fix Generator Agent**: AI-powered fix generation

4. **Database Layer**
   - User management
   - API key storage
   - Analysis results
   - Session tracking

## 📊 Technology Stack

### **Frontend Stack**
- **React 18**: Modern UI framework
- **TypeScript**: Type safety and better DX
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first styling
- **shadcn/ui**: Component library

### **Backend Stack**
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **PostgreSQL**: Primary database

### **AI & Integration**
- **Groq API**: Large Language Model integration
- **Multi-Agent System**: Specialized AI agents
- **Background Tasks**: Asynchronous processing
- **Docker**: Containerization and deployment

## 🎮 Interactive Examples

### Web Interface
1. Visit http://localhost after setup
2. Register a new account or login
3. Go to the "Playground" page
4. Paste buggy code and see instant analysis
5. Generate fixes and explanations

### API Usage
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use JWT token for API calls
curl -X POST http://localhost:8000/api/v1/analyze/quick \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

## 📊 Current Status

✅ **Fully Functional Features**
- Multi-agent analysis workflow
- Complete authentication system (JWT + API keys)
- Code analysis for Python and JavaScript
- Error explanation with multiple detail levels
- Automated fix generation
- API key management system
- Modern React web interface
- Docker-based deployment
- Comprehensive API documentation
- Server-client architecture with clear separation

✅ **Recently Resolved Issues**
- Frontend-backend integration completed
- Authentication system fully implemented
- API client properly configured
- Protected routes working
- Database schema properly migrated
- Agent system integration operational

## 🔗 Quick Navigation

### **🚀 Get Started**
- **[Quick Start Guide](guides/getting-started.md)** - Start using AgentLogger in 5 minutes

### **🏗️ Architecture**
- **[🏗️ Architecture Guide](ARCHITECTURE_GUIDE.md)** - **Complete architectural navigation hub**
- **[Server-Client Architecture](api/SERVER_CLIENT_ARCHITECTURE.md)** - Complete system design
- **[API Usage Examples](api/API_USAGE_EXAMPLES.md)** - Practical implementation examples
- **[Agent Architecture](development/agent-architecture.md)** - AI agent system design

### **🔧 API Documentation**
- **[API Overview](api/index.md)** - Complete API reference with examples
- **[Interactive API Docs](http://localhost/docs)** - Live API testing interface

### **⚙️ Configuration & Development**
- **[Configuration Guide](guides/configuration.md)** - Customize AgentLogger for your needs
- **[Development Setup](development/development-setup.md)** - Local development environment
- **[Contributing Guide](development/contributing.md)** - Help make AgentLogger better

## 🆘 Support & Community

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and API reference
- **Interactive API Docs**: Live testing at http://localhost/docs
- **Architecture Docs**: Detailed system design documentation
- **FAQ**: Common questions and troubleshooting

---

**Ready to revolutionize your debugging workflow?** Start with our [Getting Started Guide](guides/getting-started.md) and experience the power of AI-assisted debugging with clear server-client architecture! 