import os
import json
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.models.schemas.analysis import CodeIssue


class GroqClient:
    """
    Client for interacting with Groq LLM API
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1"
        
        if not self.api_key:
            raise ValueError("Groq API key not provided")
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a completion using the Groq API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add user message
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Groq API error: {response.status_code} - {response.text}")
            
            return response.json()
    
    async def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text from a prompt and return just the content string
        
        This is an alias for generate_completion that returns just the text content
        
        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (higher = more random)
            
        Returns:
            The generated text content
        """
        response = await self.generate_completion(prompt, max_tokens, temperature)
        return response["choices"][0]["message"]["content"]
            
    async def analyze_code(self, code: str, language: str) -> List[CodeIssue]:
        """
        Analyze code for bugs and issues
        """
        prompt = self._get_analysis_prompt(code, language)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert code analyzer. Your task is to identify bugs, issues, and potential improvements in code."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "response_format": {"type": "json_object"}
        }
        
        response = await self._call_api("chat/completions", payload)
        content = response["choices"][0]["message"]["content"]
        
        try:
            result = json.loads(content)
            issues = result.get("issues", [])
            return [CodeIssue(**issue) for issue in issues]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    async def fix_issue(self, code: str, language: str, issue: CodeIssue) -> Dict[str, str]:
        """
        Generate a fix for a specific issue
        """
        prompt = self._get_fix_prompt(code, language, issue)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert code fixer. Your task is to fix bugs and issues in code."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "response_format": {"type": "json_object"}
        }
        
        response = await self._call_api("chat/completions", payload)
        content = response["choices"][0]["message"]["content"]
        
        try:
            result = json.loads(content)
            return {
                "fixed_code": result.get("fixed_code", ""),
                "explanation": result.get("explanation", "")
            }
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    async def explain_error(self, error_message: str, code: str, language: str) -> str:
        """
        Explain an error message in simple terms
        """
        prompt = self._get_error_explanation_prompt(error_message, code, language)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert at explaining code errors in simple terms."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        response = await self._call_api("chat/completions", payload)
        return response["choices"][0]["message"]["content"]
    
    async def _call_api(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the Groq API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{endpoint}",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Groq API error: {response.status_code} - {response.text}")
            
            return response.json()
    
    def _get_analysis_prompt(self, code: str, language: str) -> str:
        """
        Generate the prompt for code analysis
        """
        return f"""
        Analyze the following {language} code for bugs, issues, and potential improvements:
        
        ```{language}
        {code}
        ```
        
        Identify specific issues including:
        1. Syntax errors
        2. Logical bugs
        3. Performance issues
        4. Security vulnerabilities
        5. Code style issues
        
        Return your analysis as a JSON object with the following structure:
        {{
            "issues": [
                {{
                    "id": "unique-id-1",
                    "type": "issue-type",
                    "severity": "high|medium|low",
                    "message": "Description of the issue",
                    "line_start": 10,
                    "line_end": 12,
                    "column_start": 5,
                    "column_end": 20,
                    "code_snippet": "problematic code",
                    "fix_suggestions": ["suggestion 1", "suggestion 2"]
                }}
            ]
        }}
        """
    
    def _get_fix_prompt(self, code: str, language: str, issue: CodeIssue) -> str:
        """
        Generate the prompt for fixing a specific issue
        """
        return f"""
        Fix the following issue in this {language} code:
        
        ```{language}
        {code}
        ```
        
        Issue:
        - Type: {issue.type}
        - Message: {issue.message}
        - Line: {issue.line_start}
        
        Return your fix as a JSON object with the following structure:
        {{
            "fixed_code": "the complete fixed code",
            "explanation": "explanation of what was wrong and how you fixed it"
        }}
        """
    
    def _get_error_explanation_prompt(self, error_message: str, code: str, language: str) -> str:
        """
        Generate the prompt for explaining an error message
        """
        return f"""
        Explain the following error message in simple terms:
        
        ```
        {error_message}
        ```
        
        The error occurred in this {language} code:
        
        ```{language}
        {code}
        ```
        
        Please provide:
        1. A simple explanation of what the error means
        2. The likely cause of the error
        3. How to fix it
        """


async def get_fix_from_groq(
    code: str,
    language: str,
    error_message: Optional[str] = None,
    context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a fix for code using Groq LLM
    """
    client = GroqClient()
    
    system_message = """
    You are an expert programmer tasked with fixing code errors.
    Analyze the code and error message provided, then generate a fixed version of the code.
    Also provide a clear explanation of what was wrong and how you fixed it.
    Return your response in JSON format with the following structure:
    {
        "fixed_code": "the complete fixed code",
        "explanation": "detailed explanation of the issues and fixes"
    }
    """
    
    prompt = f"""
    I need help fixing this {language} code:
    
    ```{language}
    {code}
    ```
    
    """
    
    if error_message:
        prompt += f"""
        Error message:
        ```
        {error_message}
        ```
        """
    
    if context:
        prompt += f"""
        Additional context:
        {context}
        """
    
    prompt += """
    Please provide the fixed code and an explanation of what was wrong and how you fixed it.
    Return your response in JSON format with the following structure:
    {
        "fixed_code": "the complete fixed code",
        "explanation": "detailed explanation of the issues and fixes"
    }
    """
    
    try:
        response = await client.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3,
            max_tokens=4000
        )
        
        # Extract the content from the response
        content = response["choices"][0]["message"]["content"]
        
        # Parse JSON from the content
        # Find JSON block in the response if it's not pure JSON
        if not content.strip().startswith("{"):
            import re
            # First try to find JSON block in code fence
            json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if json_match:
                content = json_match.group(1)
            else:
                # Try to find any JSON-like structure
                json_match = re.search(r"\{[\s\S]*\"fixed_code\"[\s\S]*\"explanation\"[\s\S]*\}", content)
                if json_match:
                    content = json_match.group(0)
        
        try:
            result = json.loads(content)
            
            # Ensure the result has the expected structure
            if "fixed_code" not in result or "explanation" not in result:
                raise ValueError("Invalid response format from Groq API")
        except json.JSONDecodeError:
            # If JSON parsing fails, create a fallback response
            return {
                "fixed_code": code,
                "explanation": "Failed to parse the AI response. The original code is returned unchanged."
            }
        
        return result
        
    except Exception as e:
        # Handle errors and provide a fallback response
        return {
            "fixed_code": code,  # Return original code as fallback
            "explanation": f"Error generating fix: {str(e)}"
        } 