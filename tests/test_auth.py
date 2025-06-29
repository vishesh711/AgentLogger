import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_missing_api_key(client):
    """
    Test that requests without an API key are rejected
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    
    data = response.json()
    assert "detail" in data
    assert "API key" in data["detail"]


def test_invalid_api_key(client):
    """
    Test that requests with an invalid API key are rejected
    """
    response = client.get(
        "/api/v1/users/me",
        headers={"X-API-Key": "invalid_key"}
    )
    assert response.status_code == 401
    
    data = response.json()
    assert "detail" in data
    assert "Invalid" in data["detail"]


def test_public_endpoints(client):
    """
    Test that public endpoints don't require authentication
    """
    # Test that the health endpoint doesn't require authentication
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    # Test that the docs endpoint doesn't require authentication
    response = client.get("/docs")
    assert response.status_code == 200 