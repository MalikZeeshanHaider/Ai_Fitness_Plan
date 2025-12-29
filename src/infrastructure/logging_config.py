"""
Logging Configuration Module
=============================

Enterprise-grade logging configuration with file rotation, formatting,
and multiple handlers for different log levels.

Features:
- Colored console output for development
- File rotation to manage log file sizes
- Separate handlers for different log levels
- Structured logging with contextual information
- Performance monitoring capabilities

Author: AI Engineer
Date: December 17, 2025
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
import colorlog
from datetime import datetime


class LoggerConfig:
    """
    Centralized logging configuration for the entire application.
    
    This class follows the Singleton pattern to ensure consistent
    logging configuration across all modules.
    
    Attributes:
        log_dir (Path): Directory where log files are stored
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format (str): Format string for log messages
    """
    
    _instance: Optional['LoggerConfig'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'LoggerConfig':
        """
        Implement Singleton pattern.
        
        Returns:
            LoggerConfig: Single instance of the logger configuration
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize logging configuration (only once)."""
        if not self._initialized:
            self.log_dir: Path = Path("logs")
            self.log_level: str = "INFO"
            self.max_bytes: int = 10 * 1024 * 1024  # 10 MB
            self.backup_count: int = 5
            self.console_output: bool = True
            LoggerConfig._initialized = True
    
    def setup_logging(
        self,
        log_dir: Optional[str] = None,
        log_level: Optional[str] = None,
        console_output: Optional[bool] = None
    ) -> None:
        """
        Setup logging configuration for the application.
        
        Args:
            log_dir: Directory path for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Whether to output logs to console
            
        Note:
            This method should be called once at application startup.
        """
        # Update configuration if parameters provided
        if log_dir:
            self.log_dir = Path(log_dir)
        if log_level:
            self.log_level = log_level.upper()
        if console_output is not None:
            self.console_output = console_output
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.log_level))
        
        # Remove existing handlers to avoid duplicates
        root_logger.handlers.clear()
        
        # Add handlers
        self._add_file_handler(root_logger)
        
        if self.console_output:
            self._add_console_handler(root_logger)
        
        # Log initialization
        logging.info("=" * 80)
        logging.info("AI Gym Workout Recommendation System - Logging Initialized")
        logging.info(f"Log Level: {self.log_level}")
        logging.info(f"Log Directory: {self.log_dir.absolute()}")
        logging.info(f"Timestamp: {datetime.now().isoformat()}")
        logging.info("=" * 80)
    
    def _add_file_handler(self, logger: logging.Logger) -> None:
        """
        Add rotating file handler to logger.
        
        Args:
            logger: Logger instance to add handler to
            
        Note:
            Uses RotatingFileHandler for automatic log rotation
            when file size exceeds max_bytes.
        """
        log_file = self.log_dir / "gym_ai_system.log"
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        
        # Set format for file handler
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, self.log_level))
        
        logger.addHandler(file_handler)
    
    def _add_console_handler(self, logger: logging.Logger) -> None:
        """
        Add colored console handler to logger.
        
        Args:
            logger: Logger instance to add handler to
            
        Note:
            Uses colorlog for colored output in development mode.
        """
        console_handler = colorlog.StreamHandler()
        
        # Set colored format for console
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, self.log_level))
        
        logger.addHandler(console_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance with the specified name.
        
        Args:
            name: Name of the logger (typically __name__ of the module)
            
        Returns:
            logging.Logger: Configured logger instance
            
        Example:
            >>> logger = LoggerConfig.get_logger(__name__)
            >>> logger.info("This is an info message")
        """
        return logging.getLogger(name)


class PerformanceLogger:
    """
    Performance logging utility for monitoring execution time.
    
    This class provides context manager functionality for timing
    code blocks and logging performance metrics.
    
    Example:
        >>> with PerformanceLogger("search_algorithm"):
        ...     result = perform_search()
    """
    
    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        """
        Initialize performance logger.
        
        Args:
            operation_name: Name of the operation being timed
            logger: Logger instance (uses default if not provided)
        """
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)
        self.start_time: Optional[float] = None
    
    def __enter__(self) -> 'PerformanceLogger':
        """Start timing when entering context."""
        import time
        self.start_time = time.time()
        self.logger.debug(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Log elapsed time when exiting context."""
        import time
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            if exc_type is None:
                self.logger.info(
                    f"Operation '{self.operation_name}' completed in {elapsed_time:.4f} seconds"
                )
            else:
                self.logger.error(
                    f"Operation '{self.operation_name}' failed after {elapsed_time:.4f} seconds"
                )


# Module-level convenience function
def setup_logging(
    log_dir: str = "logs",
    log_level: str = "INFO",
    console_output: bool = True
) -> None:
    """
    Convenience function to setup logging configuration.
    
    Args:
        log_dir: Directory path for log files
        log_level: Logging level
        console_output: Whether to output to console
        
    Example:
        >>> from src.infrastructure.logging_config import setup_logging
        >>> setup_logging(log_level="DEBUG")
    """
    config = LoggerConfig()
    config.setup_logging(log_dir, log_level, console_output)


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger instance.
    
    Args:
        name: Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
        
    Example:
        >>> from src.infrastructure.logging_config import get_logger
        >>> logger = get_logger(__name__)
    """
    return LoggerConfig.get_logger(name)
