# Getting Started with AgentLogger

This guide will help you get AgentLogger up and running quickly. AgentLogger is a production-ready AI-powered debugging tool with a modern web interface and robust API.

## Prerequisites

Before you begin, ensure you have:

- **Docker and Docker Compose** installed on your system
- **Groq API Key** - Get one free at [console.groq.com](https://console.groq.com)
- **Git** for cloning the repository

## Step 1: Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy your API key (it starts with `gsk_...`)

⚠️ **Important**: Keep your API key secure and never commit it to version control.

## Step 2: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Option 1: Set API key in docker-compose.yml
# Edit docker-compose.yml and replace the GROQ_API_KEY placeholder

# Option 2: Export as environment variable (recommended)
export GROQ_API_KEY="your_groq_api_key_here"
```

## Step 3: Launch the Application

```bash
# Start all services (this may take a few minutes on first run)
docker-compose up -d

# Check that all services are running
docker-compose ps

# View logs if needed
docker-compose logs -f
```

You should see:
- ✅ Frontend service running on port 8082
- ✅ Backend service running on port 8000  
- ✅ Database service running on port 5432
- ✅ Nginx proxy running on port 80

## Step 4: Access the Application

### Web Interface (Recommended)
- **Main Application**: http://localhost
- **API Documentation**: http://localhost/docs

### Direct Service Access
- **Frontend**: http://localhost:8082 (React development server)
- **Backend**: http://localhost:8000 (FastAPI server)

## Step 5: API Key Management

AgentLogger includes a comprehensive API key management system:

### Default API Key
For immediate testing, use this pre-configured key:
```
QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU
```

### Create Your Own API Keys
1. Navigate to http://localhost
2. Click **"API Keys"** in the navigation bar
3. Click **"Create API Key"**
4. Enter a name (e.g., "My Test Key")
5. Copy the generated key immediately (it's only shown once)

### Using API Keys
Include your API key in all requests:
```bash
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{"code": "print(hello world)", "language": "python"}'
```

## Step 6: Test the System

### Via Web Interface
1. Go to http://localhost
2. Click **"Playground"** in the navigation
3. Paste some buggy code:
   ```python
   print(hello world)
   for i in range(5
       print(i)
   ```
4. Select language: **Python**
5. Click **"Analyze"**
6. View the analysis results and suggested fixes

### Via API
```bash
# Test the analysis endpoint
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{
    "code": "print(hello world)",
    "language": "python"
  }' | jq '.'

# Test the explanation endpoint
curl -X POST http://localhost/api/v1/explain \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{
    "code": "print(hello world)",
    "traceback": "SyntaxError: invalid syntax",
    "language": "python"
  }' | jq '.'
```

## Navigation Guide

AgentLogger's web interface includes several key pages:

### 🏠 **Home Page** (/)
- Landing page with overview
- Links to key features

### 🎮 **Playground** (/playground)
- Interactive code analysis
- Real-time syntax checking
- Fix generation and explanation

### 📊 **Dashboard** (/dashboard)
- Analysis history
- Recent activities
- Quick statistics

### 🔑 **API Keys** (/api-keys)
- Create new API keys
- View existing keys
- Delete unused keys
- Copy keys to clipboard

### 📚 **Documentation** (/docs)
- API reference
- Usage guides
- Examples

### 🔐 **Sign In** (/signin)
- Authentication page
- GitHub OAuth integration

## Common Use Cases

### 1. Quick Code Check
```python
# Paste this in the Playground
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2
```

### 2. Error Analysis
```python
# Code with multiple issues
import os
print("Hello World"
for i in range(10)
    print(i
```

### 3. API Integration
```javascript
// Example: Integrating with your IDE
fetch('http://localhost/api/v1/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify({
    code: userCode,
    language: 'python'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Troubleshooting

### Services Not Starting
```bash
# Check Docker is running
docker --version
docker-compose --version

# View service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### API Key Issues
- Ensure your Groq API key is valid and has sufficient credits
- Check that the key is properly set in environment variables
- Verify the key format (should start with `gsk_`)

### CORS Errors
The application is configured for common development ports. If you're running on different ports, check `app/main.py` CORS configuration.

### Database Issues
```bash
# Reset database if needed
docker-compose down -v
docker-compose up -d

# Check database status
docker-compose exec db psql -U postgres -d agentlogger -c "\dt"
```

## Next Steps

1. **Explore the API**: Visit http://localhost/docs for interactive API documentation
2. **Check Configuration**: See [Configuration Guide](configuration.md) for advanced settings
3. **Development Setup**: See [Development Setup](../development/development-setup.md) for local development
4. **Agent Architecture**: Learn about the system design in [Agent Architecture](../development/agent-architecture.md)

## Support

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Documentation**: Check other guides in the `docs/` directory
- **FAQ**: See [FAQ](faq.md) for common questions

## What's Next?

Now that you have AgentLogger running:

1. Try analyzing different types of code issues
2. Explore the API endpoints
3. Create and manage your API keys
4. Check out the agent workflow in action
5. Consider contributing to the project

Happy debugging! 🐛✨ 