"""Configuration loader and manager."""
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigLoader:
    """Load, validate, and access configuration values."""
    
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Example:
            config.get("android.adb_path")
        """
        keys = key.split(".")
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get an entire configuration section."""
        return self.config.get(section, {})
    
    def save(self, path: Optional[str] = None) -> None:
        """Save current configuration to file."""
        save_path = Path(path) if path else self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
    
    def validate(self, required_keys: list) -> list:
        """Validate that required configuration keys exist."""
        missing = []
        for key in required_keys:
            if self.get(key) is None:
                missing.append(key)
        return missing