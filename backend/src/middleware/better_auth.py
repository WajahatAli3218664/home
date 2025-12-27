"""
Better Auth integration for FastAPI backend
This module provides authentication dependency for FastAPI endpoints
that validates Better Auth session tokens.
"""
import os
import httpx
from datetime import datetime
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any


# Get Better Auth API endpoint from environment
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:8000/auth")  # Default to the auth API endpoint


security = HTTPBearer()


class SessionData(BaseModel):
    """Represents the session data extracted from Better Auth token"""
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None


async def verify_better_auth_token(token: str) -> SessionData:
    """
    Verify a Better Auth token by calling the Better Auth API.
    This is the proper way to validate Better Auth tokens in a backend service.
    """
    try:
        # Make a request to Better Auth's session validation endpoint
        # This would typically be: GET /api/session with Authorization header
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{BETTER_AUTH_URL}/session",  # Better Auth's session validation endpoint
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired authentication token"
                )

            session_data = response.json()

            # Extract user information from the session
            user_info = session_data.get("user", {})
            user_id = user_info.get("id")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session: missing user identifier"
                )

            # Create SessionData object
            return SessionData(
                user_id=str(user_id),
                username=user_info.get("name"),
                email=user_info.get("email"),
                expires_at=None  # Better Auth will handle expiration internally
            )

    except httpx.RequestError:
        # Network error when trying to contact Better Auth
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify authentication token. Please try again later."
        )
    except Exception as e:
        # Any other error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication verification failed: {str(e)}"
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> SessionData:
    """
    Dependency to get current authenticated user from Better Auth token
    """
    token = credentials.credentials
    return await verify_better_auth_token(token)