import ast
from typing import List

from app.models.schemas.analysis import CodeIssue
from app.utils.parsing.base_parser import BaseParser


class PythonParser(BaseParser):
    """Python-specific code parser"""
    
    def preprocess(self, code: str) -> str:
        """
        Preprocess Python code before analysis
        
        Removes any leading/trailing whitespace and ensures proper line endings
        """
        return code.strip().replace("\r\n", "\n")
    
    def process_analysis_results(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """
        Process Python-specific analysis results
        
        Validates line numbers and enhances issue descriptions
        """
        processed_issues = []
        
        for issue in issues:
            # Ensure line numbers are valid
            if issue.line_start < 1:
                issue.line_start = 1
            
            if issue.line_end is not None and issue.line_end < issue.line_start:
                issue.line_end = issue.line_start
            
            # Add Python-specific context to certain issue types
            if issue.type == "indentation_error":
                issue.message = f"Indentation error: {issue.message}"
            elif issue.type == "syntax_error":
                issue.message = f"Python syntax error: {issue.message}"
            
            processed_issues.append(issue)
        
        return processed_issues
    
    def process_fix_result(self, fixed_code: str) -> str:
        """
        Process fixed Python code
        
        Validates that the fixed code is syntactically valid Python
        """
        try:
            # Try to parse the fixed code to ensure it's valid Python
            ast.parse(fixed_code)
            return fixed_code
        except SyntaxError:
            # If the fixed code has syntax errors, add a comment
            return fixed_code + "\n\n# Note: The fixed code may still contain syntax errors" 