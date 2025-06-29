import os
import subprocess
import tempfile
import uuid
from typing import Dict, Tuple

from app.core.config import settings


class CodeRunner:
    """
    Safely execute code in a sandbox environment
    
    Uses Docker for isolation by default, with fallback to local execution
    """
    
    def __init__(self, use_docker: bool = None):
        """
        Initialize the code runner
        
        Args:
            use_docker: Whether to use Docker for isolation (defaults to settings.USE_DOCKER_SANDBOX)
        """
        self.use_docker = settings.USE_DOCKER_SANDBOX if use_docker is None else use_docker
    
    async def run_code(self, code: str, language: str) -> Dict[str, str]:
        """
        Run code in a sandbox environment
        
        Args:
            code: The code to execute
            language: The programming language
        
        Returns:
            Dict containing stdout, stderr, and execution status
        """
        if self.use_docker:
            return await self._run_in_docker(code, language)
        else:
            return await self._run_locally(code, language)
    
    async def _run_in_docker(self, code: str, language: str) -> Dict[str, str]:
        """
        Run code in a Docker container
        """
        # Create a temporary directory to mount into the container
        with tempfile.TemporaryDirectory() as temp_dir:
            # Determine file extension and Docker image based on language
            file_ext, docker_image = self._get_language_config(language)
            
            # Write code to a temporary file
            file_path = os.path.join(temp_dir, f"code{file_ext}")
            with open(file_path, "w") as f:
                f.write(code)
            
            # Generate a unique container name
            container_name = f"agentlogger-sandbox-{uuid.uuid4().hex[:8]}"
            
            # Run the code in a Docker container
            cmd = [
                "docker", "run",
                "--name", container_name,
                "--rm",  # Remove container after execution
                "-v", f"{temp_dir}:/code",
                "--network", "none",  # Disable network access
                "--memory", "256m",  # Limit memory
                "--cpus", "0.5",  # Limit CPU
                "--read-only",  # Make filesystem read-only
                "--cap-drop", "ALL",  # Drop all capabilities
                "--security-opt", "no-new-privileges",  # Prevent privilege escalation
                docker_image,
                *self._get_execution_command(language, f"/code/code{file_ext}")
            ]
            
            # Set timeout
            timeout = settings.EXECUTION_TIMEOUT
            
            try:
                # Run the command with timeout
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                return {
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "exit_code": process.returncode,
                    "timed_out": False
                }
            
            except subprocess.TimeoutExpired:
                # Kill the container if it timed out
                subprocess.run(["docker", "kill", container_name], capture_output=True)
                
                return {
                    "stdout": "",
                    "stderr": f"Execution timed out after {timeout} seconds",
                    "exit_code": -1,
                    "timed_out": True
                }
            
            except Exception as e:
                return {
                    "stdout": "",
                    "stderr": f"Error running code: {str(e)}",
                    "exit_code": -1,
                    "timed_out": False
                }
    
    async def _run_locally(self, code: str, language: str) -> Dict[str, str]:
        """
        Run code locally (fallback method)
        
        This is less secure than Docker isolation and should only be used
        when Docker is not available
        """
        # Create a temporary file for the code
        file_ext, _ = self._get_language_config(language)
        
        with tempfile.NamedTemporaryFile(suffix=file_ext, mode="w", delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Get the command to execute the code
            cmd = self._get_execution_command(language, temp_file_path)
            
            # Set timeout
            timeout = settings.EXECUTION_TIMEOUT
            
            # Run the command with timeout
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode,
                "timed_out": False
            }
        
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {timeout} seconds",
                "exit_code": -1,
                "timed_out": True
            }
        
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error running code: {str(e)}",
                "exit_code": -1,
                "timed_out": False
            }
        
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    
    def _get_language_config(self, language: str) -> Tuple[str, str]:
        """
        Get file extension and Docker image for a language
        """
        language = language.lower()
        
        if language in ["python", "py"]:
            return ".py", "python:3.11-slim"
        elif language in ["javascript", "js"]:
            return ".js", "node:18-slim"
        elif language in ["typescript", "ts"]:
            return ".ts", "node:18-slim"
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _get_execution_command(self, language: str, file_path: str) -> list:
        """
        Get the command to execute code in a specific language
        """
        language = language.lower()
        
        if language in ["python", "py"]:
            return ["python", file_path]
        elif language in ["javascript", "js"]:
            return ["node", file_path]
        elif language in ["typescript", "ts"]:
            return ["npx", "ts-node", file_path]
        else:
            raise ValueError(f"Unsupported language: {language}") 