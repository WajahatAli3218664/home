"""
Rate limiting for API endpoints
"""
from fastapi import Request, HTTPException, status
from typing import Dict
from datetime import datetime, timedelta
import time


class RateLimiter:
    """
    Simple in-memory rate limiter
    In production, you would typically use Redis or another distributed store
    """
    
    def __init__(self, requests: int = 10, window: int = 60):
        """
        Initialize rate limiter
        
        Args:
            requests: Number of requests allowed
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log: Dict[str, list] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the identifier is allowed
        
        Args:
            identifier: Unique identifier for the requester (e.g., IP address)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        window_start = now - self.window
        
        # Clean old entries
        if identifier in self.requests_log:
            self.requests_log[identifier] = [
                timestamp for timestamp in self.requests_log[identifier]
                if timestamp > window_start
            ]
        else:
            self.requests_log[identifier] = []
        
        # Check if we've exceeded the limit
        if len(self.requests_log[identifier]) >= self.requests:
            return False
        
        # Add current request to log
        self.requests_log[identifier].append(now)
        return True


# Create a global rate limiter instance
rate_limiter = RateLimiter(requests=30, window=60)  # 30 requests per minute per IP


def check_rate_limit(request: Request) -> bool:
    """
    Check if the request is within rate limits
    
    Args:
        request: The incoming request object
        
    Returns:
        True if request is allowed, raises HTTPException if not
    """
    # Use the client's IP address as the identifier
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    return True