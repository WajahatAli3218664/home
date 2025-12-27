from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgressSchema(BaseModel):
    id: int
    user_id: int
    chapter_id: int
    progress: float
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgressUpdateRequest(BaseModel):
    chapter_id: int
    progress: float