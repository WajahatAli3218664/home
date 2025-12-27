from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta

from ..database.session import get_session
from ..database.models import User as DatabaseUser
from ..auth.models import UserRegisterRequest, UserLoginRequest, Token, TokenData
from ..auth.service import AuthService
from ..auth.password_hash import verify_password
from ..config.settings import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


@router.post("/register", response_model=Token)
async def register(user: UserRegisterRequest, db: Session = Depends(get_session)):
    """Register a new user with background information."""
    auth_service = AuthService(db)
    db_user = await auth_service.register_user(user)

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email, "user_id": str(db_user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signup", response_model=Token)
async def signup(user: UserRegisterRequest, db: Session = Depends(get_session)):
    """Register a new user with background information (alias for register)."""
    # This is an alias for the register endpoint to match frontend expectations
    auth_service = AuthService(db)
    db_user = await auth_service.register_user(user)

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email, "user_id": str(db_user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Authenticate user and return access token."""
    auth_service = AuthService(db)

    # For login, we need to handle email/username and password
    user = auth_service.get_user_by_email(form_data.username)  # form_data.username contains the email

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Authenticate user and return access token (alias for login)."""
    # This is an alias for the login endpoint to match frontend expectations
    auth_service = AuthService(db)

    # For login, we need to handle email/username and password
    user = auth_service.get_user_by_email(form_data.username)  # form_data.username contains the email

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.get("/me")
async def read_users_me(credentials: HTTPBearer = Depends(security), db: Session = Depends(get_session)):
    """Get current user info."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception

    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception

    return {
        "id": str(user.id),
        "email": user.email,
        "programming_level": user.programming_level,
        "ai_experience": user.ai_experience,
        "gpu_available": user.gpu_available,
        "ram_size": user.ram_size,
        "created_at": user.created_at
    }