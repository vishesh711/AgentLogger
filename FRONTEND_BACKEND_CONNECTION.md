# Frontend-Backend Connection

This document explains how the frontend and backend components of AgentLogger are connected and how to ensure they work together properly.

## Core Concept: Multi-Agent Architecture

AgentLogger's core concept is its multi-agent architecture for debugging code:

1. **Analyzer Agent**: Examines code to identify bugs, issues, and potential improvements
2. **Fix Generator Agent**: Creates fixes for the identified issues
3. **Coordinator Agent**: Orchestrates the workflow between agents

These agents communicate through a message-passing system to provide comprehensive debugging assistance.

## Connection Overview

The frontend React application communicates with the backend FastAPI service through REST API endpoints. The main connection points are:

1. API base URL configuration
2. Authentication via API key
3. Endpoint mapping for core functionality

## Configuration

### Backend Configuration

The backend API is configured to:

- Run on port 8000 inside the Docker container
- Accept API key authentication via the `X-API-Key` header
- Expose endpoints under the `/api/v1/` prefix

### Frontend Configuration

The frontend is configured to:

- Connect to the backend API using the base URL `/api/v1/`
- Include the API key in all requests
- Handle API responses and errors appropriately

## API Key Authentication

API key authentication is implemented as follows:

1. The backend validates the `X-API-Key` header against stored API keys in the database
2. The frontend includes this header in all API requests
3. For development, a default API key is configured: `l0W7EsOlXlvcoTfRg1Fmdg6z9gsZalpSeEBRVcHiY_4`

## Nginx Configuration

Nginx is configured as a reverse proxy to:

1. Serve the frontend static files
2. Proxy API requests to the backend
3. Forward the API key header for documentation access
4. Handle the API documentation endpoints properly

## Core Functionality Endpoints

The main endpoints that connect the frontend to the backend's agent-based functionality are:

- `/api/v1/analyze` - Submit code for analysis by the Analyzer Agent
- `/api/v1/fix` - Request fixes from the Fix Generator Agent
- `/api/v1/explain` - Get explanations for error messages
- `/api/v1/patch` - Generate patches for code issues
- `/api/v1/agent-debug` - Debug and monitor the agent system

## Troubleshooting

If you encounter connection issues between the frontend and backend:

1. Ensure the API key is correctly configured in the frontend
2. Check that the nginx configuration properly proxies requests
3. Verify that the backend API is running and accessible
4. Check for CORS issues if developing locally outside Docker
5. Ensure the database is properly initialized with the required tables and data

## Development Workflow

When developing new features:

1. Start the backend API using `docker-compose up backend`
2. Start the frontend development server using `./run_frontend.sh`
3. Make changes to the frontend code and test against the API
4. Use the API documentation at `/docs` to understand available endpoints

## Issues Fixed

1. **Database Schema Issues**
   - Added missing columns to the database schema:
     - `file_path` column to `analysis_requests` table
     - `summary` column to `analysis_requests` table
     - `completed_at` column to `analysis_requests` table
   - Created PostgreSQL enum type `analysisstatus` for the status column

2. **API Key Integration**
   - Added a default API key in the frontend code
   - Improved error handling in the frontend to show more informative messages

3. **Docker Configuration**
   - Updated the Dockerfile to run database migrations on startup
   - Fixed the PostgreSQL version to match the existing database files
   - Added healthchecks to ensure services start in the correct order

4. **Frontend Updates**
   - Enhanced error handling in the Playground component
   - Added better error messages for API connection issues

## How to Use

1. The application is now running at http://localhost
2. The API key is automatically set in the frontend
3. You can analyze code by going to the Playground page

## Known Issues

There are still some issues with the database schema that need to be addressed:

1. The `analysisstatus` enum type needs to be properly defined in the database
2. The backend needs to be updated to use the correct enum values

These issues will be addressed in a future update. 