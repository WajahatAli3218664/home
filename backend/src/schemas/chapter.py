from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChapterSchema(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    version: Optional[str] = '1.0.0'
    position: int
    word_count: Optional[int] = 0
    estimated_reading_time: Optional[int] = 0  # in minutes
    metadata: Optional[str] = None  # JSON string for additional metadata

    class Config:
        from_attributes = True