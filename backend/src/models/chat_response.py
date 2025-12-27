"""
Data models for chat responses and related entities
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class QueryType(str, Enum):
    GENERAL = "general"
    SELECTED_TEXT = "selected_text"


class ChatSession(BaseModel):
    """
    Represents a conversation session between a user and the chatbot
    """
    session_id: str
    user_id: Optional[str] = None  # Optional for anonymous sessions
    book_id: str
    created_at: datetime
    updated_at: datetime
    language_preference: str = "en"  # Language preference for the session ('en' or 'ur')
    metadata: Optional[dict] = None


class ChatMessage(BaseModel):
    """
    Represents a single message in the conversation (either user query or bot response)
    """
    message_id: str
    session_id: str
    role: ChatRole
    content: str
    timestamp: datetime
    confidence_level: Optional[ConfidenceLevel] = None
    retrieved_context_ids: Optional[List[str]] = []
    query_type: QueryType = QueryType.GENERAL


class RetrievedContext(BaseModel):
    """
    Represents a chunk of book content retrieved for answering a query
    """
    context_id: str
    book_id: str
    chunk_text: str
    chunk_metadata: Optional[dict] = None  # Additional metadata about the chunk (page number, chapter, etc.)
    similarity_score: float  # Similarity score from vector search (0.0 to 1.0)
    embedding_id: str  # Reference to the vector embedding in Qdrant


class BookContent(BaseModel):
    """
    Represents the book content that the chatbot queries
    """
    book_id: str
    title: str
    author: str
    content_type: str  # Type of content (e.g., "textbook", "manual")
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None  # Additional book metadata


class UserSessionPreference(BaseModel):
    """
    Stores user preferences for the chat session (optional, for personalization)
    """
    preference_id: str
    session_id: str
    language_preference: str = "en"  # Language for responses (default: "en")
    response_style: str = "casual"  # Style of responses (e.g., "formal", "casual", "technical")
    last_selected_text: Optional[str] = None  # Last selected text for context (for continuity)