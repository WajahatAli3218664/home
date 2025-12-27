from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class ChatRequest(BaseModel):
    query: str  # Changed to match the actual schema used by the RAG service

class ChatResponse(BaseModel):
    response: str
    timestamp: Optional[datetime] = None  # Added timestamp to match schema

@router.post("/chat/")
async def simple_chat(request: ChatRequest):
    """
    Simple chat endpoint that echoes back the user's message with a prefix.
    This is a minimal example to demonstrate the endpoint working.
    """
    return ChatResponse(
        response=f"Echo: {request.query}. This is a simple response from the chat endpoint.",
        timestamp=datetime.now()
    )