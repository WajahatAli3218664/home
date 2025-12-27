from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class VectorEmbeddingBase(BaseModel):
    book_id: str
    content_chunk: str
    embedding_vector: List[float]
    chapter: Optional[str] = None
    section: Optional[str] = None
    page: Optional[str] = None
    language: str = "en"
    source: str = "book"
    metadata: Optional[dict] = None

class VectorEmbeddingCreate(VectorEmbeddingBase):
    pass

class VectorEmbeddingUpdate(BaseModel):
    content_chunk: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page: Optional[str] = None
    language: Optional[str] = None
    metadata: Optional[dict] = None

class VectorEmbedding(VectorEmbeddingBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True