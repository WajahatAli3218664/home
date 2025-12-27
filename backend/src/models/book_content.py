from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class BookContentBase(BaseModel):
    title: str
    author: str
    content: str
    embedding_model: Optional[str] = "MiniLM"
    chunk_size: Optional[int] = 512

class BookContentCreate(BookContentBase):
    pass

class BookContentUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None

class BookContent(BookContentBase):
    book_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True