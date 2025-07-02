from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Ensure database URI is a string
database_uri = settings.SQLALCHEMY_DATABASE_URI or "sqlite:///./agentlogger.db"

# Create SQLAlchemy engine
engine = create_engine(
    database_uri,
    pool_pre_ping=True,  # Test connections before using them
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 