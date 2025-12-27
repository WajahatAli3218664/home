"""
Logging for debugging and monitoring
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Name of the logger
        log_file: Path to the log file (optional, defaults to logs/app.log)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    if log_file is None:
        log_file = logs_dir / "app.log"
    else:
        log_file = logs_dir / log_file
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create a default logger for the application
app_logger = setup_logger("rag_chatbot", "rag_chatbot.log")


def log_api_call(endpoint: str, method: str, user_id: str = None, session_id: str = None):
    """
    Log an API call
    
    Args:
        endpoint: The API endpoint that was called
        method: The HTTP method used
        user_id: Optional user ID
        session_id: Optional session ID
    """
    app_logger.info(f"API Call: {method} {endpoint} | User: {user_id} | Session: {session_id}")


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    app_logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_performance(start_time: datetime, endpoint: str, execution_time: float):
    """
    Log performance metrics
    
    Args:
        start_time: When the operation started
        endpoint: The endpoint that was called
        execution_time: How long the operation took in seconds
    """
    app_logger.info(f"Performance: {endpoint} executed in {execution_time:.4f}s")


# Export the main logger
logger = app_logger