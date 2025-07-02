import os
import asyncio
import tempfile
import subprocess
from typing import Dict, Any, Optional

from app.core.config import settings

class CodeRunner:
    """
    Class for running code in a sandbox environment
    """
    def __init__(self, use_docker: Optional[bool] = None):
        """
        Initialize the CodeRunner
        
        Args:
            use_docker: Whether to use Docker for sandboxing (defaults to settings.USE_DOCKER_SANDBOX)
        """
        self.use_docker = use_docker if use_docker is not None else settings.USE_DOCKER_SANDBOX
    
    async def run_code(self, code: str, language: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Run code in a sandbox environment and return the result
        
        Args:
            code: The code to run
            language: The programming language of the code
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with execution results including:
            - success: Whether execution was successful
            - output: Output from the execution (if successful)
            - error: Error message (if unsuccessful)
        """
        if self.use_docker:
            return await run_in_docker(code, language, timeout)
        else:
            return await run_locally(code, language, timeout)

async def run_code_in_sandbox(
    code: str, 
    language: str, 
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Run code in a sandbox environment and return the result
    
    Args:
        code: The code to run
        language: The programming language of the code
        timeout: Maximum execution time in seconds
        
    Returns:
        Dict with execution results including:
        - success: Whether execution was successful
        - output: Output from the execution (if successful)
        - error: Error message (if unsuccessful)
    """
    # Use Docker sandbox if enabled
    if settings.USE_DOCKER_SANDBOX:
        return await run_in_docker(code, language, timeout)
    else:
        return await run_locally(code, language, timeout)

async def run_locally(code: str, language: str, timeout: int) -> Dict[str, Any]:
    """
    Run code locally in a subprocess with timeout
    """
    # Create a temporary file for the code
    file_extension = get_file_extension(language)
    with tempfile.NamedTemporaryFile(suffix=file_extension, mode='w', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    
    try:
        # Get the command to run the code
        cmd = get_run_command(language, temp_file_path)
        
        # Execute the command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # Wait for process with timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output": stdout.decode().strip()
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode().strip()
                }
        except asyncio.TimeoutError:
            # Kill the process if it times out
            process.kill()
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds"
            }
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

async def run_in_docker(code: str, language: str, timeout: int) -> Dict[str, Any]:
    """
    Run code in a Docker container for isolation
    """
    # In a real implementation, this would use Docker API to create and run a container
    # For now, we'll simulate it with a message
    return {
        "success": True,
        "output": f"Docker sandbox execution simulation for {language} code (not actually executed)"
    }

def get_file_extension(language: str) -> str:
    """
    Get the file extension for a programming language
    """
    language_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "go": ".go",
        "rust": ".rs",
        "ruby": ".rb",
        "php": ".php",
    }
    
    return language_map.get(language.lower(), ".txt")

def get_run_command(language: str, file_path: str) -> list:
    """
    Get the command to run code in a specific language
    """
    language = language.lower()
    
    if language == "python":
        return ["python", file_path]
    elif language == "javascript":
        return ["node", file_path]
    elif language == "typescript":
        return ["ts-node", file_path]
    elif language == "java":
        # Compile and run Java
        class_name = os.path.basename(file_path).replace(".java", "")
        return ["java", "-cp", os.path.dirname(file_path), class_name]
    elif language == "c":
        # Compile and run C
        output_path = file_path.replace(".c", "")
        subprocess.run(["gcc", file_path, "-o", output_path])
        return [output_path]
    elif language == "cpp":
        # Compile and run C++
        output_path = file_path.replace(".cpp", "")
        subprocess.run(["g++", file_path, "-o", output_path])
        return [output_path]
    elif language == "go":
        return ["go", "run", file_path]
    elif language == "rust":
        # Compile and run Rust
        output_path = file_path.replace(".rs", "")
        subprocess.run(["rustc", file_path, "-o", output_path])
        return [output_path]
    elif language == "ruby":
        return ["ruby", file_path]
    elif language == "php":
        return ["php", file_path]
    else:
        # Default to Python for unknown languages
        return ["python", file_path] 