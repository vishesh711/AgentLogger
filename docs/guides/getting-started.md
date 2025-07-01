# Getting Started with AgentLogger

This guide will help you get AgentLogger up and running quickly. AgentLogger is a production-ready AI-powered debugging tool with a modern web interface and robust API.

## 🚀 Quick Start (30 seconds)

The absolute fastest way to get AgentLogger running:

```bash
# 1. Clone and enter directory
git clone https://github.com/your-username/AgentLogger.git && cd AgentLogger

# 2. Set your Groq API key (get free at console.groq.com)
export GROQ_API_KEY="your_groq_api_key_here"

# 3. Launch everything with Docker
docker-compose up -d

# 4. Open in browser
open http://localhost  # macOS
# or visit http://localhost manually
```

That's it! 🎉 AgentLogger is now running with:
- ✅ Beautiful web interface at http://localhost
- ✅ Complete API at http://localhost/api/v1
- ✅ Interactive playground and documentation

## 📋 Prerequisites

### Essential Requirements
- **Git** - For cloning the repository
- **Groq API Key** - Get one free at [console.groq.com](https://console.groq.com)

### Choose Your Installation Method

| Method | Requirements | Best For |
|--------|--------------|----------|
| **🐳 Docker** (Recommended) | Docker & Docker Compose | Quick setup, consistent environment |
| **💻 Manual** | Python 3.11+, Node.js 18+ | Development, customization |
| **☁️ Cloud** | Cloud account | Production deployment |

## Method 1: Docker Deployment (Recommended) 🐳

### Step 1: Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy your API key (it starts with `gsk_...`)

⚠️ **Important**: Keep your API key secure and never commit it to version control.

### Step 2: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Option 1: Export as environment variable (recommended)
export GROQ_API_KEY="your_groq_api_key_here"

# Option 2: Create .env file
cp env.example .env
# Edit .env and set GROQ_API_KEY=your_actual_key
```

### Step 3: Launch the Application

```bash
# Start all services (this may take a few minutes on first run)
docker-compose up -d

# Check that all services are running
docker-compose ps

# View logs if needed
docker-compose logs -f
```

**Services Started:**
- ✅ Frontend (React) - Port 8080
- ✅ Backend (FastAPI) - Port 8000  
- ✅ Database (SQLite) - Embedded
- ✅ Nginx Proxy - Port 80

### Step 4: Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Main App** | http://localhost | Beautiful web interface |
| 🎮 **Playground** | http://localhost/playground | Interactive testing |
| 📊 **Dashboard** | http://localhost/dashboard | Analytics & management |
| 🔑 **API Keys** | http://localhost/api-keys | Key management |
| 📚 **API Docs** | http://localhost/docs | Complete API reference |
| 🔧 **Backend Direct** | http://localhost:8000 | Direct API access |

## Method 2: Manual Installation 💻

### Full Manual Setup

**Best for**: Development, learning the system, customization

```bash
# 1. Clone repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# 2. Backend Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Environment Configuration
cp env.example .env
# Edit .env file and set GROQ_API_KEY=your_key

# 4. Database Setup
python scripts/init_db.py

# 5. Start Backend (in one terminal)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Frontend Setup (in another terminal)
cd frontend
npm install
npm run dev

# 7. Access Application
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

### Backend Only Setup

**Best for**: API-only usage, custom frontend, CLI development

```bash
# Quick backend setup
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp env.example .env
# Set GROQ_API_KEY in .env file

# Initialize database
python scripts/init_db.py

# Start API server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test API
curl http://localhost:8000/api/v1/health/
```

## Method 3: CLI Installation 🖥️

### Install and Use CLI

```bash
# Install AgentLogger CLI
cd cli
pip install -e .

# Configure with your API key
agent-logger configure --api-key YOUR_API_KEY --api-url http://localhost:8000/api/v1

# Test CLI
agent-logger analyze --file test_file.py
agent-logger explain --code "print(hello world)" --language python
```

## 🔑 API Key Management

AgentLogger includes a comprehensive API key management system accessible through the web interface.

### Default API Key
For immediate testing, use this pre-configured key:
```
QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU
```

### Create Your Own API Keys
1. Navigate to http://localhost/api-keys
2. Click **"Create API Key"**
3. Enter a descriptive name (e.g., "Development Key")
4. Copy the generated key immediately (it's only shown once)
5. Use the key in your API requests

### Using API Keys

**Web Interface**: Keys are automatically used when logged in

**API Requests**: Include in headers:
```bash
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

**CLI**: Configure once with `agent-logger configure`

## 🧪 Test the System

### Via Web Interface
1. Go to http://localhost
2. Navigate to **"Playground"**
3. Paste buggy code:
   ```python
   # Example buggy Python code
   print(hello world)
   for i in range(5
       print(i)
   ```
4. Select language: **Python**
5. Click **"Analyze"**
6. View the AI-powered analysis and suggested fixes

### Via API
```bash
# Test health endpoint
curl http://localhost/api/v1/health/

# Test analysis endpoint
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{
    "code": "print(hello world)",
    "language": "python"
  }' | jq '.'

# Test explanation endpoint  
curl -X POST http://localhost/api/v1/explain \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python"
  }' | jq '.'

# Test fix generation
curl -X POST http://localhost/api/v1/fix \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{
    "code": "print(hello world)",
    "language": "python",
    "errors": ["SyntaxError: invalid syntax"]
  }' | jq '.'
```

## 🌐 Explore the Interface

### 🏠 Home Page
- Welcome screen with overview
- Quick action buttons
- System status indicators

### 🎮 Playground
- **Interactive Code Editor**: Paste or type code
- **Language Selection**: Python, JavaScript, Java, etc.
- **Real-time Analysis**: Get instant feedback
- **Fix Generation**: AI-powered code corrections
- **Error Explanation**: Detailed error breakdowns

### 📊 Dashboard  
- **Usage Analytics**: API call statistics
- **Recent Activity**: Latest analyses and fixes
- **Performance Metrics**: Response times and success rates
- **API Key Usage**: Track usage by key

### 🔑 API Keys
- **Create Keys**: Generate new API keys with custom names
- **View Keys**: See all your active keys (values hidden for security)
- **Copy Keys**: One-click copy to clipboard
- **Delete Keys**: Remove unused or compromised keys
- **Usage Stats**: See which keys are being used

### 📚 Documentation
- **API Reference**: Complete endpoint documentation
- **Code Examples**: Copy-paste examples in multiple languages
- **Authentication**: How to use API keys
- **Rate Limits**: Understanding usage limits

## 🎯 Common Use Cases

### 1. Quick Syntax Check
```python
# Paste this in Playground to see syntax error detection
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2  # Missing closing parenthesis
```

### 2. Debug Runtime Errors
```python
# Example with logic errors
def divide_numbers(a, b):
    return a / b  # Will fail with ZeroDivisionError

result = divide_numbers(10, 0)
```

### 3. Code Quality Analysis
```python
# Example with style and performance issues
def bad_function():
    numbers = []
    for i in range(1000):
        numbers.append(i)
    return numbers
```

### 4. API Integration
```javascript
// Example: Integrating AgentLogger into your IDE or editor
async function analyzeCode(code, language) {
    const response = await fetch('http://localhost/api/v1/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': 'your-api-key'
        },
        body: JSON.stringify({ code, language })
    });
    
    const result = await response.json();
    return result;
}
```

## ✅ Verification Steps

### 1. Check All Services
```bash
# Docker method
docker-compose ps

# Manual method
curl http://localhost:8000/api/v1/health/  # Backend health
curl http://localhost:8080  # Frontend (if running manually)
curl http://localhost  # Main app (Docker)
```

### 2. Test Core Functionality
1. **Health Check**: Visit http://localhost/api/v1/health/ 
2. **Web Interface**: Navigate through all pages
3. **API Key Creation**: Create a new key in the web interface
4. **Code Analysis**: Test the playground with sample code
5. **API Access**: Make direct API calls

### 3. Verify Database
```bash
# Check if database was created and populated
# Docker method
docker-compose exec backend python -c "
from app.core.db import SessionLocal
from app.models.db.user import User
session = SessionLocal()
users = session.query(User).all()
print(f'Found {len(users)} users in database')
session.close()
"
```

## 🛠️ Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the ports
lsof -i :8000  # Backend
lsof -i :8080  # Frontend  
lsof -i :80    # Nginx

# Kill processes if needed
sudo kill -9 PID_NUMBER
```

**Docker Issues:**
```bash
# Reset Docker completely
docker-compose down
docker system prune -f
docker-compose pull
docker-compose up -d --build
```

**Environment Variables Not Set:**
```bash
# Check if Groq API key is set
echo $GROQ_API_KEY
cat .env | grep GROQ_API_KEY

# If empty, set it:
export GROQ_API_KEY="your_key_here"
```

**Database Connection Issues:**
```bash
# Reset database (development only)
rm -f agentlogger.db  # SQLite file
python scripts/init_db.py  # Recreate
```

**Frontend Build Issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Getting Help

**Can't Access Web Interface?**
- Check if all services are running: `docker-compose ps`
- Try different browsers or incognito mode
- Check firewall settings

**API Returning Errors?**
- Verify your Groq API key is valid
- Check API key permissions in the web interface
- Look at backend logs: `docker-compose logs backend`

**Slow Performance?**
- Check your internet connection (Groq API requires internet)
- Monitor system resources: `docker stats`
- Try restarting services: `docker-compose restart`

## 📚 Next Steps

After successful setup:

1. **🎮 Try the Playground** - Test with your own code
2. **🔑 Create API Keys** - Set up authentication for your projects
3. **📖 Read the Docs** - Explore full API capabilities
4. **🛠️ Set Up Development** - If you want to contribute or customize
5. **🚀 Deploy to Production** - See the deployment guide for cloud setup

### Recommended Learning Path

1. **Start with Web Interface** - Get familiar with all features
2. **Try API Calls** - Use curl or Postman to test endpoints
3. **Install CLI** - For command-line usage
4. **Read Architecture Docs** - Understand how it works internally
5. **Contribute** - Help improve AgentLogger

## 🆘 Need More Help?

- **📚 Full Documentation**: Check all guides in `docs/` directory
- **🐛 Found a Bug?**: Open an issue on GitHub
- **💬 Questions?**: Join our GitHub Discussions
- **📧 Contact**: Reach out to the development team
- **🔧 Advanced Setup**: See `docs/guides/deployment.md` for production deployment

Welcome to AgentLogger! 🎉 Start debugging with AI-powered assistance! 