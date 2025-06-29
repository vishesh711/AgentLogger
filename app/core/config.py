import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    
    # Project info
    PROJECT_NAME: str = "AgentLogger API"
    PROJECT_DESCRIPTION: str = "AI-powered debugging API service that helps developers detect, analyze, and fix code bugs."
    VERSION: str = "0.1.0"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis (optional)
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = 6379
    REDIS_PASSWORD: Optional[str] = None
    USE_REDIS: bool = False
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM settings
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"
    
    # GitHub integration
    GITHUB_ACCESS_TOKEN: Optional[str] = None
    
    # Sandbox execution
    USE_DOCKER_SANDBOX: bool = True
    EXECUTION_TIMEOUT: int = 30  # seconds
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60


settings = Settings() 