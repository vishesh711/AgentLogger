from fastapi.testclient import TestClient
import re
from datetime import datetime


def test_health_endpoint(client):
    """
    Test the health endpoint returns a 200 status code and the correct response format
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "timestamp" in data
    assert "environment" in data
    
    assert data["status"] == "ok"
    assert isinstance(data["version"], str)
    assert isinstance(data["timestamp"], str)
    assert data["environment"] == "development"


def test_health_endpoint_timestamp_format(client):
    """
    Test that the timestamp in the health endpoint response is in ISO format
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    timestamp = data["timestamp"]
    
    # Check that the timestamp is in ISO format
    iso_format_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$'
    assert re.match(iso_format_regex, timestamp) is not None
    
    # Verify it can be parsed as a datetime
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        assert False, f"Timestamp {timestamp} is not in a valid ISO format"


def test_health_endpoint_version_format(client):
    """
    Test that the version in the health endpoint response is in semantic versioning format
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    version = data["version"]
    
    # Check that the version is in semantic versioning format (e.g., 1.0.0)
    semver_regex = r'^\d+\.\d+\.\d+$'
    assert re.match(semver_regex, version) is not None 