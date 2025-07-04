import pytest
from fastapi.testclient import TestClient
import re
from datetime import datetime

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns a successful response"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data

def test_health_endpoint_timestamp_format():
    """
    Test that the health endpoint returns a timestamp in ISO format
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    timestamp = data["timestamp"]
    
    # The timestamp is now a float (time.time()), not ISO string
    assert isinstance(timestamp, (int, float))
    assert timestamp > 0

def test_health_endpoint_version_format():
    """
    Test that the health endpoint returns a version in semantic versioning format
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    version = data["version"]
    
    # Test semantic versioning format (major.minor.patch)
    semver_pattern = r'^\d+\.\d+\.\d+$'
    assert re.match(semver_pattern, version), f"Version {version} is not in semantic versioning format"

def test_health_endpoint_agent_system_info():
    """
    Test that the health endpoint includes agent system information
    """
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "agent_system" in data
    agent_system = data["agent_system"]
    assert "status" in agent_system
    assert "agent_count" in agent_system
    assert isinstance(agent_system["agent_count"], int) 