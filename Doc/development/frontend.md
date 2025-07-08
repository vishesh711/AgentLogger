# AgentLogger Frontend Documentation

## Overview

The AgentLogger frontend provides a user-friendly interface for interacting with the AgentLogger API. It's built with modern web technologies and follows best practices for web development.

## Technology Stack

- **React 18**: Modern UI library for building component-based interfaces
- **TypeScript**: For type safety and better developer experience
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Component library built on Radix UI
- **React Router**: For client-side routing

## Architecture

- **Component-based design**: Modular components for reusability and maintainability
- **Responsive design**: Works on desktop and mobile devices
- **Dark mode support**: Automatic dark mode based on system preferences

## Key Components

### Pages

1. **Dashboard**: Main landing page with feature overview and API key management
2. **Playground**: Code analysis page for detecting issues
3. **NotFound**: 404 page for handling invalid routes

### Features

- **Code Editor**: Monaco Editor integration for syntax highlighting and code editing
- **Language Detection**: Automatic language detection from code snippets
- **Authentication**: API key-based authentication with local storage
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Responsive UI**: Mobile-friendly design that works on all devices

## Setup Instructions

### Development

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env` file:
```
VITE_API_BASE_URL=/api/v1
```

3. Start development server:
```bash
npm run dev
```

### Production

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Deploy the generated `dist` directory to your hosting service

## Docker Setup

1. Build and run using Docker:
```bash
docker build -t agentlogger-frontend ./frontend
docker run -p 80:80 agentlogger-frontend
```

2. Or use docker-compose to run the entire stack:
```bash
docker-compose up
```

## Nginx Configuration

The frontend uses Nginx to serve the static files and proxy API requests to the backend:

```nginx
location / {
    root /usr/share/nginx/html;
    index index.html;
    try_files $uri $uri/ /index.html;
}

location /api/v1/ {
    proxy_pass http://backend:8000/api/v1/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## API Integration

The frontend connects to the following backend endpoints:
- `/api/v1/analyze` - Code analysis
- `/api/v1/fix` - Code fixing
- `/api/v1/explain` - Error explanation
- `/api/v1/patch` - Patch generation
- `/api/v1/api-keys` - API key management

API key authentication is implemented using the `x-api-key` header for all API requests. The API key is stored in the browser's localStorage for persistence.

## Recent Fixes and Improvements

1. **Removed Lovable References**
   - Removed all references to Lovable from package.json
   - Removed Lovable tagger from vite.config.ts
   - Updated README.md to remove Lovable content
   - Updated index.html to remove Lovable image URLs

2. **Fixed API Integration**
   - Created a proper API client in `src/lib/api.ts`
   - Added localStorage checks for SSR compatibility
   - Added proper type definitions for API responses
   - Added error handling for API calls

3. **Fixed TypeScript Errors**
   - Added proper type annotations in vite.config.ts
   - Fixed header type issues in API fetch function
   - Installed missing type definitions (@types/node, @types/react, @types/react-dom)
   - Fixed component prop type issues

4. **Added API Key Management**
   - Updated Dashboard component to manage API keys
   - Added create, delete, and copy functionality for API keys
   - Added proper UI feedback for API operations

5. **Environment Configuration**
   - Added .env file for API URL configuration
   - Made API base URL configurable

6. **Docker Setup**
   - Created Dockerfile for the frontend
   - Added nginx configuration for serving the frontend
   - Updated docker-compose.yml to include frontend service
   - Added proper networking between frontend and backend

## Future Enhancements

1. **User Management**: Add user registration and profile management
2. **Project Management**: Save and manage multiple code projects
3. **History Tracking**: Track analysis and fix history
4. **GitHub Integration UI**: Direct GitHub PR creation from the UI
5. **Real-time Collaboration**: Add real-time collaboration features
6. **Offline Support**: Add offline capabilities with service workers
7. **Performance Optimization**: Code splitting and lazy loading for better performance 