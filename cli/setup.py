from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-logger-cli",
    version="0.1.0",
    description="Command-line interface for the AgentLogger API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AgentLogger Team",
    author_email="info@agentlogger.ai",
    url="https://github.com/AgentLogger/AgentLogger",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "httpx>=0.24.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "typer>=0.9.0",
        "pathspec>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-logger=agent_logger_cli:main_entry_point",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    keywords="cli, code-analysis, debugging, ai, linting",
    project_urls={
        "Bug Reports": "https://github.com/AgentLogger/AgentLogger/issues",
        "Documentation": "https://agentlogger.com/docs",
        "Source": "https://github.com/AgentLogger/AgentLogger",
    },
) 