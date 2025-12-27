from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserQueryBase(BaseModel):
    session_id: UUID
    query_text: str
    book_id: UUID
    is_highlighted_query: Optional[bool] = False

class UserQueryCreate(UserQueryBase):
    user_id: Optional[UUID] = None

class UserQueryUpdate(BaseModel):
    query_text: Optional[str] = None
    is_highlighted_query: Optional[bool] = None

class UserQuery(UserQueryBase):
    query_id: UUID
    query_timestamp: datetime
    user_id: Optional[UUID] = None
    source_chunks: Optional[List[UUID]] = []

    class Config:
        from_attributes = True