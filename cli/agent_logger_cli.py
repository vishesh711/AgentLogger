#!/usr/bin/env python3
import os
import argparse
import configparser
from pathlib import Path
from typing import Optional

import httpx


class AgentLoggerCLI:
    """
    Command-line interface for the AgentLogger API
    """
    
    def __init__(self):
        self.config_dir = Path.home() / ".agent_logger"
        self.config_file = self.config_dir / "config.ini"
        self.api_key = None
        self.api_url = "http://localhost:8000/v1"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from config file"""
        config = configparser.ConfigParser()
        
        if self.config_file.exists():
            config.read(self.config_file)
            
            if "api" in config:
                self.api_key = config["api"].get("api_key")
                self.api_url = config["api"].get("api_url", self.api_url)
    
    def save_config(self) -> None:
        """Save configuration to config file"""
        config = configparser.ConfigParser()
        
        config["api"] = {
            "api_key": self.api_key or "",
            "api_url": self.api_url
        }
        
        with open(self.config_file, "w") as f:
            config.write(f)
    
    def configure(self, api_key: Optional[str] = None, api_url: Optional[str] = None) -> None:
        """Configure the CLI with API key and URL"""
        if api_key:
            self.api_key = api_key
        
        if api_url:
            self.api_url = api_url
        
        self.save_config()
        print(f"Configuration saved to {self.config_file}")
    
    async def analyze_code(self, file_path: str, language: Optional[str] = None) -> None:
        """Analyze code for bugs and issues"""
        if not self.api_key:
            print("Error: API key not configured. Run 'agent-logger configure --api-key YOUR_API_KEY'")
            return
        
        # Determine language from file extension if not provided
        if not language:
            ext = Path(file_path).suffix.lower()
            language_map = {
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".jsx": "javascript",
                ".tsx": "typescript",
                ".java": "java",
                ".go": "go",
                ".rb": "ruby",
                ".php": "php",
                ".cs": "csharp",
                ".cpp": "cpp",
                ".c": "c"
            }
            language = language_map.get(ext, "unknown")
        
        # Read file content
        try:
            with open(file_path, "r") as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return
        
        # Send request to API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/analyze",
                    headers={"X-API-Key": self.api_key},
                    json={"code": code, "language": language}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    issues = result.get("issues", [])
                    
                    if not issues:
                        print("✅ No issues found!")
                        return
                    
                    print(f"Found {len(issues)} issue(s):")
                    for i, issue in enumerate(issues, 1):
                        severity = issue.get("severity", "").upper()
                        severity_icon = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟡"
                        
                        print(f"\n{severity_icon} Issue #{i}: {issue.get('message')}")
                        print(f"  Type: {issue.get('type')}")
                        print(f"  Severity: {severity}")
                        print(f"  Location: Line {issue.get('line_start')}-{issue.get('line_end')}")
                        print(f"  Code: {issue.get('code_snippet')}")
                        
                        if issue.get("fix_suggestions"):
                            print("  Suggestions:")
                            for suggestion in issue.get("fix_suggestions", []):
                                print(f"    - {suggestion}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    async def fix_code(self, file_path: str, language: Optional[str] = None, auto_apply: bool = False) -> None:
        """Fix code issues"""
        if not self.api_key:
            print("Error: API key not configured. Run 'agent-logger configure --api-key YOUR_API_KEY'")
            return
        
        # Determine language from file extension if not provided
        if not language:
            ext = Path(file_path).suffix.lower()
            language_map = {
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".jsx": "javascript",
                ".tsx": "typescript",
                ".java": "java",
                ".go": "go",
                ".rb": "ruby",
                ".php": "php",
                ".cs": "csharp",
                ".cpp": "cpp",
                ".c": "c"
            }
            language = language_map.get(ext, "unknown")
        
        # Read file content
        try:
            with open(file_path, "r") as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return
        
        # Send request to API
        try:
            async with httpx.AsyncClient() as client:
                # First analyze the code
                analyze_response = await client.post(
                    f"{self.api_url}/analyze",
                    headers={"X-API-Key": self.api_key},
                    json={"code": code, "language": language}
                )
                
                if analyze_response.status_code != 200:
                    print(f"Error analyzing code: {analyze_response.status_code} - {analyze_response.text}")
                    return
                
                analysis_result = analyze_response.json()
                analysis_id = analysis_result.get("analysis_id")
                issues = analysis_result.get("issues", [])
                
                if not issues:
                    print("✅ No issues found!")
                    return
                
                print(f"Found {len(issues)} issue(s).")
                
                # Fix the issues
                fix_response = await client.post(
                    f"{self.api_url}/fix",
                    headers={"X-API-Key": self.api_key},
                    json={
                        "analysis_id": analysis_id,
                        "code": code,
                        "language": language
                    }
                )
                
                if fix_response.status_code != 200:
                    print(f"Error fixing code: {fix_response.status_code} - {fix_response.text}")
                    return
                
                fix_result = fix_response.json()
                fixed_code = fix_result.get("fixed_code")
                
                if not fixed_code:
                    print("❌ Failed to fix the code.")
                    return
                
                print("✅ Fixed code generated!")
                
                if auto_apply:
                    # Backup original file
                    backup_path = f"{file_path}.bak"
                    with open(backup_path, "w") as f:
                        f.write(code)
                    
                    # Write fixed code to file
                    with open(file_path, "w") as f:
                        f.write(fixed_code)
                    
                    print(f"✅ Fixed code applied to {file_path}")
                    print(f"Original code backed up to {backup_path}")
                else:
                    # Show diff
                    print("\nDiff:")
                    import difflib
                    diff = difflib.unified_diff(
                        code.splitlines(),
                        fixed_code.splitlines(),
                        fromfile=f"{file_path} (original)",
                        tofile=f"{file_path} (fixed)",
                        lineterm=""
                    )
                    for line in diff:
                        if line.startswith("+"):
                            print(f"\033[92m{line}\033[0m")  # Green
                        elif line.startswith("-"):
                            print(f"\033[91m{line}\033[0m")  # Red
                        else:
                            print(line)
                    
                    # Ask user if they want to apply the fix
                    apply = input("\nApply this fix? (y/n): ").lower().strip()
                    if apply == "y":
                        # Backup original file
                        backup_path = f"{file_path}.bak"
                        with open(backup_path, "w") as f:
                            f.write(code)
                        
                        # Write fixed code to file
                        with open(file_path, "w") as f:
                            f.write(fixed_code)
                        
                        print(f"✅ Fixed code applied to {file_path}")
                        print(f"Original code backed up to {backup_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    async def explain_error(self, error_message: str, file_path: Optional[str] = None, language: Optional[str] = None, level: str = "intermediate") -> None:
        """Explain an error message"""
        if not self.api_key:
            print("Error: API key not configured. Run 'agent-logger configure --api-key YOUR_API_KEY'")
            return
        
        code_context = ""
        
        # Read file content if provided
        if file_path:
            try:
                with open(file_path, "r") as f:
                    code_context = f.read()
                
                # Determine language from file extension if not provided
                if not language:
                    ext = Path(file_path).suffix.lower()
                    language_map = {
                        ".py": "python",
                        ".js": "javascript",
                        ".ts": "typescript",
                        ".jsx": "javascript",
                        ".tsx": "typescript",
                        ".java": "java",
                        ".go": "go",
                        ".rb": "ruby",
                        ".php": "php",
                        ".cs": "csharp",
                        ".cpp": "cpp",
                        ".c": "c"
                    }
                    language = language_map.get(ext, "unknown")
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                return
        
        # Send request to API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/explain",
                    headers={"X-API-Key": self.api_key},
                    json={
                        "error_trace": error_message,
                        "code_context": code_context,
                        "language": language or "unknown",
                        "user_level": level
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    explanation = result.get("explanation", {})
                    
                    # Print explanation based on level
                    if level == "beginner":
                        print("🔍 Simple Explanation:")
                        print(explanation.get("simple", "No simple explanation available."))
                    elif level == "intermediate":
                        print("🔍 Detailed Explanation:")
                        print(explanation.get("detailed", "No detailed explanation available."))
                    else:
                        print("🔍 Technical Explanation:")
                        print(explanation.get("technical", "No technical explanation available."))
                    
                    # Print learning resources
                    learning_resources = result.get("learning_resources", [])
                    if learning_resources:
                        print("\n📚 Learning Resources:")
                        for resource in learning_resources:
                            print(f"  - {resource.get('title')}: {resource.get('url')}")
                            if resource.get("description"):
                                print(f"    {resource.get('description')}")
                    
                    # Print related concepts
                    related_concepts = result.get("related_concepts", [])
                    if related_concepts:
                        print("\n🧩 Related Concepts:")
                        for concept in related_concepts:
                            print(f"  - {concept}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")


async def main():
    """Main entry point"""
    cli = AgentLoggerCLI()
    
    parser = argparse.ArgumentParser(description="AgentLogger CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Configure command
    configure_parser = subparsers.add_parser("configure", help="Configure the CLI")
    configure_parser.add_argument("--api-key", help="API key for authentication")
    configure_parser.add_argument("--api-url", help="API URL")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze code for bugs and issues")
    analyze_parser.add_argument("file", help="File to analyze")
    analyze_parser.add_argument("--language", help="Programming language")
    
    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Fix code issues")
    fix_parser.add_argument("file", help="File to fix")
    fix_parser.add_argument("--language", help="Programming language")
    fix_parser.add_argument("--auto-apply", action="store_true", help="Automatically apply fixes")
    
    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Explain an error message")
    explain_parser.add_argument("error", help="Error message or file containing error message")
    explain_parser.add_argument("--file", help="File with code context")
    explain_parser.add_argument("--language", help="Programming language")
    explain_parser.add_argument("--level", choices=["beginner", "intermediate", "advanced"], default="intermediate", help="Explanation level")
    
    args = parser.parse_args()
    
    if args.command == "configure":
        cli.configure(args.api_key, args.api_url)
    elif args.command == "analyze":
        await cli.analyze_code(args.file, args.language)
    elif args.command == "fix":
        await cli.fix_code(args.file, args.language, args.auto_apply)
    elif args.command == "explain":
        # Check if error is a file path
        error_message = args.error
        if os.path.isfile(args.error):
            with open(args.error, "r") as f:
                error_message = f.read()
        
        await cli.explain_error(error_message, args.file, args.language, args.level)
    else:
        parser.print_help()


def main_entry_point():
    """Entry point for the CLI when installed as a package"""
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    main_entry_point() 