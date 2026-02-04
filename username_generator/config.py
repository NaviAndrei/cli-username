import json
import os
from pathlib import Path
from typing import Dict, Any
from functools import lru_cache
from .exceptions import ConfigError

# Default internal configuration used if external file is missing or broken
DEFAULT_CONFIG = {
    "leet_map": {
        'a': '4', 'e': '3', 'g': '6', 'i': '1', 'o': '0', 's': '5', 't': '7',
        'A': '4', 'E': '3', 'G': '6', 'I': '1', 'O': '0', 'S': '5', 'T': '7',
    },
    "prefixes": ["Cyber", "Master", "The", "Alpha", "Dark", "Ghost"],
    "suffixes": ["Ninja", "Pro", "X", "Tech", "Hunter", "Lord"],
    "retro_words": {
        "adjectives": ["Cyber", "Mega", "Extreme", "Digital", "Pixel", "Turbo"],
        "nouns": ["Warrior", "Knight", "Lord", "Master", "Dude", "Gamer"]
    },
    "vibes": {},
    "professions": {},
    "special_chars": "!@#$%^&*"
}

@lru_cache(maxsize=1)
def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Loads external configuration from a JSON file.
    
    Uses high-performance caching (lru_cache) to prevent repeated disk I/O.
    The function looks for the file in the project's root directory.
    
    Args:
        config_path: Name of the configuration file.
        
    Returns:
        Dict[str, Any]: The loaded configuration dictionary.
        
    Raises:
        ConfigError: If JSON is malformed or file reading fails.
    """
    # Navigate up from current package to find config.json in the project root
    base_dir = Path(__file__).resolve().parent.parent
    full_path = base_dir / config_path

    if not full_path.exists():
        # Fallback to internal defaults if external config is missing
        return DEFAULT_CONFIG

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Failed to parse {config_path}: {e}")
    except Exception as e:
        raise ConfigError(f"Unexpected error reading configuration: {e}")

def get_config_value(key: str, default: Any = None) -> Any:
    """Retrieves a specific value from the configuration.
    
    Args:
        key: The configuration key to look for.
        default: Fallback value if key is not found.
        
    Returns:
        Any: The value from the config or the default provided.
    """
    config = load_config()
    return config.get(key, default)
