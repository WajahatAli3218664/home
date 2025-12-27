from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .retrieved_context import RetrievedContext


class LLMPrompt(BaseModel):
    """
    The input sent to the Qwen LLM that should contain both user query and retrieved context
    """
    id: str
    user_query: str  # The original query from the user
    retrieved_context: List[RetrievedContext]  # Array of retrieved context objects
    formatted_prompt: str  # The final prompt string sent to the LLM
    timestamp: datetime  # When the prompt was created