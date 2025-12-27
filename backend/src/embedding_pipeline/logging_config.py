import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import time
from typing import Callable, Any


def setup_logging(log_level: str = "INFO", log_file: str = "embedding_pipeline.log"):
    """
    Set up logging configuration for the embedding pipeline

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: The file to write logs to
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Create formatter with more detailed information
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Default logger setup
logger = setup_logging()


def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log execution time of functions
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds with error: {str(e)}")
            raise

    return wrapper


def log_processing_status(status: str, details: str = ""):
    """
    Log processing status with timestamp and details

    Args:
        status: The processing status (e.g., "STARTED", "PROGRESS", "COMPLETED", "FAILED")
        details: Additional details about the status
    """
    logger.info(f"PROCESSING_STATUS: {status} - {details}")


def log_metrics(url_count: int = 0, chunk_count: int = 0, embedding_count: int = 0,
                success_count: int = 0, failure_count: int = 0):
    """
    Log processing metrics

    Args:
        url_count: Number of URLs processed
        chunk_count: Number of text chunks created
        embedding_count: Number of embeddings generated
        success_count: Number of successful operations
        failure_count: Number of failed operations
    """
    logger.info(f"PROCESSING_METRICS - URLs: {url_count}, Chunks: {chunk_count}, "
                f"Embeddings: {embedding_count}, Success: {success_count}, Failures: {failure_count}")