"""
Fix Generator Agent for generating fixes for identified issues.
"""
import asyncio
import json
import uuid
from typing import Any, Dict, List, Optional, Union

from app.agents.base_agent import BaseAgent, Message
from app.services.ai.groq_client import GroqClient

class FixGeneratorAgent(BaseAgent):
    """
    Fix Generator Agent that creates solutions for identified issues.
    """
    def __init__(
        self, 
        agent_id: str, 
        llm_client: GroqClient
    ):
        super().__init__(agent_id=agent_id, agent_type="fix_generator")
        self.llm_client = llm_client
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and generate fixes."""
        self.log(f"Processing message: {message.message_type} from {message.sender_id}")
        
        if message.message_type == "task" and message.content.get("step") == "fix":
            return await self.generate_fixes(message)
        else:
            self.log(f"Ignoring message type: {message.message_type}", level="INFO")
            return None
    
    async def generate_fixes(self, message: Message) -> Message:
        """Generate fixes for identified issues."""
        session_id = message.content.get("session_id")
        code = message.content.get("code")
        language = message.content.get("language")
        issues = message.content.get("issues", [])
        
        self.log(f"Generating fixes for {len(issues)} issues in session {session_id}")
        
        fixes = []
        
        # Process each issue and generate a fix
        for issue in issues:
            fix = await self.generate_fix_for_issue(code, language, issue)
            if fix:
                fixes.append(fix)
        
        # Create response message
        response = Message(
            message_type="agent_response",
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            content={
                "session_id": session_id,
                "fixes": fixes
            },
            parent_id=message.message_id
        )
        
        self.log(f"Generated {len(fixes)} fixes")
        return response
    
    async def generate_fix_for_issue(self, code: str, language: str, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a fix for a specific issue."""
        try:
            issue_id = issue.get("id")
            issue_type = issue.get("type")
            message = issue.get("message")
            line_start = issue.get("line_start", 1)
            line_end = issue.get("line_end", line_start)
            
            # Get the relevant code snippet
            code_lines = code.splitlines()
            if line_start > len(code_lines):
                line_start = len(code_lines)
            if line_end > len(code_lines):
                line_end = len(code_lines)
            
            # Extract the relevant code snippet (with context)
            context_lines = 5  # Number of lines of context to include
            snippet_start = max(0, line_start - context_lines - 1)
            snippet_end = min(len(code_lines), line_end + context_lines)
            code_snippet = "\n".join(code_lines[snippet_start:snippet_end])
            
            # Create a prompt for the LLM
            prompt = self.create_fix_prompt(code, code_snippet, language, issue, snippet_start + 1)
            
            # Call the LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse the response
            fix_data = self.parse_llm_response(response)
            
            if fix_data:
                return {
                    "id": str(uuid.uuid4()),
                    "issue_id": issue_id,
                    "description": fix_data.get("description", f"Fix for {message}"),
                    "code_before": code,
                    "code_after": self.apply_fix(code, fix_data),
                    "explanation": fix_data.get("explanation", ""),
                    "confidence": fix_data.get("confidence", 0.7)
                }
            
            return None
        except Exception as e:
            self.log(f"Error generating fix: {str(e)}", level="ERROR")
            return None
    
    def create_fix_prompt(self, full_code: str, code_snippet: str, language: str, issue: Dict[str, Any], snippet_start_line: int) -> str:
        """Create a prompt for the LLM to generate a fix."""
        issue_message = issue.get("message", "Unknown issue")
        issue_type = issue.get("type", "Unknown")
        line_start = issue.get("line_start", 1)
        line_end = issue.get("line_end", line_start)
        
        # Adjust line numbers for the snippet
        relative_line_start = line_start - snippet_start_line + 1
        relative_line_end = line_end - snippet_start_line + 1
        
        prompt = f"""
You are an expert code fixer. Fix the following {language} code that has an issue.

FULL CODE:
```{language}
{full_code}
```

CODE SNIPPET (with context):
```{language}
{code_snippet}
```

ISSUE:
- Type: {issue_type}
- Message: {issue_message}
- Location: Lines {line_start}-{line_end} in the full code (Lines {relative_line_start}-{relative_line_end} in the snippet)

Your task is to fix this issue. Provide:
1. A description of the fix
2. The fixed code (the ENTIRE fixed file, not just the snippet)
3. An explanation of why this fix works
4. A confidence score (0.0 to 1.0) of how certain you are this fix will resolve the issue

Format your response as a JSON object with the following structure:
{{
  "description": "brief description of the fix",
  "fixed_code": "the entire fixed code",
  "explanation": "explanation of why this fix works",
  "confidence": confidence_score
}}

Only respond with the JSON object, no other text.
"""
        return prompt
    
    def parse_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse the LLM response to extract the fix."""
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
            if isinstance(parsed, dict):
                return {
                    "description": parsed.get("description", ""),
                    "fixed_code": parsed.get("fixed_code", ""),
                    "explanation": parsed.get("explanation", ""),
                    "confidence": parsed.get("confidence", 0.5)
                }
        except Exception as e:
            self.log(f"Error parsing LLM response: {str(e)}", level="ERROR")
        
        return None
    
    def apply_fix(self, original_code: str, fix_data: Dict[str, Any]) -> str:
        """Apply the fix to the original code."""
        fixed_code = fix_data.get("fixed_code", "")
        
        # If the LLM provided a complete fixed code, use it
        if fixed_code:
            return fixed_code
        
        # Otherwise, return the original code (this should not happen with a well-designed prompt)
        return original_code 