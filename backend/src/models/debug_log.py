from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class DebugLog(BaseModel):
    """
    Log entries for debugging the context flow
    """
    id: str
    timestamp: datetime
    component: str  # Which component generated the log (e.g., RAG Service, Context Retrieval)
    message: str
    context_snapshot: Optional[Dict[str, Any]] = None  # Snapshot of relevant context at the time of logging
    level: str = "info"  # Log level (info, warning, error)