from typing import Dict, Any, Optional
from pydantic import BaseModel


class RetrievedContext(BaseModel):
    """
    Text data retrieved from Qdrant vector database that should be included in the LLM prompt
    """
    id: str
    content: str  # The actual text content retrieved from the vector database
    source_document: str  # Reference to the original document/chapter
    similarity_score: float  # Score indicating relevance to the query
    metadata: Optional[Dict[str, Any]] = None  # Additional information about the context chunk