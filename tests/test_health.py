from fastapi.testclient import TestClient


def test_health_endpoint(client):
    """
    Test the health endpoint returns a 200 status code and the correct response format
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database_connected" in data
    
    assert data["status"] == "ok"
    assert isinstance(data["version"], str)
    assert isinstance(data["database_connected"], bool) 