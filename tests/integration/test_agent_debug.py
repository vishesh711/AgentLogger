"""
Test script for the agent-based debugging system.
"""
import requests
import pytest
import os

# API URL
API_URL = "http://localhost:8000/api/v1"

# Sample buggy code
BUGGY_CODE = """
def divide_numbers(a, b):
    # Bug: No check for division by zero
    return a / b

def main():
    # This will cause a ZeroDivisionError
    result = divide_numbers(10, 0)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
"""

def test_agent_debug():
    """Test the agent-based debugging system."""
    # Skip if running in CI without actual server
    if os.getenv("ENVIRONMENT") == "testing":
        pytest.skip("Skipping integration test in CI environment")
    
    print("Starting agent system test...")
    
    # Test health endpoint first
    try:
        response = requests.get(f"{API_URL}/health/health", timeout=5)
        if response.status_code != 200:
            pytest.skip("Backend server not available for integration testing")
    except requests.RequestException:
        pytest.skip("Backend server not available for integration testing")
    
    print("\nSubmitting code for debugging...")
    
    # Test the agent debug endpoint
    try:
        response = requests.post(
            f"{API_URL}/agent-debug/test-full-workflow",
            json={
                "code": BUGGY_CODE,
                "language": "python"
            },
            headers={
                "X-API-Key": "QwF6KA863mAeRHOCY9HJJEccV9Gp0chKTL5pogRjeOU"
            },
            timeout=30
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "workflow_result" in data or "result" in data, "Expected workflow result in response"
        
        print(f"Agent debug test completed successfully: {data}")
        
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")

if __name__ == "__main__":
    test_agent_debug() 