"""
Analyzer Agent for analyzing code and identifying issues.
"""
import asyncio
import json
import uuid
from typing import Any, Dict, List, Optional, Union

from app.agents.base_agent import BaseAgent, Message
from app.services.ai.groq_client import GroqClient
from app.utils.parsing.parser_factory import get_parser
from app.utils.sandbox.code_runner import CodeRunner

class AnalyzerAgent(BaseAgent):
    """
    Analyzer Agent that analyzes code and identifies issues.
    """
    def __init__(
        self, 
        agent_id: str, 
        llm_client: GroqClient,
        code_runner: Optional[CodeRunner] = None
    ):
        super().__init__(agent_id=agent_id, agent_type="analyzer")
        self.llm_client = llm_client
        self.code_runner = code_runner
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and analyze code."""
        self.log(f"Processing message: {message.message_type} from {message.sender_id}")
        
        if message.message_type == "analyze_request":
            return await self.analyze_code(message)
        elif message.message_type == "task" and message.content.get("step") == "analyze":
            return await self.analyze_code(message)
        else:
            self.log(f"Ignoring message type: {message.message_type}", level="INFO")
            return None
    
    async def analyze_code(self, message: Message) -> Message:
        """Analyze code to identify issues."""
        session_id = message.content.get("session_id")
        code = message.content.get("code")
        language = message.content.get("language")
        error_message = message.content.get("error_message")
        
        self.log(f"Analyzing code for session {session_id}")
        
        issues = []
        
        try:
            # Step 1: Static analysis using language-specific parser
            static_issues = await self.perform_static_analysis(code, language)
            issues.extend(static_issues)
            
            # Step 2: If there's an error message, analyze it
            if error_message:
                error_issues = await self.analyze_error_message(code, language, error_message)
                issues.extend(error_issues)
            
            # Step 3: If we have a code runner, try to execute the code
            if self.code_runner and not error_message:
                runtime_issues = await self.execute_code(code, language)
                issues.extend(runtime_issues)
            
            # Step 4: Use LLM to identify additional issues
            llm_issues = await self.identify_issues_with_llm(code, language, error_message)
            issues.extend(llm_issues)
            
            # Remove duplicates and assign IDs
            unique_issues = []
            seen_messages = set()
            
            for issue in issues:
                if issue["message"] not in seen_messages:
                    issue["id"] = str(uuid.uuid4())
                    unique_issues.append(issue)
                    seen_messages.add(issue["message"])
            
            # Sort issues by severity
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
            unique_issues.sort(key=lambda x: severity_order.get(x.get("severity", "info"), 5))
            
        except Exception as e:
            self.log(f"Error during analysis: {str(e)}", level="ERROR")
            unique_issues = [{
                "id": str(uuid.uuid4()),
                "type": "analysis_error",
                "message": f"Analysis failed: {str(e)}",
                "line_start": 1,
                "line_end": 1,
                "severity": "critical",
                "confidence": 0.9
            }]
        
        # Create response message for coordinator
        response = Message(
            message_type="analysis_result",
            sender_id=self.agent_id,
            recipient_id=message.sender_id,  # Send back to coordinator
            content={
                "session_id": session_id,
                "issues": unique_issues,
                "analysis_complete": True
            },
            parent_id=message.message_id
        )
        
        self.log(f"Found {len(unique_issues)} issues in code")
        return response
    
    async def perform_static_analysis(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Perform static analysis on the code using language-specific parsers."""
        issues = []
        
        try:
            # Get the appropriate parser for the language
            parser = get_parser(language)
            if not parser:
                self.log(f"No parser available for language: {language}", level="WARNING")
                return issues
            
            # Parse the code and get syntax issues
            parsed = parser.parse(code)
            syntax_issues = parser.get_syntax_issues(parsed)
            
            for issue in syntax_issues:
                issues.append({
                    "type": "syntax",
                    "message": issue.get("message", "Syntax error"),
                    "line_start": issue.get("line", 1),
                    "line_end": issue.get("line", 1),
                    "column_start": issue.get("column", 1),
                    "column_end": issue.get("column", 1) + 1,
                    "severity": "high",
                    "confidence": 0.9
                })
        except Exception as e:
            self.log(f"Error in static analysis: {str(e)}", level="ERROR")
        
        return issues
    
    async def analyze_error_message(self, code: str, language: str, error_message: str) -> List[Dict[str, Any]]:
        """Analyze an error message to identify issues."""
        issues = []
        
        # Extract line numbers from error message if possible
        line_number = self.extract_line_number(error_message)
        
        issues.append({
            "type": "runtime",
            "message": f"Runtime error: {error_message}",
            "line_start": line_number if line_number else 1,
            "line_end": line_number if line_number else len(code.splitlines()),
            "severity": "critical",
            "confidence": 0.9
        })
        
        return issues
    
    async def execute_code(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Execute the code in a sandbox to identify runtime issues."""
        issues = []
        
        if not self.code_runner:
            return issues
        
        try:
            result = await self.code_runner.run_code(code, language)
            
            if result.get("error"):
                error_message = result.get("error")
                line_number = self.extract_line_number(error_message)
                
                issues.append({
                    "type": "runtime",
                    "message": f"Runtime error: {error_message}",
                    "line_start": line_number if line_number else 1,
                    "line_end": line_number if line_number else len(code.splitlines()),
                    "severity": "critical",
                    "confidence": 0.9
                })
        except Exception as e:
            self.log(f"Error executing code: {str(e)}", level="ERROR")
        
        return issues
    
    async def identify_issues_with_llm(self, code: str, language: str, error_message: Optional[str]) -> List[Dict[str, Any]]:
        """Use LLM to identify issues in the code."""
        issues = []
        
        try:
            # Use the Groq client's analyze_code method which is properly designed
            llm_issues = await self.llm_client.analyze_code(code, language)
            
            # Convert CodeIssue objects to dictionaries
            for issue in llm_issues:
                issues.append({
                    "type": issue.type,
                    "message": issue.message,
                    "line_start": issue.line_start,
                    "line_end": issue.line_end or issue.line_start,
                    "column_start": getattr(issue, 'column_start', None),
                    "column_end": getattr(issue, 'column_end', None),
                    "severity": issue.severity,
                    "confidence": 0.9  # Default confidence since CodeIssue doesn't have this field
                })
            
            self.log(f"LLM analysis found {len(issues)} issues")
            
        except Exception as e:
            self.log(f"Error in LLM analysis: {str(e)}", level="ERROR")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}", level="ERROR")
        
        return issues
    
    def create_analysis_prompt(self, code: str, language: str, error_message: Optional[str]) -> str:
        """Create a prompt for the LLM to analyze the code."""
        prompt = f"""
You are an expert code analyzer. Analyze the following {language} code and identify any issues, bugs, or potential problems.

CODE:
```{language}
{code}
```

{f"ERROR MESSAGE: {error_message}" if error_message else ""}

Identify all issues in the code. For each issue, provide:
1. A brief description of the issue
2. The line number(s) where the issue occurs
3. The severity (critical, high, medium, low, info)
4. A confidence score (0.0 to 1.0) of how certain you are about this issue

Format your response as a JSON array of issues. Each issue should have the following structure:
{{
  "type": "issue_type",
  "message": "description of the issue",
  "line_start": line_number_start,
  "line_end": line_number_end,
  "severity": "severity_level",
  "confidence": confidence_score
}}

Only respond with the JSON array, no other text.
"""
        return prompt
    
    def parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse the LLM response to extract issues."""
        issues = []
        
        try:
            # Try to extract JSON from the response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            response = response.strip()
            
            # Parse the JSON
            parsed = json.loads(response)
            if isinstance(parsed, list):
                for issue in parsed:
                    if isinstance(issue, dict) and "message" in issue:
                        # Ensure all required fields are present
                        issues.append({
                            "type": issue.get("type", "logic"),
                            "message": issue.get("message", "Unknown issue"),
                            "line_start": issue.get("line_start", 1),
                            "line_end": issue.get("line_end", issue.get("line_start", 1)),
                            "severity": issue.get("severity", "medium"),
                            "confidence": issue.get("confidence", 0.5)
                        })
        except Exception as e:
            self.log(f"Error parsing LLM response: {str(e)}", level="ERROR")
        
        return issues
    
    def extract_line_number(self, error_message: str) -> Optional[int]:
        """Extract line number from an error message."""
        import re
        
        # Common patterns for line numbers in error messages
        patterns = [
            r"line (\d+)",
            r"Line (\d+)",
            r":(\d+):",
            r"at line (\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_message)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass
        
        return None 