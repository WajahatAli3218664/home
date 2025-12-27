from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserSessionBase(BaseModel):
    book_id: UUID
    is_active: Optional[bool] = True

class UserSessionCreate(UserSessionBase):
    user_id: Optional[UUID] = None

class UserSessionUpdate(BaseModel):
    is_active: Optional[bool] = None
    session_end: Optional[datetime] = None

class UserSession(UserSessionBase):
    session_id: UUID
    session_start: datetime
    session_end: Optional[datetime] = None
    user_id: Optional[UUID] = None
    conversation_history: Optional[str] = None  # JSON string representation

    class Config:
        from_attributes = True