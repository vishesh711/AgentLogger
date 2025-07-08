# AgentLogger - Quick Start Reference

⚡ Get AgentLogger running in under 2 minutes with any of these methods!

## 🐳 Docker (Recommended) - 30 seconds

```bash
git clone https://github.com/your-username/AgentLogger.git && cd AgentLogger
export GROQ_API_KEY="your_groq_key_from_console.groq.com"
docker-compose up -d
open http://localhost
```

## 💻 Manual Setup - 3 minutes

```bash
# Backend
git clone https://github.com/your-username/AgentLogger.git && cd AgentLogger
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # Edit with GROQ_API_KEY
python scripts/init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

## ☁️ Cloud Deployment

### Vercel
```bash
cd frontend && vercel --prod
```

### VPS/Server
```bash
git clone https://github.com/your-username/AgentLogger.git && cd AgentLogger
cp env.example .env  # Edit with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## 🖥️ CLI Only

```bash
cd AgentLogger/cli
pip install -e .
agent-logger configure --api-key YOUR_KEY
agent-logger analyze --file your_code.py
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| 🏠 **Main App** | http://localhost | Beautiful web interface |
| 🎮 **Playground** | http://localhost/playground | Test code analysis |
| 📊 **Dashboard** | http://localhost/dashboard | Usage analytics |
| 🔑 **API Keys** | http://localhost/api-keys | Manage authentication |
| 📚 **API Docs** | http://localhost/docs | API reference |

## ⚡ Quick Test

```bash
# Test via API
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU" \
  -d '{"code": "print(hello world)", "language": "python"}'

# Test via web interface
# Go to http://localhost/playground and paste buggy code
```

## 🆘 Troubleshooting

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Reset everything
docker-compose down && docker system prune -f && docker-compose up -d
```

## 📚 Full Documentation

- **[Complete Setup Guide](docs/guides/getting-started.md)**
- **[Installation Options](docs/guides/installation.md)**
- **[Deployment Guide](docs/guides/deployment.md)**
- **[API Documentation](docs/api/index.md)**
- **[Development Setup](docs/development/development-setup.md)**

---

🎉 **That's it!** Choose your method and start debugging with AI assistance!
