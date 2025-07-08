import requests
import sys

# Replace with your API key
API_KEY = "your_api_key_here"  # Replace with the key generated earlier
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"X-API-Key": API_KEY}

def create_github_pr(code, repo, branch="fix-branch"):
    """Create a GitHub PR with code changes"""
    print("Creating GitHub PR...")
    
    # First, submit the code for direct fix (without analysis)
    fix_response = requests.post(
        f"{BASE_URL}/fix/direct",
        headers=HEADERS,
        json={
            "code": code,
            "language": "python",
            "error_message": "ZeroDivisionError: division by zero",
            "description": "The function divides by zero without checking the denominator"
        }
    )
    
    if fix_response.status_code != 200:
        print(f"Error creating fix: {fix_response.status_code}")
        print(fix_response.json())
        return None
    
    fix_data = fix_response.json()
    fix_id = fix_data.get("id")
    
    print(f"Fix ID: {fix_id}")
    print("Waiting for fix to be generated...")
    
    # Wait for fix to be generated
    max_attempts = 10
    attempts = 0
    
    while attempts < max_attempts:
        status_response = requests.get(
            f"{BASE_URL}/fix/{fix_id}",
            headers=HEADERS
        )
        
        if status_response.status_code != 200:
            print(f"Error checking fix status: {status_response.status_code}")
            print(status_response.json())
            return None
        
        status_data = status_response.json()
        status = status_data.get("status")
        
        if status == "completed":
            print("Fix generated successfully!")
            print(f"Fixed code:\n{status_data.get('fixed_code')}")
            break
        
        print(f"Fix status: {status}. Waiting...")
        attempts += 1
        import time
        time.sleep(3)
    
    if attempts >= max_attempts:
        print("Fix generation timed out")
        return None
    
    # Now create a PR with the fix
    pr_response = requests.post(
        f"{BASE_URL}/github/pr",
        headers=HEADERS,
        json={
            "fix_id": fix_id,
            "repo": repo,
            "branch": branch,
            "title": "Fix: Division by zero error",
            "description": "Automatically generated fix for division by zero error"
        }
    )
    
    if pr_response.status_code != 200:
        print(f"Error creating PR: {pr_response.status_code}")
        print(pr_response.json())
        return None
    
    pr_data = pr_response.json()
    return pr_data

def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/integration/test_github_pr.py <github_repo> [branch_name]")
        sys.exit(1)
    
    repo = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else "fix-division-by-zero"
    
    # Fixed code
    code = """def divide_numbers(a, b):
    # Fixed: Added check for division by zero
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def main():
    # This will now handle the division by zero case
    try:
        result = divide_numbers(10, 0)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()"""
    
    # Create PR
    pr_data = create_github_pr(code, repo, branch)
    
    if pr_data:
        print("\nSuccessfully created PR!")
        print(f"PR URL: {pr_data.get('url')}")
        print(f"PR Number: {pr_data.get('number')}")
    else:
        print("\nFailed to create PR")

if __name__ == "__main__":
    main() 