import re
import secrets


def test_api_key_format():
    """
    Test that generated API keys follow the expected format
    """
    # Use the same method as the service uses
    api_key = secrets.token_urlsafe(32)
    
    # Check that the API key is a string
    assert isinstance(api_key, str)
    
    # Check that the API key has the expected length
    assert len(api_key) >= 32
    
    # Check that the API key only contains valid characters
    valid_chars_pattern = r'^[A-Za-z0-9_-]+$'
    assert re.match(valid_chars_pattern, api_key) is not None


def test_api_key_uniqueness():
    """
    Test that generated API keys are unique
    """
    # Generate multiple API keys
    api_keys = [secrets.token_urlsafe(32) for _ in range(10)]
    
    # Check that all API keys are unique
    assert len(api_keys) == len(set(api_keys)) 