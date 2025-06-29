from app.utils.parsing.base_parser import BaseParser
from app.utils.parsing.python_parser import PythonParser
from app.utils.parsing.javascript_parser import JavaScriptParser


def get_parser_for_language(language: str) -> BaseParser:
    """
    Get the appropriate parser for a language
    
    Args:
        language: Programming language name (e.g., 'python', 'javascript')
    
    Returns:
        A parser instance for the specified language
    
    Raises:
        ValueError: If the language is not supported
    """
    language = language.lower()
    
    if language in ["python", "py"]:
        return PythonParser()
    elif language in ["javascript", "js", "typescript", "ts"]:
        return JavaScriptParser()
    else:
        # For unsupported languages, return the base parser
        return BaseParser() 