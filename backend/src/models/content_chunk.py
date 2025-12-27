from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ContentChunkBase(BaseModel):
    book_id: UUID
    chunk_text: str
    chunk_index: int
    embedding_vector: List[float]
    metadata: Optional[dict] = None

class ContentChunkCreate(ContentChunkBase):
    pass

class ContentChunkUpdate(BaseModel):
    chunk_text: Optional[str] = None
    chunk_index: Optional[int] = None
    embedding_vector: Optional[List[float]] = None
    metadata: Optional[dict] = None

class ContentChunk(ContentChunkBase):
    chunk_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True