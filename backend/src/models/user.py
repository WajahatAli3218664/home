from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

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