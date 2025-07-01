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

def test_public_endpoints():
    """Test that public endpoints don't require API key"""
    # Test health endpoint (correct path)
    response = client.get("/api/v1/health/health")
    assert response.status_code == 200
    
    # Test docs endpoints
    response = client.get("/docs")
    assert response.status_code == 200

def test_valid_api_key():
    """Test that valid API keys work"""
    # Use the default API key for testing with analyze endpoint
    response = client.post(
        "/api/v1/analyze",
        json={"code": "print('hello')", "language": "python"},
        headers={"X-API-Key": "QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU"}
    )
    # Should succeed (200) or have a validation error (422) but not auth error
    assert response.status_code in [200, 422] 