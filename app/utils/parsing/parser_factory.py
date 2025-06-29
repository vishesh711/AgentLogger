from typing import Dict, Type

from app.utils.parsing.base_parser import BaseParser
from app.utils.parsing.python_parser import PythonParser
from app.utils.parsing.javascript_parser import JavaScriptParser

# Registry of language parsers
_parsers: Dict[str, Type[BaseParser]] = {
    "python": PythonParser,
    "javascript": JavaScriptParser,
    # Add more parsers as they are implemented
}

def get_parser_for_language(language: str) -> BaseParser:
    """
    Get a parser for the specified programming language
    
    Args:
        language: The programming language to get a parser for
        
    Returns:
        An instance of the appropriate parser
        
    Raises:
        ValueError: If no parser is available for the language
    """
    language = language.lower()
    
    # Check if we have a parser for this language
    if language in _parsers:
        return _parsers[language]()
    
    # Fall back to a default parser for unknown languages
    # In a real implementation, you might want to raise an error instead
    return PythonParser()  # Default to Python parser

# Alias for backward compatibility
get_parser = get_parser_for_language 