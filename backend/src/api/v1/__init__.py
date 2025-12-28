"""
API v1 package initialization.
Expose `router` for easy inclusion by the application.
"""
from ..routers import api_router as router

__all__ = ["router"]