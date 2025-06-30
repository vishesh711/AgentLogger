from setuptools import setup, find_packages

setup(
    name="agent-logger",
    version="0.1.0",
    description="Command-line interface for the AgentLogger API",
    author="AgentLogger Team",
    author_email="info@agentlogger.ai",
    url="https://github.com/yourusername/agentlogger",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "httpx>=0.24.0",
        "configparser>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agent-logger=cli.agent_logger_cli:main_entry_point",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 