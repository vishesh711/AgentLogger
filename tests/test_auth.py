import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_missing_api_key():
    """Test that protected endpoints require API key"""
    # Use an endpoint that definitely exists - analyze
    response = client.post("/api/v1/analyze", json={"code": "test", "language": "python"})
    assert response.status_code == 401

def test_invalid_api_key():
    """Test that invalid API keys are rejected"""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "test", "language": "python"},
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 401

def test_public_endpoints(client):
    """Test that public endpoints don't require API key"""
    # Test health endpoint (correct path)
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    # Test docs endpoints
    response = client.get("/docs")
    assert response.status_code == 200

def test_valid_api_key(client, test_api_key):
    """Test that valid API keys are accepted"""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "print('hello')", "language": "python"},
        headers={"X-API-Key": test_api_key.key}
    )
    # With a valid API key, we should get past authentication
    # But might still fail with other errors (not 401)
    assert response.status_code != 401 