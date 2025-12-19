"""
Configuration management - UI-agnostic settings.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json


@dataclass
class Config:
    """Application configuration."""
    show_meaning: bool
    
    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create Config from dictionary."""
        return cls(
            show_meaning=data.get("show_meaning", True)
        )
    
    @classmethod
    def load(cls, json_path: Path) -> "Config":
        """Load configuration from JSON file."""
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            # Return default config if file doesn't exist
            return cls(show_meaning=True)
    
    def to_dict(self) -> dict:
        """Convert Config to dictionary."""
        return {
            "show_meaning": self.show_meaning
        }


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from file.
    
    Args:
        config_path: Optional path to config file. If None, uses default location.
    
    Returns:
        Config object
    """
    if config_path is None:
        # Default location: data/config.json relative to project root
        config_path = Path(__file__).parent.parent / "data" / "config.json"
    
    return Config.load(config_path)

