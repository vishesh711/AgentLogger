import json
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.models.schemas.analysis import CodeIssue


class GroqClient:
    """Client for Groq LLM API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _call_api(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Groq API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    
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
        5. Best practice violations
        
        For each issue, provide:
        - A unique ID
        - Issue type
        - Severity (critical, high, medium, low)
        - Description of the problem
        - Line numbers where the issue occurs
        - A code snippet showing the issue
        - Suggestions for fixing the issue
        
        Format your response as a JSON object with an "issues" array containing each issue.
        Example format:
        {{
            "issues": [
                {{
                    "id": "ISSUE-1",
                    "type": "security_vulnerability",
                    "severity": "high",
                    "message": "SQL injection vulnerability in query construction",
                    "line_start": 15,
                    "line_end": 17,
                    "column_start": 10,
                    "column_end": 52,
                    "code_snippet": "query = f'SELECT * FROM users WHERE id = {{user_input}}'",
                    "fix_suggestions": ["Use parameterized queries instead of string interpolation"]
                }}
            ]
        }}
        """
    
    def _get_fix_prompt(self, code: str, language: str, issue: CodeIssue) -> str:
        """
        Generate the prompt for fixing an issue
        """
        return f"""
        Fix the following issue in this {language} code:
        
        ```{language}
        {code}
        ```
        
        Issue details:
        - ID: {issue.id}
        - Type: {issue.type}
        - Severity: {issue.severity}
        - Message: {issue.message}
        - Location: Lines {issue.line_start} to {issue.line_end or issue.line_start}
        
        Please provide:
        1. The complete fixed code
        2. A clear explanation of the changes made
        
        Format your response as a JSON object with "fixed_code" and "explanation" fields.
        Example format:
        {{
            "fixed_code": "def example():\\n    return 'fixed code here'",
            "explanation": "The issue was fixed by..."
        }}
        """
    
    def _get_error_explanation_prompt(self, error_message: str, code: str, language: str) -> str:
        """
        Generate the prompt for error explanation
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
        2. The likely cause of the error in this specific code
        3. How to fix the error
        
        Use simple language that a beginner programmer would understand.
        """ 