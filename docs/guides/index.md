# AgentLogger Documentation

Welcome to AgentLogger! This documentation will help you get started, deploy, and use AgentLogger effectively.

## 🚀 Quick Start Guides

### New to AgentLogger?
- **[Getting Started](getting-started.md)** - Complete setup guide with multiple deployment methods
- **[Installation Guide](installation.md)** - Comprehensive installation options (Docker, manual, cloud)

### How to Run AgentLogger

| Method | Time to Setup | Best For | Guide |
|--------|---------------|----------|-------|
| **🐳 Docker** | 2 minutes | Quick testing, production | [Getting Started](getting-started.md) |
| **💻 Manual** | 5 minutes | Development, learning | [Installation Guide](installation.md) |
| **☁️ Cloud** | 10 minutes | Production, scaling | [Deployment Guide](deployment.md) |
| **🖥️ CLI Only** | 1 minute | Command line usage | [CLI Guide](cli.md) |

## 📚 Core Documentation

### Usage & Configuration
- **[Configuration Guide](configuration.md)** - Environment variables and settings
- **[CLI Guide](cli.md)** - Command-line interface usage
- **[Core Functionality](core-functionality.md)** - Understanding AgentLogger's features

### Deployment & Production
- **[Deployment Guide](deployment.md)** - Production deployment on VPS, cloud platforms
- **[Vercel Deployment](vercel-deployment.md)** - Serverless deployment guide

### Support
- **[FAQ](faq.md)** - Common questions and troubleshooting

## 🎯 Quick Commands Reference

### Docker (Recommended)
```bash
# Get AgentLogger running in 30 seconds
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger
export GROQ_API_KEY="your_key"
docker-compose up -d
open http://localhost
```

### Manual Installation
```bash
# Backend + Frontend manual setup
git clone https://github.com/your-username/AgentLogger.git
cd AgentLogger

# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # Edit .env with GROQ_API_KEY
python scripts/init_db.py
uvicorn app.main:app --reload &

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

### CLI Only
```bash
# Just the CLI tool
cd AgentLogger/cli
pip install -e .
agent-logger configure --api-key YOUR_KEY
agent-logger analyze --file your_code.py
```

## 🌐 Access Points

Once running, AgentLogger is available at:

- **🏠 Main App**: http://localhost - Web interface
- **🎮 Playground**: http://localhost/playground - Interactive testing  
- **📊 Dashboard**: http://localhost/dashboard - Analytics
- **🔑 API Keys**: http://localhost/api-keys - Key management
- **📚 API Docs**: http://localhost/docs - Complete API reference
- **🔧 Backend**: http://localhost:8000 - Direct API access

## 🆘 Need Help?

1. **Quick Issues**: Check [FAQ](faq.md)
2. **Setup Problems**: See [Getting Started](getting-started.md) troubleshooting section
3. **Deployment**: Read [Deployment Guide](deployment.md)
4. **Development**: Visit [Development Documentation](../development/index.md)

## 📖 What's Next?

After getting AgentLogger running:

1. **🎮 Try the Playground** - Test with sample code
2. **🔑 Create API Keys** - Set up authentication
3. **📊 Explore Dashboard** - Monitor usage
4. **🛠️ Read API Docs** - Integrate with your tools
5. **🚀 Deploy to Production** - Scale your usage

Choose your path and get started with AI-powered debugging! 🎉 