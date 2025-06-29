import requests
import time
import sys
import os

# Replace with your API key
API_KEY = "your_api_key_here"  # Replace with the key generated earlier
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"X-API-Key": API_KEY}

def read_file(file_path):
    """Read the content of a file"""
    with open(file_path, "r") as file:
        return file.read()

def analyze_code(code, language="python"):
    """Submit code for analysis"""
    print("Submitting code for analysis...")
    response = requests.post(
        f"{BASE_URL}/analyze",
        headers=HEADERS,
        json={"language": language, "code": code}
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None
    
    return response.json()

def get_analysis_results(analysis_id):
    """Get analysis results"""
    print("Getting analysis results...")
    max_attempts = 10
    attempts = 0
    
    while attempts < max_attempts:
        response = requests.get(
            f"{BASE_URL}/analyze/{analysis_id}",
            headers=HEADERS
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            return None
        
        data = response.json()
        status = data.get("status", "")
        
        if status == "completed":
            return data
        
        print(f"Analysis status: {status}. Waiting...")
        attempts += 1
        time.sleep(2)
    
    print("Analysis timed out")
    return None

def request_fix(analysis_id, issue_id):
    """Request a fix for an issue"""
    print("Requesting fix...")
    response = requests.post(
        f"{BASE_URL}/fix",
        headers=HEADERS,
        json={"analysis_id": analysis_id, "issue_id": issue_id}
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None
    
    return response.json()

def get_fix_results(fix_id):
    """Get fix results"""
    print("Getting fix results...")
    max_attempts = 10
    attempts = 0
    
    while attempts < max_attempts:
        response = requests.get(
            f"{BASE_URL}/fix/{fix_id}",
            headers=HEADERS
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            return None
        
        data = response.json()
        status = data.get("status", "")
        
        if status == "completed":
            return data
        
        print(f"Fix status: {status}. Waiting...")
        attempts += 1
        time.sleep(2)
    
    print("Fix generation timed out")
    return None

def create_github_pr(fix_id, repo, branch="fix-branch"):
    """Create a GitHub PR with the fix"""
    print("Creating GitHub PR...")
    response = requests.post(
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
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None
    
    return response.json()

def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/integration/test_agent_logger.py <file_path> [github_repo]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    github_repo = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Read the code from file
    code = read_file(file_path)
    
    # Step 1: Analyze the code
    analysis_response = analyze_code(code)
    if not analysis_response:
        sys.exit(1)
    
    analysis_id = analysis_response.get("id")
    print(f"Analysis ID: {analysis_id}")
    
    # Step 2: Get analysis results
    analysis_results = get_analysis_results(analysis_id)
    if not analysis_results:
        sys.exit(1)
    
    issues = analysis_results.get("issues", [])
    if not issues:
        print("No issues found")
        sys.exit(0)
    
    print(f"Found {len(issues)} issues:")
    for i, issue in enumerate(issues):
        print(f"{i+1}. {issue.get('message')} (Line {issue.get('line_start')})")
    
    # Step 3: Request a fix for the first issue
    issue_id = issues[0].get("id")
    fix_response = request_fix(analysis_id, issue_id)
    if not fix_response:
        sys.exit(1)
    
    fix_id = fix_response.get("id")
    print(f"Fix ID: {fix_id}")
    
    # Step 4: Get fix results
    fix_results = get_fix_results(fix_id)
    if not fix_results:
        sys.exit(1)
    
    print("\nFixed code:")
    print(fix_results.get("fixed_code", ""))
    print("\nExplanation:")
    print(fix_results.get("explanation", ""))
    
    # Step 5: Create GitHub PR (if repo provided)
    if github_repo:
        pr_response = create_github_pr(fix_id, github_repo)
        if pr_response:
            print(f"\nCreated PR: {pr_response.get('url')}")

if __name__ == "__main__":
    main() 