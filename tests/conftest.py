import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient

from app.main import app
from app.core.db import Base, get_db
from app.models.db import user, api_key, analysis, fix, github

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
    
    # Clean up (for SQLite in-memory)
    if TEST_DATABASE_URL.startswith("sqlite"):
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
def client(db_session):
    """Create a test client with a database session"""
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
    from app.services.user_service import get_password_hash
    
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
    import secrets
    
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
