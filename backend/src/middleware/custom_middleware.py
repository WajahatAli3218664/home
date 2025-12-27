from typing import Callable
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse


# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        start_time = time.time()
        
        # Log incoming request
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Process the request
        response = await call_next(request)
        
        # Calculate process time
        process_time = time.time() - start_time
        
        # Add process time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        logger.info(f"Response status: {response.status_code}, Process time: {process_time:.4f}s")
        
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authentication globally."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        # Add authentication logic if needed
        # This is a placeholder for more complex auth middleware
        response = await call_next(request)
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request size."""
    
    def __init__(self, app, max_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        if request.headers.get('content-length'):
            content_length = int(request.headers['content-length'])
            if content_length > self.max_size:
                return StarletteResponse(
                    status_code=413,
                    content="Request too large"
                )
        
        response = await call_next(request)
        return response