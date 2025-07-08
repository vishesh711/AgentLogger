# Contributing to AgentLogger

Thank you for your interest in contributing to AgentLogger! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a positive and inclusive community.

## How to Contribute

There are many ways to contribute to AgentLogger:

1. **Report bugs**: If you find a bug, please report it by creating an issue on GitHub.
2. **Suggest features**: Have an idea for a new feature? Create an issue to suggest it.
3. **Improve documentation**: Documentation is crucial for any project. Help us improve it!
4. **Submit pull requests**: Fix bugs, add features, or improve documentation by submitting pull requests.

## Development Process

### Setting Up the Development Environment

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/agentlogger.git
   cd agentlogger
   ```
3. Set up the development environment:
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes in your branch.
2. Follow the [code style guidelines](#code-style-guidelines).
3. Add tests for your changes.
4. Run the tests to make sure everything passes:
   ```bash
   pytest
   ```
5. Update the documentation if necessary.

### Submitting a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Create a pull request on GitHub.
3. Describe your changes in the pull request description.
4. Link any related issues.
5. Wait for a maintainer to review your pull request.

## Code Style Guidelines

We follow these coding standards:

- **Python**: We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:
  - Line length: 100 characters
  - Use 4 spaces for indentation
  - Use docstrings for all public functions, classes, and methods
  - Use type hints for function parameters and return values

- **JavaScript/TypeScript**: We follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).

- **Markdown**: We follow the [Markdown Style Guide](https://www.markdownguide.org/basic-syntax/).

We use the following tools to enforce code style:

- **Black**: For formatting Python code
- **isort**: For sorting imports
- **Flake8**: For linting Python code
- **mypy**: For type checking Python code

You can run these tools with:

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint code
flake8 app tests

# Type check
mypy app
```

## Testing Guidelines

We use pytest for testing. All new features should include tests. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test files
pytest tests/test_health.py
```

## Documentation Guidelines

We use Markdown for documentation. All new features should include documentation.

- Use clear and concise language
- Include examples where appropriate
- Update existing documentation if your changes affect it

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Changes that do not affect the meaning of the code (formatting, etc.)
- **refactor**: Code changes that neither fix a bug nor add a feature
- **perf**: Code changes that improve performance
- **test**: Adding or updating tests
- **chore**: Changes to the build process or auxiliary tools

Examples:
- `feat: add multi-level error explanations`
- `fix: handle division by zero in code execution`
- `docs: update installation guide`

## Issue and Pull Request Labels

We use labels to categorize issues and pull requests:

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Documentation changes
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **question**: Further information is requested

## Release Process

We use [Semantic Versioning](https://semver.org/) for releases:

- **MAJOR**: Incompatible API changes
- **MINOR**: Add functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

## Getting Help

If you need help, you can:

- Create an issue on GitHub
- Contact the maintainers directly
- Join our community chat (if available)

## Thank You

Thank you for contributing to AgentLogger! Your help is greatly appreciated. 