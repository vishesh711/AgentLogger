from typing import Dict, List, Any

from app.models.schemas.analysis import CodeIssue


class BaseParser:
    """
    Base class for language-specific code parsers
    
    This class provides the interface for all language parsers and
    default implementations for common methods.
    """
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse code and extract structure information
        
        Args:
            code: Source code to parse
            
        Returns:
            Dictionary with parsed information
        """
        # Base implementation just returns basic info
        return {
            "lines": len(code.splitlines()),
            "chars": len(code),
            "tokens": []
        }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract functions/methods from code
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of dictionaries with function information
        """
        # Base implementation returns empty list
        return []
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract classes from code
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of dictionaries with class information
        """
        # Base implementation returns empty list
        return []
    
    def identify_imports(self, code: str) -> List[str]:
        """
        Identify imports in the code
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of import statements
        """
        # Base implementation returns empty list
        return []
    
    def preprocess(self, code: str) -> str:
        """
        Preprocess code before analysis
        
        Args:
            code: Source code to preprocess
            
        Returns:
            Preprocessed code
        """
        # Base implementation returns code unchanged
        return code
    
    def process_analysis_results(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """
        Process analysis results
        
        By default, returns the issues unchanged
        """
        return issues
    
    def process_fix_result(self, fixed_code: str) -> str:
        """
        Process fixed code after generation
        
        Args:
            fixed_code: Generated fixed code
            
        Returns:
            Processed fixed code
        """
        # Base implementation returns code unchanged
        return fixed_code

    def get_syntax_issues(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract syntax issues from parsed data
        
        Args:
            parsed_data: Dictionary with parsed information from parse() method
            
        Returns:
            List of syntax issues found in the code
        """
        issues = []
        
        # Check if there's an error in the parsed data
        if "error" in parsed_data:
            error = parsed_data["error"]
            issues.append({
                "message": error.get("message", "Syntax error"),
                "line": error.get("line", 1),
                "column": error.get("column", 1),
                "type": error.get("type", "SyntaxError")
            })
        
        return issues 