from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatInput(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str
    timestamp: Optional[datetime] = None


class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    query: str
    response: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True