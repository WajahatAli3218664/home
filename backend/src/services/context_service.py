"""
Context tracking for multi-turn conversations
"""
from typing import List, Dict, Optional
from ..models.chat_response import ChatMessage
import json


class ContextService:
    """
    Service for tracking context across multi-turn conversations
    """
    
    def __init__(self):
        # In a real implementation, this would use a persistent store
        # For now, we'll use an in-memory dictionary
        self.session_contexts: Dict[str, List[ChatMessage]] = {}
    
    def add_message_to_context(self, session_id: str, message: ChatMessage):
        """
        Add a message to the conversation context for a session
        """
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = []
        
        self.session_contexts[session_id].append(message)
    
    def get_conversation_context(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """
        Get the recent conversation context for a session
        
        Args:
            session_id: The session identifier
            limit: Maximum number of messages to return
            
        Returns:
            List of recent ChatMessage objects
        """
        if session_id not in self.session_contexts:
            return []
        
        # Return the most recent messages up to the limit
        return self.session_contexts[session_id][-limit:]
    
    def clear_context(self, session_id: str):
        """
        Clear the conversation context for a session
        """
        if session_id in self.session_contexts:
            del self.session_contexts[session_id]
    
    def get_topic_context(self, session_id: str) -> Optional[str]:
        """
        Extract the main topic or context from the conversation
        
        Args:
            session_id: The session identifier
            
        Returns:
            A string representing the current topic or context, or None if not available
        """
        messages = self.get_conversation_context(session_id, limit=5)
        
        if not messages:
            return None
        
        # Simple approach: concatenate recent user messages to infer topic
        user_messages = [msg.content for msg in messages if msg.role == "user"]
        
        if not user_messages:
            return None
        
        # In a more sophisticated implementation, we would use NLP to extract topics
        return " ".join(user_messages[-2:])  # Return last 2 user messages as context
    
    def get_context_summary(self, session_id: str) -> dict:
        """
        Get a summary of the conversation context
        
        Args:
            session_id: The session identifier
            
        Returns:
            Dictionary with context summary information
        """
        messages = self.get_conversation_context(session_id)
        
        if not messages:
            return {
                "session_id": session_id,
                "message_count": 0,
                "topic": None,
                "last_activity": None
            }
        
        last_message = messages[-1]
        
        return {
            "session_id": session_id,
            "message_count": len(messages),
            "topic": self.get_topic_context(session_id),
            "last_activity": last_message.timestamp.isoformat() if last_message.timestamp else None
        }
    
    def update_context_metadata(self, session_id: str, key: str, value: any):
        """
        Update metadata for a session context
        """
        # This would require a more sophisticated storage system
        # For now, we'll just log that this functionality is needed
        pass