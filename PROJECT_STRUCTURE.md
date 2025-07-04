# AgentLogger Project Structure

This document provides a comprehensive overview of the organized AgentLogger codebase structure.

## 📁 Root Directory Structure

```
AgentLogger/
├── 📁 app/                    # Backend application (FastAPI)
├── 📁 frontend/              # React frontend application
├── 📁 deployment/            # Docker and deployment files
├── 📁 config/                # Configuration files
├── 📁 scripts/               # Utility scripts
├── 📁 docs/                  # Documentation
├── 📁 database/              # Database files
├── 📁 logs/                  # Application logs
├── 📁 assets/                # Static assets
├── 📁 tests/                 # Test suite
├── 📁 alembic/               # Database migrations
├── 📁 nginx/                 # Nginx configuration
├── 📁 cli/                   # Command-line interface
├── 📁 api/                   # Legacy API directory
├── 📁 .github/               # GitHub Actions workflows
├── 📄 README.md              # Main project documentation
├── 📄 PROJECT_STRUCTURE.md   # This file
├── 📄 LICENSE                # MIT License
├── 📄 requirements.txt       # Python dependencies
├── 📄 pytest.ini            # Pytest configuration
├── 📄 mypy.ini              # MyPy configuration
├── 📄 alembic.ini           # Alembic configuration
├── 📄 Makefile              # Build automation
└── 📄 .gitignore            # Git ignore rules
```

## 🔧 Backend Application (`app/`)

```
app/
├── 📁 agents/                # Multi-agent system
│   ├── __init__.py
│   ├── agent_system.py      # Main agent orchestrator
│   ├── base_agent.py        # Base agent class
│   ├── coordinator_agent.py # Coordinates other agents
│   ├── analyzer_agent.py    # Code analysis agent
│   └── fix_generator_agent.py # Code fixing agent
├── 📁 api/                   # API endpoints and routing
│   ├── __init__.py
│   ├── middleware/          # Custom middleware
│   └── v1/                  # API version 1
│       ├── __init__.py
│       ├── router.py        # Main API router
│       └── endpoints/       # API endpoints
│           ├── __init__.py
│           ├── analyze.py   # Code analysis endpoint
│           ├── fix.py       # Code fixing endpoint
│           ├── explain.py   # Code explanation endpoint
│           ├── auth.py      # Authentication endpoints
│           ├── users.py     # User management
│           ├── api_keys.py  # API key management
│           ├── health.py    # Health check endpoint
│           └── github.py    # GitHub integration
├── 📁 core/                  # Core configuration and utilities
│   ├── __init__.py
│   ├── config.py            # Application configuration
│   ├── db.py                # Database setup
│   ├── dependencies.py      # FastAPI dependencies
│   └── middleware.py        # Custom middleware
├── 📁 models/                # Database models and schemas
│   ├── __init__.py
│   ├── db/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py          # Base model
│   │   ├── user.py          # User model
│   │   ├── api_key.py       # API key model
│   │   ├── analysis.py      # Analysis model
│   │   ├── fix.py           # Fix model
│   │   └── github.py        # GitHub model
│   └── schemas/             # Pydantic schemas
│       ├── __init__.py
│       ├── user.py          # User schemas
│       ├── api_key.py       # API key schemas
│       ├── analysis.py      # Analysis schemas
│       ├── fix.py           # Fix schemas
│       └── patch.py         # Patch schemas
├── 📁 services/              # Business logic services
│   ├── __init__.py
│   ├── ai/                  # AI/LLM services
│   │   ├── __init__.py
│   │   └── groq_client.py   # Groq LLM client
│   ├── analysis_service.py  # Code analysis service
│   ├── fix_service.py       # Code fixing service
│   ├── user_service.py      # User management service
│   ├── api_key_service.py   # API key service
│   ├── github_service.py    # GitHub integration service
│   └── monitoring_service.py # Analytics service
├── 📁 utils/                 # Utility functions
│   ├── __init__.py
│   ├── parsing/             # Code parsing utilities
│   │   ├── __init__.py
│   │   ├── base_parser.py   # Base parser
│   │   ├── python_parser.py # Python parser
│   │   ├── javascript_parser.py # JavaScript parser
│   │   └── parser_factory.py # Parser factory
│   └── sandbox/             # Code execution sandbox
│       ├── __init__.py
│       └── code_runner.py   # Safe code execution
└── 📄 main.py               # FastAPI application entry point
```

## 🎨 Frontend Application (`frontend/`)

```
frontend/
├── 📁 src/                   # Source code
│   ├── 📁 components/        # React components
│   │   ├── 📁 ui/           # Reusable UI components
│   │   ├── Navigation.tsx   # Navigation component
│   │   └── ProtectedRoute.tsx # Route protection
│   ├── 📁 pages/            # Page components
│   │   ├── Index.tsx        # Home page
│   │   ├── Dashboard.tsx    # Dashboard page
│   │   ├── Playground.tsx   # Code playground
│   │   ├── ApiKeys.tsx      # API key management
│   │   ├── SignIn.tsx       # Sign in page
│   │   ├── SignUp.tsx       # Sign up page
│   │   ├── Docs.tsx         # Documentation page
│   │   └── NotFound.tsx     # 404 page
│   ├── 📁 contexts/         # React contexts
│   │   └── AuthContext.tsx  # Authentication context
│   ├── 📁 hooks/            # Custom React hooks
│   │   ├── use-mobile.tsx   # Mobile detection hook
│   │   └── use-toast.ts     # Toast notification hook
│   ├── 📁 lib/              # Utility libraries
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # App entry point
│   ├── index.css            # Global styles
│   └── App.css              # App-specific styles
├── 📁 public/               # Static assets
│   ├── favicon.ico          # Favicon
│   ├── logo.png             # Logo
│   └── robots.txt           # SEO robots file
├── 📄 package.json          # Node.js dependencies
├── 📄 vite.config.ts        # Vite configuration
├── 📄 tailwind.config.ts    # Tailwind CSS configuration
├── 📄 tsconfig.json         # TypeScript configuration
└── 📄 Dockerfile            # Frontend Docker configuration
```

## 🐳 Deployment (`deployment/`)

```
deployment/
├── 📄 Dockerfile            # Development Docker image
├── 📄 Dockerfile.prod       # Production Docker image
├── 📄 docker-compose.yml    # Development Docker Compose
└── 📄 docker-compose.prod.yml # Production Docker Compose
```

## ⚙️ Configuration (`config/`)

```
config/
├── 📄 env.example           # Environment variables template
└── 📄 requirements-vercel.txt # Vercel-specific requirements
```

## 📜 Scripts (`scripts/`)

```
scripts/
├── 📄 start_app.sh          # Main application startup script
├── 📄 run.sh                # Development server script
├── 📄 setup.sh              # Initial setup script
├── 📄 test.sh               # Test runner script
├── 📄 run_frontend.sh       # Frontend development script
├── 📄 backup.sh             # Database backup script
├── 📄 init_db.py            # Database initialization
└── 📄 generate_api_key.py   # API key generation utility
```

## 📚 Documentation (`docs/`)

```
docs/
├── 📁 setup/                # Setup guides
│   ├── 📄 DATABASE_SETUP.md # Database setup guide
│   ├── 📄 DOCKER_SETUP.md   # Docker setup guide
│   ├── 📄 QUICK_START.md    # Quick start guide
│   └── 📄 FRONTEND_BACKEND_CONNECTION.md # Integration guide
├── 📁 deployment/           # Deployment guides
│   ├── 📄 deploy-vercel.sh  # Vercel deployment script
│   └── 📄 vercel.json       # Vercel configuration
├── 📁 development/          # Development documentation
│   ├── 📄 CHANGES.md        # Change log
│   ├── 📄 FIXES_APPLIED.md  # Applied fixes log
│   └── 📄 AgentLogger_Resume_Description.md # Project description
├── 📁 guides/               # User guides
├── 📁 api/                  # API documentation
├── 📁 assets/               # Documentation assets
└── 📄 index.md              # Documentation index
```

## 🗄️ Database (`database/`)

```
database/
├── 📄 agentlogger.db        # SQLite database (development)
├── 📄 test_agentlogger.db   # Test database
└── 📄 test.db               # Additional test database
```

## 📊 Logs (`logs/`)

```
logs/
├── 📄 backend.log           # Backend application logs
└── 📄 .coverage             # Test coverage data
```

## 🎨 Assets (`assets/`)

```
assets/
├── 📄 Mainpage.png          # Main page screenshot
├── 📄 test_frontend_backend.html # Test file
├── 📄 setup_groq_key.txt    # Groq API key setup guide
└── 📄 .api_key              # API key file
```

## 🧪 Tests (`tests/`)

```
tests/
├── 📁 integration/          # Integration tests
│   ├── 📄 test_agent_debug.py # Agent debugging tests
│   ├── 📄 test_agent_logger.py # Agent logger tests
│   ├── 📄 test_buggy_code.py # Buggy code tests
│   └── 📄 test_github_pr.py # GitHub PR tests
├── 📄 conftest.py           # Pytest configuration
├── 📄 test_health.py        # Health endpoint tests
├── 📄 test_auth.py          # Authentication tests
├── 📄 test_api_keys.py      # API key tests
└── 📄 __init__.py
```

## 🔄 Database Migrations (`alembic/`)

```
alembic/
├── 📁 versions/             # Migration files
│   ├── 📄 83870bd3255c_initial_migration.py
│   ├── 📄 make_password_nullable_oauth.py
│   ├── 📄 make_updated_at_nullable.py
│   ├── 📄 update_api_key_user_id.py
│   └── 📄 update_user_model.py
├── 📄 env.py                # Alembic environment
├── 📄 script.py.mako        # Migration template
└── 📄 alembic.ini           # Alembic configuration
```

## 🌐 Nginx (`nginx/`)

```
nginx/
├── 📁 conf.d/               # Nginx configuration files
│   └── 📄 default.conf      # Default server configuration
└── 📁 prod/                 # Production configuration
    └── 📄 default.conf      # Production server configuration
```

## 💻 CLI (`cli/`)

```
cli/
├── 📄 __init__.py
├── 📄 agent_logger_cli.py   # Main CLI application
├── 📄 setup.py              # CLI package setup
└── 📄 test_buggy_code.py    # CLI test file
```

## 🔧 GitHub Actions (`.github/`)

```
.github/
└── 📁 workflows/            # CI/CD workflows
    ├── 📄 ci-cd.yml         # Main CI/CD pipeline
    └── 📄 cli-package.yml   # CLI package workflow
```

## 📋 Key Files in Root

- **`README.md`**: Main project documentation and quick start guide
- **`PROJECT_STRUCTURE.md`**: This file - comprehensive structure overview
- **`requirements.txt`**: Python dependencies for the backend
- **`pytest.ini`**: Pytest configuration for testing
- **`mypy.ini`**: MyPy configuration for type checking
- **`alembic.ini`**: Alembic configuration for database migrations
- **`Makefile`**: Build automation and common tasks
- **`.gitignore`**: Git ignore rules for the project
- **`LICENSE`**: MIT License for the project

## 🎯 Benefits of This Organization

1. **Clear Separation**: Each directory has a specific purpose
2. **Easy Navigation**: Developers can quickly find what they need
3. **Scalable Structure**: Easy to add new features and components
4. **Deployment Ready**: Clear separation of deployment configurations
5. **Documentation**: Well-organized documentation structure
6. **Testing**: Dedicated test structure with clear organization
7. **Configuration**: Centralized configuration management
8. **Scripts**: Utility scripts for common tasks

## 🔄 Migration Notes

If you're migrating from the old structure:
1. Update any hardcoded paths in your code
2. Update Docker Compose files to use new paths
3. Update CI/CD workflows to reference new locations
4. Update documentation links
5. Test all functionality to ensure paths work correctly 