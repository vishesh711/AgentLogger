# Frequently Asked Questions

This page answers common questions about AgentLogger.

## General Questions

### What is AgentLogger?

AgentLogger is an AI-powered debugging service that helps developers identify and fix code issues quickly. It leverages advanced AI models to analyze code, explain errors, generate fixes, and create patches.

### What programming languages does AgentLogger support?

AgentLogger currently supports:
- Python
- JavaScript
- TypeScript
- Java
- C#
- Go

Support for additional languages is planned for future releases.

### Is AgentLogger free to use?

AgentLogger offers both free and paid tiers. The free tier includes a limited number of API calls per month, while paid tiers offer higher limits and additional features.

## API Questions

### How do I get an API key?

You can generate an API key using the `/v1/api-keys` endpoint or the `scripts/generate_api_key.py` script if you're running your own instance.

### What is the rate limit for API calls?

The default rate limit is 60 requests per minute per API key. This can be configured in the `.env` file if you're running your own instance.

### Can I use AgentLogger in my CI/CD pipeline?

Yes, AgentLogger can be integrated into CI/CD pipelines to automatically analyze code, detect issues, and suggest fixes. You can use the API directly or the CLI tool.

## Features Questions

### How accurate are the code fixes?

AgentLogger uses advanced AI models to generate fixes, which are generally accurate for common issues. However, complex or domain-specific issues may require human review. Always review the generated fixes before applying them to production code.

### Can AgentLogger explain error messages from any library or framework?

AgentLogger can explain most standard error messages from popular libraries and frameworks. For less common or custom error messages, it will attempt to provide a general explanation based on the error pattern.

### How does the multi-level explanation feature work?

The multi-level explanation feature provides explanations tailored to different experience levels:

- **Beginner**: Simple, easy-to-understand explanations with examples
- **Intermediate**: More detailed explanations with technical context
- **Advanced**: In-depth explanations with implementation details

You can specify the desired level when making a request to the `/v1/explain` endpoint.

### Can AgentLogger create GitHub pull requests automatically?

Yes, AgentLogger can create GitHub pull requests with fixes automatically. You need to provide a GitHub token with appropriate permissions and specify the repository in your request.

## CLI Questions

### How do I install the AgentLogger CLI?

You can install the CLI using pip:

```bash
pip install agent-logger-cli
```

Or from source:

```bash
git clone https://github.com/yourusername/agentlogger.git
cd agentlogger
pip install -e cli/
```

### Can I use the CLI with my own AgentLogger instance?

Yes, you can configure the CLI to use your own AgentLogger instance:

```bash
agent-logger configure --api-key YOUR_API_KEY --api-url https://your-instance.com/v1
```

### Does the CLI support all API features?

Yes, the CLI supports all the features available in the API, including code analysis, fix generation, error explanation, and patch generation.

## Deployment Questions

### Can I deploy AgentLogger on my own server?

Yes, AgentLogger is open source and can be deployed on your own server. See the [Installation Guide](installation.md) and [Deployment Guide](deployment.md) for details.

### What are the server requirements for running AgentLogger?

The minimum server requirements are:
- 2GB RAM
- 1 CPU core
- 10GB disk space
- Docker and Docker Compose (recommended)

### Can I deploy AgentLogger without Docker?

Yes, you can deploy AgentLogger without Docker using a traditional setup with a WSGI/ASGI server like Uvicorn or Gunicorn behind a reverse proxy like Nginx. See the [Deployment Guide](deployment.md) for details.

## Troubleshooting

### I'm getting authentication errors with my API key

Make sure you're including the API key in the `X-API-Key` header with each request. If you're using the CLI, make sure you've configured it with the correct API key.

### The API is returning a 429 error

This means you've exceeded the rate limit. Wait a minute and try again, or consider upgrading to a higher tier with a higher rate limit.

### I'm getting a database connection error when running my own instance

Make sure your database is running and accessible, and that the database connection details in your `.env` file are correct.

### The CLI is not working

Make sure you've installed the CLI correctly and configured it with the correct API key and URL. You can check your configuration with:

```bash
cat ~/.agentlogger/config.json
```

## Contributing

### How can I contribute to AgentLogger?

You can contribute to AgentLogger by:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Improving documentation

See the [Contributing Guide](../development/contributing.md) for details.

### Where can I report bugs or request features?

You can report bugs or request features on the [GitHub Issues page](https://github.com/yourusername/agentlogger/issues). 