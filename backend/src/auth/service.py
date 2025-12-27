from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends
from typing import Optional
from datetime import datetime
from uuid import UUID

from ..database.models import User
from ..auth.password_hash import get_password_hash
from ..database.session import get_session
from ..auth.models import UserRegisterRequest


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def register_user(self, user_data: UserRegisterRequest) -> User:
        """Register a new user with profile information"""
        # Check if user already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user instance with all required fields
        db_user = User(
            email=user_data.email,
            username=user_data.email.split('@')[0],  # Use email prefix as username for now
            programming_level=user_data.programming_level,
            ai_experience=user_data.ai_experience,
            software_experience="",  # Default empty - can be updated through profile
            hardware_background="",  # Default empty - can be updated through profile
            gpu_available=user_data.gpu_available,
            ram_size=user_data.ram_size,
            password_hash=hashed_password,
            created_at=datetime.utcnow()
        )

        # Add to database
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        from sqlmodel import select
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not self.verify_password(password, user.password_hash):
            return None

        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        from .password_hash import verify_password
        return verify_password(plain_password, hashed_password)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        from sqlmodel import select
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        return user

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        user = self.session.get(User, user_id)

        return user

    def update_user_profile(self, user_id: UUID, **updates) -> Optional[User]:
        """Update a user's profile information"""
        user = self.session.get(User, user_id)
        if not user:
            return None

        # Update only the fields that are provided
        for field, value in updates.items():
            if hasattr(user, field):
                setattr(user, field, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user