# AgentLogger - AI-Powered Debugging Tool

AgentLogger is an advanced debugging tool that uses AI-powered agents to analyze, explain, and fix code issues automatically. The system leverages a multi-agent architecture to provide comprehensive debugging assistance.

## Core Concept

The core of AgentLogger is its agent-based architecture:

1. **Analyzer Agent**: Examines code for bugs, issues, and potential improvements
2. **Fix Generator Agent**: Creates fixes for identified issues
3. **Coordinator Agent**: Orchestrates the workflow between agents

These agents work together through a message-passing system to provide a complete debugging experience.

## Key Features

- **Code Analysis**: Identify bugs, anti-patterns, and performance issues in your code
- **Error Explanation**: Get multi-level explanations of error messages (simple, detailed, technical)
- **Automated Fixes**: Generate patches and fixes for common code issues
- **GitHub Integration**: Analyze PRs and issues directly from GitHub
- **Sandbox Execution**: Test code in a safe environment to verify issues
- **Multi-language Support**: Works with Python, JavaScript, and more

## Architecture

The system uses a multi-agent architecture where specialized AI agents communicate to solve debugging tasks:

```
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
│                                         │
└─────────────────┬───────────────────────┘
                  │
                  │
                  ▼
┌─────────────────────────────────────────┐
│                                         │
│               User Interface            │
│                                         │
└─────────────────────────────────────────┘
```

## Getting Started

1. Clone the repository
2. **Set your Groq API key**
   - Open `docker-compose.yml`
   - Replace the placeholder in `GROQ_API_KEY=` with your key (`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`)
   - (Optional) Alternatively, export `GROQ_API_KEY` in your shell before running Docker Compose
3. Run `docker-compose up -d` to start the application (frontend, backend, and database)
4. Access the web UI at `http://localhost` (served by nginx)
5. API documentation is available at `http://localhost/docs` (proxied by nginx)

> **Note**: If you prefer to bypass nginx you can reach the backend directly at `http://localhost:8000` but the docs at `/docs` will then require the `X-API-Key` header.

## Configuration

Key environment variables (see `docs/guides/configuration.md` for full list):

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq LLM API key | **Required** |
| `GROQ_MODEL` | LLM model to use | `llama3-70b-8192` |
| `DATABASE_URL` | Database connection string | `postgresql://postgres:postgres@db:5432/agentlogger` |

These can be set in the `docker-compose.yml`, a local `.env` file, or exported in your shell session.

## API Documentation

The API provides endpoints for:

- `/api/v1/analyze` - Analyze code for issues
- `/api/v1/explain` - Explain error messages
- `/api/v1/fix` - Generate fixes for issues
- `/api/v1/patch` - Create patches for code

Base URL when running with Docker Compose:
```
http://localhost/api/v1
```

For detailed API documentation, visit `http://localhost/docs` when the application is running.

## Development

See [Development Setup](docs/development/development-setup.md) for instructions on setting up a development environment.

## License

MIT