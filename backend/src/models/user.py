from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.database import Base

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: Optional[str] = None
    auth_provider: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    preferences: Optional[dict] = None

class User(UserBase):
    user_id: UUID
    name: Optional[str] = None
    auth_provider: str
    created_at: datetime
    preferences: Optional[dict] = None

    class Config:
        from_attributes = True


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    background_level = Column(String(50), default="intermediate")
    ai_experience = Column(String(100), nullable=True)
    programming_level = Column(String(100), nullable=True)
    gpu_available = Column(Boolean, default=False)
    ram_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)