import os
from typing import Any, List, Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")
    
    # Project info
    PROJECT_NAME: str = "AgentLogger API"
    PROJECT_DESCRIPTION: str = "AI-powered debugging API service that helps developers detect, analyze, and fix code bugs."
    VERSION: str = "0.1.0"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:80", 
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "https://agentlogger.vercel.app",
        "https://*.vercel.app",
        "https://agentlogger-frontend.vercel.app"
    ]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        default_origins = [
            "http://localhost",
            "http://localhost:80", 
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080"
        ]
        
        if v is None or v == "":
            return default_origins
            
        if isinstance(v, str):
            # Handle comma-separated string
            try:
                origins = [i.strip() for i in v.split(",") if i.strip()]
                return origins if origins else default_origins
            except Exception:
                # Fallback to default if parsing fails
                return default_origins
        elif isinstance(v, list):
            return v if v else default_origins
            
        return default_origins
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB", "agentlogger")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
            
        # Use SQLite for development if DATABASE_URL is not set
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
            
        # Get values from field info context
        values = info.data if hasattr(info, 'data') else {}
            
        # Use SQLite for development by default
        if values.get("ENVIRONMENT") == "development" and not os.getenv("USE_POSTGRES", "").lower() == "true":
            return "sqlite:///./agentlogger.db"
            
        # Build the PostgreSQL connection string
        postgres_server = values.get('POSTGRES_SERVER') or os.getenv("POSTGRES_SERVER", "db")
        postgres_user = values.get('POSTGRES_USER') or os.getenv("POSTGRES_USER", "postgres")
        postgres_password = values.get('POSTGRES_PASSWORD') or os.getenv("POSTGRES_PASSWORD", "postgres")
        postgres_db = values.get('POSTGRES_DB') or os.getenv("POSTGRES_DB", "agentlogger")
        
        return f"postgresql://{postgres_user}:{postgres_password}@{postgres_server}/{postgres_db}"
    
    # Redis settings (optional)
    REDIS_HOST: Optional[str] = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: Optional[int] = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "")
    USE_REDIS: bool = os.getenv("USE_REDIS", "false").lower() == "true"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    # GitHub integration
    GITHUB_ACCESS_TOKEN: Optional[str] = os.getenv("GITHUB_ACCESS_TOKEN", "")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    GITHUB_REDIRECT_URI: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/github/callback")
    
    # Google OAuth integration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/google/callback")
    
    # Sandbox execution
    USE_DOCKER_SANDBOX: bool = os.getenv("USE_DOCKER_SANDBOX", "true").lower() == "true"
    EXECUTION_TIMEOUT: int = int(os.getenv("EXECUTION_TIMEOUT", "30"))  # seconds
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Sentry settings
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN", "")
    SENTRY_ENVIRONMENT: str = os.getenv("SENTRY_ENVIRONMENT", "development")
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))
    
    # Analytics settings
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
    ANALYTICS_PROVIDER: Optional[str] = os.getenv("ANALYTICS_PROVIDER", "")
    ANALYTICS_API_KEY: Optional[str] = os.getenv("ANALYTICS_API_KEY", "")


settings = Settings() 