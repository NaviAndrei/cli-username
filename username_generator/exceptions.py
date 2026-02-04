class UsernameGeneratorError(Exception):
    """Base exception class for the Username Generator package."""
    pass

class ConfigError(UsernameGeneratorError):
    """Raised when there is an issue loading or parsing the configuration."""
    pass

class ValidationError(UsernameGeneratorError):
    """Raised when input parameters are invalid (e.g., non-existent profession/vibe)."""
    pass
