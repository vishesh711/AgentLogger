import ast
import re
from typing import Dict, List, Any

from app.models.schemas.analysis import CodeIssue
from app.utils.parsing.base_parser import BaseParser


class PythonParser(BaseParser):
    """
    Parser for Python code
    """
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code and extract structure information
        
        Args:
            code: Python source code to parse
            
        Returns:
            Dictionary with parsed information
        """
        result = super().parse(code)
        
        try:
            # Parse the code using ast
            tree = ast.parse(code)
            
            # Extract functions and classes
            result["functions"] = self.extract_functions(code)
            result["classes"] = self.extract_classes(code)
            result["imports"] = self.identify_imports(code)
            
            # Add more Python-specific information
            result["ast_type"] = type(tree).__name__
            
        except SyntaxError as e:
            # Handle syntax errors
            result["error"] = {
                "type": "SyntaxError",
                "message": str(e),
                "line": e.lineno,
                "column": e.offset
            }
        
        return result
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract functions from Python code
        
        Args:
            code: Python source code to analyze
            
        Returns:
            List of dictionaries with function information
        """
        functions = []
        
        try:
            tree = ast.parse(code)
            
            # Find all function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [
                            ast.unparse(decorator) for decorator in node.decorator_list
                        ] if hasattr(ast, "unparse") else []  # ast.unparse is Python 3.9+
                    })
        
        except SyntaxError:
            # If there's a syntax error, return an empty list
            pass
        
        return functions
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract classes from Python code
        
        Args:
            code: Python source code to analyze
            
        Returns:
            List of dictionaries with class information
        """
        classes = []
        
        try:
            tree = ast.parse(code)
            
            # Find all class definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Get methods in the class
                    methods = []
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            methods.append(child.name)
                    
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods,
                        "bases": [
                            ast.unparse(base) for base in node.bases
                        ] if hasattr(ast, "unparse") else []  # ast.unparse is Python 3.9+
                    })
        
        except SyntaxError:
            # If there's a syntax error, return an empty list
            pass
        
        return classes
    
    def identify_imports(self, code: str) -> List[str]:
        """
        Identify imports in Python code
        
        Args:
            code: Python source code to analyze
            
        Returns:
            List of import statements
        """
        imports = []
        
        try:
            tree = ast.parse(code)
            
            # Find all import statements
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(f"import {name.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for name in node.names:
                        imports.append(f"from {module} import {name.name}")
        
        except SyntaxError:
            # If there's a syntax error, try regex-based approach
            import_pattern = r"^\s*(from\s+[\w.]+\s+import\s+[\w.*,\s]+|import\s+[\w.,\s]+)"
            imports = [line.strip() for line in code.splitlines() 
                      if re.match(import_pattern, line)]
        
        return imports
    
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

    def get_syntax_issues(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract Python-specific syntax issues from parsed data
        
        Args:
            parsed_data: Dictionary with parsed information from parse() method
            
        Returns:
            List of syntax issues found in the Python code
        """
        issues = []
        
        # Check if there's a syntax error in the parsed data
        if "error" in parsed_data:
            error = parsed_data["error"]
            issues.append({
                "message": error.get("message", "Python syntax error"),
                "line": error.get("line", 1),
                "column": error.get("column", 1),
                "type": error.get("type", "SyntaxError")
            })
        
        return issues 