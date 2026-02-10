import json
import os
import string
from pathlib import Path
from typing import List, Dict, Union, Any, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# --- Pydantic Models for Validation ---

class RetroWords(BaseModel):
    """Configuration schema for retro style words."""
    adjectives: List[str]
    nouns: List[str]

class VibeCategory(BaseModel):
    """Configuration schema for thematic vibes (e.g., tech, fantasy)."""
    adjectives: List[str]
    nouns: List[str]

class ProfessionCategory(BaseModel):
    """Configuration schema for profession-based words."""
    adjectives: List[str]
    nouns: List[str]

class AppConfig(BaseModel):
    """Main application configuration model (strict schema)."""
    leet_map: Dict[str, Union[str, List[str]]] = Field(default_factory=dict)
    patterns: List[str] = Field(default_factory=list)
    separators: List[str] = Field(default_factory=list)
    prefixes: List[str] = Field(default_factory=list)
    suffixes: List[str] = Field(default_factory=list)
    retro_words: RetroWords
    vibes: Dict[str, Union[VibeCategory, Dict[str, List[str]]]] # Flexible for legacy dict structure
    professions: Dict[str, Union[ProfessionCategory, Dict[str, List[str]]]]
    mythology: Dict[str, List[str]]
    # Legacy fields that might exist
    check_targets: Optional[Dict[str, str]] = None
    
    @model_validator(mode='after')
    def validate_patterns(self):
        """Ensures all patterns contain only valid placeholders ({noun}, {adjective}, {number})."""
        valid_keys = {'noun', 'adjective', 'number'}
        for pattern in self.patterns:
            try:
                # Parse format string to extract keys like {noun}
                keys = [t[1] for t in string.Formatter().parse(pattern) if t[1] is not None]
            except ValueError as e:
                # Invalid format string
                raise ValueError(f"Invalid pattern format '{pattern}': {e}")
                
            for key in keys:
                if key not in valid_keys:
                    raise ValueError(f"Unknown placeholder '{{{key}}}' in pattern '{pattern}'. Valid keys: {valid_keys}")
        return self

# --- Configuration Manager ---

class ConfigManager:
    """Singleton manager for application configuration."""
    _instance = None
    _config: Optional[AppConfig] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def load(self, config_path: str = "config.json"):
        """Loads configuration from JSON and applies environment overrides."""
        # Determine path relative to project root (assuming standard layout)
        # Packages: project/username_generator/config.py
        # Config: project/config.json
        base_dir = Path(__file__).resolve().parent.parent
        path = base_dir / config_path
            
        if not path.exists():
             # Fallback: check current directory
             path = Path(config_path)
             if not path.exists():
                # Allow running with defaults if file missing? 
                # Ideally, we should raise error if config is mandatory.
                # For now, let's assume it must exist as per previous logic.
                raise FileNotFoundError(f"Config file not found at {path.absolute()}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Environment variable overrides (simple generic override)
            # Example: UG_PATTERNS='["{noun}_{number}"]'
            prefix = "UG_"
            for key, value in os.environ.items():
                if key.startswith(prefix):
                    config_key = key[len(prefix):].lower()
                    if config_key in data:
                        try:
                            # Try to parse env var as JSON to support complex types
                            data[config_key] = json.loads(value)
                        except json.JSONDecodeError:
                            # Fallback to string value
                            data[config_key] = value
                            
            # Validate and instantiate Config Model
            self._config = AppConfig(**data)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except ValidationError as e:
            raise ValueError(f"Configuration Validation Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error loading config: {e}")

    @property
    def config(self) -> AppConfig:
        if self._config is None:
            # Auto-load if accessed before explicit load
            self.load()
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value safely (with auto-load)."""
        try:
            if self._config is None:
                 self.load()
            return getattr(self.config, key, default)
        except AttributeError:
            return default

# --- Module Level Interface (Backwards Compatibility) ---

_manager = ConfigManager()

def load_config(path: str = "config.json") -> None:
    """Explicitly reloads configuration from disk."""
    _manager.load(path)

def get_config_value(key: str, default: Any = None) -> Any:
    """Helper: Gets a specific value from the configuration singleton."""
    val = _manager.get(key, default)
    return val if val is not None else default

# Direct access to the Pydantic model
def get_config_model() -> AppConfig:
    """Returns the full Pydantic configuration model instance."""
    return _manager.config
