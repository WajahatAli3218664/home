"""
Data models for AI responses and related entities
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class GroundingStatus(str, Enum):
    VALID = "Valid"
    NOT_FOUND = "Not Found"
    EXTERNAL = "External"


class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TextbookContent(BaseModel):
    """
    Represents the textbook content that the AI assistant queries
    """
    content_id: str
    book_id: str
    chapter: str
    section: str
    page_number: int
    content_text: str
    embedding_id: str
    metadata: Optional[dict] = None


class UserQuery(BaseModel):
    """
    Represents a question or input from the reader that triggers the AI process
    """
    query_id: str
    session_id: str
    query_text: str
    timestamp: datetime
    selected_text: Optional[str] = None
    source_context: Optional[str] = None


class RetrievedContext(BaseModel):
    """
    Represents a chunk of textbook content retrieved for answering a query
    """
    context_id: str
    query_id: str
    content_id: str
    text_chunk: str
    similarity_score: float  # Similarity score from vector search (0.0 to 1.0)
    chapter: str
    section: str
    page_number: int


class AIResponse(BaseModel):
    """
    Represents the generated answer from the AI assistant based on the retrieved context
    """
    response_id: str
    query_id: str
    response_text: str
    timestamp: datetime
    citations: List[str]  # List of citations used in the response
    confidence_level: ConfidenceLevel
    grounding_status: GroundingStatus


class Citation(BaseModel):
    """
    Represents the reference information that indicates the source of the answer within the textbook
    """
    citation_id: str
    response_id: str
    content_id: str
    chapter: str
    section: str
    page_number: int
    citation_format: str  # The formatted citation string


class UserSession(BaseModel):
    """
    Represents a user's interaction session with the AI assistant
    """
    session_id: str
    user_id: Optional[str] = None  # Optional for anonymous sessions
    book_id: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None