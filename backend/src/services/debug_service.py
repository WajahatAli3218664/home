from typing import Dict, Any, List, Optional
from datetime import datetime
from ..models.debug_log import DebugLog
from ..config.logging import log_context_flow


class DebugService:
    """
    Service for debugging context flow in the RAG system
    """
    
    def __init__(self):
        self.recent_contexts: List[Dict[str, Any]] = []
        self.max_stored_contexts = 10  # Keep last 10 contexts for debugging
    
    def log_context_flow(
        self,
        component: str,
        message: str,
        context_data: Optional[Dict[str, Any]] = None,
        level: str = "info"
    ) -> DebugLog:
        """
        Log context flow information
        """
        log_entry = log_context_flow(component, message, context_data, level)
        
        # Store recent contexts for debugging endpoint
        if context_data:
            context_entry = {
                "timestamp": log_entry.timestamp,
                "user_query": context_data.get("query", context_data.get("user_query", "")),
                "retrieved_context": context_data.get("retrieved_context", []),
                "retrieved_contexts_count": context_data.get("retrieved_contexts_count", 0),
                "context_str_preview": context_data.get("context_str_preview", ""),
                "context_str_length": context_data.get("context_str_length", 0),
                "formatted_prompt": context_data.get("formatted_prompt", context_data.get("context_str_preview", "")),
                "llm_response": context_data.get("llm_response", context_data.get("llm_response_preview", "")),
                "llm_response_length": context_data.get("llm_response_length", 0),
                "final_response_preview": context_data.get("final_response_preview", ""),
                "confidence_level": context_data.get("confidence_level", ""),
                "retrieved_context_count": context_data.get("retrieved_context_count", 0),
                "selected_text": context_data.get("selected_text", ""),
                "book_id": context_data.get("book_id", ""),
                "session_id": context_data.get("session_id", "")
            }

            self.recent_contexts.append(context_entry)

            # Keep only the most recent contexts
            if len(self.recent_contexts) > self.max_stored_contexts:
                self.recent_contexts.pop(0)
        
        return log_entry
    
    def get_recent_contexts(self) -> List[Dict[str, Any]]:
        """
        Get the most recently stored contexts
        """
        return self.recent_contexts
    
    def get_latest_context(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recently stored context
        """
        if self.recent_contexts:
            return self.recent_contexts[-1]
        return None
    
    def clear_recent_contexts(self):
        """
        Clear the stored recent contexts
        """
        self.recent_contexts.clear()