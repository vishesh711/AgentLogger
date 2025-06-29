from typing import List

from app.models.schemas.analysis import CodeIssue


class BaseParser:
    """Base class for language-specific code parsers"""
    
    def __init__(self):
        """Initialize the parser"""
        pass
    
    def preprocess(self, code: str) -> str:
        """
        Preprocess code before analysis
        
        By default, returns the code unchanged
        """
        return code
    
    def process_analysis_results(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """
        Process analysis results
        
        By default, returns the issues unchanged
        """
        return issues
    
    def process_fix_result(self, fixed_code: str) -> str:
        """
        Process fixed code
        
        By default, returns the fixed code unchanged
        """
        return fixed_code 