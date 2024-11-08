# src/utils/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional
from ..config.settings import Settings

class CustomFormatter(logging.Formatter):
    """Custom formatter with color coding for different log levels"""
    
    COLORS = {
        'DEBUG': '\033[0;36m',  # Cyan
        'INFO': '\033[0;32m',   # Green
        'WARNING': '\033[0;33m', # Yellow
        'ERROR': '\033[0;31m',   # Red
        'CRITICAL': '\033[0;37;41m'  # White on Red
    }
    RESET = '\033[0m'

    def format(self, record):
        # Add color to log level if on console
        if hasattr(self, 'use_color') and self.use_color:
            record.levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}{self.RESET}"
        return super().format(record)

def setup_logger(
    name: str,
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logger with both file and console handlers
    
    Args:
        name: Logger name
        log_level: Optional override for log level
        log_file: Optional override for log file path
    
    Returns:
        Configured logger instance
    """
    try:
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level or Settings.LOG_LEVEL)

        # Avoid adding handlers if they already exist
        if logger.handlers:
            return logger

        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        )
        
        console_formatter = CustomFormatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        )
        console_formatter.use_color = True

        # Create and configure file handler
        log_file = log_file or Settings.LOG_FILE
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Rotating file handler (size-based)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        
        # Time-based rotating handler for daily logs
        daily_handler = TimedRotatingFileHandler(
            str(log_dir / f"daily_{datetime.now():%Y-%m-%d}.log"),
            when="midnight",
            interval=1,
            backupCount=30
        )
        daily_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(daily_handler)
        logger.addHandler(console_handler)

        return logger

    except Exception as e:
        # Fallback to basic logging if setup fails
        basic_logger = logging.getLogger(name)
        basic_logger.setLevel(logging.INFO)
        basic_logger.addHandler(logging.StreamHandler(sys.stdout))
        basic_logger.error(f"Error setting up logger: {str(e)}")
        return basic_logger# Logging configuration implementation
