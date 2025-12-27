import time
import random
from functools import wraps
from typing import Callable, Type, Tuple, Any
from .logging_config import logger


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0, 
                     exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """
    Decorator to retry a function on failure

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (in seconds)
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exception types to retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):  # +1 to include the initial attempt
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:  # Don't log if this is the last attempt
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                                       f"Retrying in {current_delay} seconds...")
                        time.sleep(current_delay)
                        # Exponential backoff with jitter
                        current_delay *= backoff
                        current_delay *= (0.5 + random.random())  # Add jitter to prevent thundering herd
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}")
            
            # If all retries are exhausted, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator


def handle_api_call(func: Callable) -> Callable:
    """
    Decorator to handle API calls with proper error handling and logging
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.debug(f"API call to {func.__name__} was successful")
            return result
        except Exception as e:
            logger.error(f"API call to {func.__name__} failed: {str(e)}")
            # Re-raise the exception to be handled by the calling function
            raise
    
    return wrapper