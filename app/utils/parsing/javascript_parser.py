import re
from typing import Dict, List, Any

from app.models.schemas.analysis import CodeIssue
from app.utils.parsing.base_parser import BaseParser


class JavaScriptParser(BaseParser):
    """
    Parser for JavaScript code
    """
    
    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse JavaScript code and extract structure information
        
        Args:
            code: JavaScript source code to parse
            
        Returns:
            Dictionary with parsed information
        """
        result = super().parse(code)
        
        # Extract functions and classes
        result["functions"] = self.extract_functions(code)
        result["classes"] = self.extract_classes(code)
        result["imports"] = self.identify_imports(code)
        
        return result
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract functions from JavaScript code using regex
        
        Args:
            code: JavaScript source code to analyze
            
        Returns:
            List of dictionaries with function information
        """
        functions = []
        
        # Regular function declarations
        func_pattern = r"function\s+(\w+)\s*\((.*?)\)"
        for match in re.finditer(func_pattern, code):
            name = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
            line = code[:match.start()].count("\n") + 1
            
            functions.append({
                "name": name,
                "line": line,
                "args": args,
                "type": "function"
            })
        
        # Arrow functions with explicit names
        arrow_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*(?:\((.*?)\)|(\w+))\s*=>"
        for match in re.finditer(arrow_pattern, code):
            name = match.group(1)
            args_group = match.group(2) or match.group(3) or ""
            args = [arg.strip() for arg in args_group.split(",") if arg.strip()]
            line = code[:match.start()].count("\n") + 1
            
            functions.append({
                "name": name,
                "line": line,
                "args": args,
                "type": "arrow"
            })
        
        # Method definitions in classes or objects
        method_pattern = r"(\w+)\s*\((.*?)\)\s*\{"
        for match in re.finditer(method_pattern, code):
            # Exclude if/for/while statements
            prev_chars = code[max(0, match.start() - 10):match.start()].strip()
            if prev_chars.endswith("if") or prev_chars.endswith("for") or prev_chars.endswith("while"):
                continue
                
            name = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
            line = code[:match.start()].count("\n") + 1
            
            functions.append({
                "name": name,
                "line": line,
                "args": args,
                "type": "method"
            })
        
        return functions
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract classes from JavaScript code using regex
        
        Args:
            code: JavaScript source code to analyze
            
        Returns:
            List of dictionaries with class information
        """
        classes = []
        
        # ES6 class declarations
        class_pattern = r"class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{"
        for match in re.finditer(class_pattern, code):
            name = match.group(1)
            parent = match.group(2)
            line = code[:match.start()].count("\n") + 1
            
            # Find the class body
            start_pos = match.end()
            brace_count = 1
            end_pos = start_pos
            
            for i in range(start_pos, len(code)):
                if code[i] == "{":
                    brace_count += 1
                elif code[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break
            
            class_body = code[start_pos:end_pos]
            
            # Extract methods from the class body
            method_pattern = r"(\w+)\s*\((.*?)\)\s*\{"
            methods = []
            for method_match in re.finditer(method_pattern, class_body):
                methods.append(method_match.group(1))
            
            classes.append({
                "name": name,
                "line": line,
                "parent": parent,
                "methods": methods
            })
        
        return classes
    
    def identify_imports(self, code: str) -> List[str]:
        """
        Identify imports in JavaScript code
        
        Args:
            code: JavaScript source code to analyze
            
        Returns:
            List of import statements
        """
        imports = []
        
        # ES6 imports
        import_pattern = r"import\s+(?:{[^}]*}|[^{;]*)?\s*from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(import_pattern, code):
            imports.append(match.group(0).strip())
        
        # CommonJS requires
        require_pattern = r"(?:const|let|var)\s+(?:{[^}]*}|\w+)\s*=\s*require\(['\"]([^'\"]+)['\"]"
        for match in re.finditer(require_pattern, code):
            imports.append(match.group(0).strip())
        
        return imports
    
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

    def get_syntax_issues(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract JavaScript-specific syntax issues from parsed data
        
        Args:
            parsed_data: Dictionary with parsed information from parse() method
            
        Returns:
            List of syntax issues found in the JavaScript code
        """
        issues = []
        
        # Check if there's an error in the parsed data
        if "error" in parsed_data:
            error = parsed_data["error"]
            issues.append({
                "message": error.get("message", "JavaScript syntax error"),
                "line": error.get("line", 1),
                "column": error.get("column", 1),
                "type": error.get("type", "SyntaxError")
            })
        
        return issues 