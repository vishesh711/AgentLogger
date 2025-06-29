"""
Test script for the agent-based debugging system.
"""
import asyncio
import json
import requests
import time
from typing import Dict, Any

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

async def test_agent_debug():
    """Test the agent-based debugging system."""
    print("Starting agent system...")
    response = requests.post(f"{API_URL}/agent/start")
    print(f"Response: {response.status_code} - {response.json()}")
    
    print("\nSubmitting code for debugging...")
    response = requests.post(
        f"{API_URL}/agent/agent-debug",
        json={
            "code": BUGGY_CODE,
            "language": "python",
            "error_message": "ZeroDivisionError: division by zero"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json()}")
        return
    
    data = response.json()
    session_id = data["session_id"]
    print(f"Session ID: {session_id}")
    
    print("\nChecking status...")
    max_attempts = 30
    for i in range(max_attempts):
        response = requests.get(f"{API_URL}/agent/agent-debug/{session_id}")
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json()}")
            break
        
        data = response.json()
        status = data["status"]
        print(f"Status: {status}")
        
        if status == "completed":
            print("\nDebugging completed!")
            print(json.dumps(data, indent=2))
            break
        
        time.sleep(2)
    
    print("\nStopping agent system...")
    response = requests.post(f"{API_URL}/agent/stop")
    print(f"Response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    asyncio.run(test_agent_debug()) 