import time
from typing import Dict
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize rate limiter
        
        :param max_requests: Maximum number of requests allowed
        :param window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed
        
        :param identifier: Unique identifier for the requester (e.g., user ID or IP)
        :return: True if allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.window_size
        ]
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < self.max_requests:
            # Add current request
            self.requests[identifier].append(current_time)
            return True
        
        return False