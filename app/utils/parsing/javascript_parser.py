import re
from typing import List

from app.models.schemas.analysis import CodeIssue
from app.utils.parsing.base_parser import BaseParser


class JavaScriptParser(BaseParser):
    """JavaScript-specific code parser"""
    
    def preprocess(self, code: str) -> str:
        """
        Preprocess JavaScript code before analysis
        
        Removes any leading/trailing whitespace and ensures proper line endings
        """
        return code.strip().replace("\r\n", "\n")
    
    def process_analysis_results(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """
        Process JavaScript-specific analysis results
        
        Validates line numbers and enhances issue descriptions
        """
        processed_issues = []
        
        for issue in issues:
            # Ensure line numbers are valid
            if issue.line_start < 1:
                issue.line_start = 1
            
            if issue.line_end is not None and issue.line_end < issue.line_start:
                issue.line_end = issue.line_start
            
            # Add JavaScript-specific context to certain issue types
            if issue.type == "reference_error":
                issue.message = f"Reference error: {issue.message}"
            elif issue.type == "type_error":
                issue.message = f"Type error: {issue.message}"
            elif issue.type == "syntax_error":
                issue.message = f"JavaScript syntax error: {issue.message}"
            
            processed_issues.append(issue)
        
        return processed_issues
    
    def process_fix_result(self, fixed_code: str) -> str:
        """
        Process fixed JavaScript code
        
        Performs basic validation on the fixed code
        """
        # Check for common JavaScript syntax errors
        if self._has_unmatched_brackets(fixed_code):
            return fixed_code + "\n\n// Note: The fixed code may have unmatched brackets"
        
        return fixed_code
    
    def _has_unmatched_brackets(self, code: str) -> bool:
        """
        Check if the code has unmatched brackets
        """
        stack = []
        brackets = {')': '(', '}': '{', ']': '['}
        
        for char in code:
            if char in '({[':
                stack.append(char)
            elif char in ')}]':
                if not stack or stack.pop() != brackets[char]:
                    return True
        
        return len(stack) > 0 