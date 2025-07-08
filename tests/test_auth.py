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
    # Should return 401 for invalid API key
    assert response.status_code == 401

def test_public_endpoints():
    """Test that public endpoints don't require API key"""
    # Test health endpoint (correct path)
    response = client.get("/health")
    assert response.status_code == 200
    
    # Test docs endpoints
    response = client.get("/docs")
    assert response.status_code == 200

def test_root_endpoint():
    """Test that root endpoint is public"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "AgentLogger API"

 