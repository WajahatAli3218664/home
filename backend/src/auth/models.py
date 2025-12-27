from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    programming_level: str
    ai_experience: str
    gpu_available: bool
    ram_size: str
    created_at: datetime

    class Config:
        from_attributes = True  # This allows the model to work with ORM objects


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserRegisterRequest(BaseModel):
    email: str
    password: str
    programming_level: str
    ai_experience: str
    gpu_available: bool
    ram_size: str