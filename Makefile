.PHONY: help setup run test lint format migrate db-init docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  setup      - Install dependencies"
	@echo "  run        - Run the development server"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code using black"
	@echo "  migrate    - Run database migrations"
	@echo "  db-init    - Initialize database with initial data"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

setup:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest

lint:
	flake8 app tests

format:
	black app tests

migrate:
	alembic upgrade head

db-init:
	python scripts/init_db.py

docker-build:
	docker build -t agentlogger-api .

docker-run:
	docker run -p 8000:8000 --env-file .env agentlogger-api 