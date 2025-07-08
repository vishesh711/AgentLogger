import os
import pytest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Handle SQLAlchemy Utils import for different versions
try:
    from sqlalchemy_utils import database_exists, create_database
except ImportError:
    # Fallback implementation for tests
    def database_exists(url):
        return True
    
    def create_database(url):
        pass
from fastapi.testclient import TestClient

from app.main import app
from app.core.db import Base, get_db

# Test database URL - use in-memory SQLite for tests
TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "sqlite:///./test_agentlogger.db"
)

# Create test engine
engine = create_engine(TEST_DATABASE_URL)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """Set up the test database"""
    # Create database if it doesn't exist
    if not database_exists(engine.url) and not TEST_DATABASE_URL.startswith("sqlite"):
        create_database(engine.url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Return the engine
    yield engine
    
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    """Create a fresh database session for each test"""
    connection = setup_database.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def mock_agent_system():
    """Mock the agent system to prevent it from starting during tests"""
    mock_system = Mock()
    mock_system.running = True
    mock_system.agents = {"coordinator_1": Mock(), "analyzer_1": Mock(), "fix_generator_1": Mock()}
    
    with patch("app.core.dependencies.get_agent_system", return_value=mock_system):
        with patch("app.core.dependencies.cleanup_agent_system"):
            yield mock_system

@pytest.fixture
def client(db_session, mock_agent_system):
    """Create a test client with a database session and mocked agent system"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    from app.models.db.user import User
    from app.api.v1.endpoints.auth import get_password_hash
    
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_superuser=False,
        full_name="Test User"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    
    return test_user

@pytest.fixture
def test_api_key(db_session, test_user):
    """Create a test API key"""
    from app.models.db.api_key import APIKey
    
    api_key = APIKey(
        key="test-api-key-for-testing",
        name="Test API Key",
        user_id=test_user.id,
        is_active=True
    )
    db_session.add(api_key)
    db_session.commit()
    db_session.refresh(api_key)
    
    return api_key

@pytest.fixture
def client_no_auth(db_session):
    """Create a test client without authentication middleware for testing"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Create a test app without authentication middleware
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.core.middleware import RateLimitMiddleware, AnalyticsMiddleware
    
    test_app = FastAPI()
    
    # Add only rate limiting and analytics middleware, skip auth
    test_app.add_middleware(RateLimitMiddleware)
    test_app.add_middleware(AnalyticsMiddleware)
    
    # Include the API router
    from app.api.v1.router import api_router
    test_app.include_router(api_router)
    
    # Add the health endpoint
    @test_app.get("/health")
    async def health_check():
        """Health check endpoint"""
        import time
        from app.core.config import settings
        from app.core.dependencies import get_agent_system
        
        try:
            agent_sys = get_agent_system()
            agent_status = "running" if agent_sys.running else "stopped"
            agent_count = len(agent_sys.agents)
        except Exception as e:
            agent_status = f"error: {str(e)}"
            agent_count = 0
        
        return {
            "status": "ok",
            "timestamp": time.time(),
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
            "agent_system": {
                "status": agent_status,
                "agent_count": agent_count
            }
        }
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(test_app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
