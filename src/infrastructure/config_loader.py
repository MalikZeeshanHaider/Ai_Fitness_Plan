"""
Configuration Loader Module
============================

Loads and validates configuration from YAML files and environment variables.
Provides type-safe access to configuration values.

Features:
- YAML configuration loading
- Environment variable override
- Type validation
- Default value handling
- Singleton pattern for global config access

Author: AI Engineer
Date: December 17, 2025
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from dotenv import load_dotenv


class ConfigLoader:
    """
    Configuration loader with environment variable support.
    
    This class implements the Singleton pattern to ensure
    consistent configuration across the application.
    
    Attributes:
        config (Dict): Loaded configuration dictionary
        config_path (Path): Path to configuration file
    """
    
    _instance: Optional['ConfigLoader'] = None
    _config: Optional[Dict[str, Any]] = None
    
    def __new__(cls) -> 'ConfigLoader':
        """
        Implement Singleton pattern.
        
        Returns:
            ConfigLoader: Single instance of configuration loader
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to YAML configuration file
        """
        if self._config is None:
            # Load environment variables
            load_dotenv()
            
            # Determine config path
            if config_path is None:
                config_path = os.getenv('CONFIG_PATH', 'config/config.yaml')
            
            self.config_path = Path(config_path)
            self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from YAML file.
        
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as file:
            self._config = yaml.safe_load(file)
        
        # Override with environment variables
        self._apply_env_overrides()
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        # Log level override
        if log_level := os.getenv('LOG_LEVEL'):
            if self._config and 'logging' in self._config:
                self._config['logging']['level'] = log_level
        
        # Data directory override
        if data_dir := os.getenv('DATA_DIR'):
            if self._config and 'data' in self._config:
                self._config['data']['dataset_path'] = f"{data_dir}/GymDataset.csv"
        
        # Debug mode override
        if app_debug := os.getenv('APP_DEBUG'):
            if self._config and 'application' in self._config:
                self._config['application']['debug_mode'] = app_debug.lower() == 'true'
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key path.
        
        Args:
            key: Dot-separated key path (e.g., 'logging.level')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config = ConfigLoader()
            >>> log_level = config.get('logging.level', 'INFO')
        """
        if self._config is None:
            return default
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., 'agents', 'search')
            
        Returns:
            Dictionary containing section configuration
            
        Example:
            >>> config = ConfigLoader()
            >>> agent_config = config.get_section('agents')
        """
        if self._config is None:
            return {}
        
        return self._config.get(section, {})
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    @property
    def config(self) -> Dict[str, Any]:
        """
        Get full configuration dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config or {}


# Module-level convenience functions
_config_instance: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """
    Get global configuration instance.
    
    Returns:
        ConfigLoader: Global configuration loader
        
    Example:
        >>> from src.infrastructure.config_loader import get_config
        >>> config = get_config()
        >>> log_level = config.get('logging.level')
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Convenience function to get configuration value.
    
    Args:
        key: Dot-separated key path
        default: Default value if key not found
        
    Returns:
        Configuration value or default
        
    Example:
        >>> from src.infrastructure.config_loader import get_config_value
        >>> max_exercises = get_config_value('workout_plan.max_exercises', 12)
    """
    return get_config().get(key, default)
