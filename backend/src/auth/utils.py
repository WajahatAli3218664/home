from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from ..config.settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with the provided data and expiration time"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str):
    """Verify a JWT token and return the payload if valid"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None