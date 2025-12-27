"""
Session management service
"""
from typing import Dict, Optional
from datetime import datetime, timedelta
from ..models.chat_response import ChatSession
import uuid


class SessionService:
    """
    Service for managing chat sessions
    """
    
    def __init__(self):
        # In a real implementation, this would use a persistent store
        # For now, we'll use an in-memory dictionary
        self.sessions: Dict[str, ChatSession] = {}
        self.session_timeout = timedelta(hours=24)  # Session expires after 24 hours
    
    def create_session(self, book_id: str, user_id: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session
        
        Args:
            book_id: The ID of the book for this session
            user_id: Optional user ID for authenticated users
            
        Returns:
            The created ChatSession object
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            book_id=book_id,
            created_at=now,
            updated_at=now,
            metadata={}
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a session by its ID
        
        Args:
            session_id: The session identifier
            
        Returns:
            The ChatSession object if found and not expired, None otherwise
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session has expired
        if datetime.utcnow() - session.updated_at > self.session_timeout:
            self.delete_session(session_id)
            return None
        
        return session
    
    def update_session(self, session_id: str, **kwargs) -> Optional[ChatSession]:
        """
        Update session properties
        
        Args:
            session_id: The session identifier
            **kwargs: Properties to update
            
        Returns:
            The updated ChatSession object if found, None otherwise
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Update the provided properties
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        # Update the last accessed time
        session.updated_at = datetime.utcnow()
        
        return session
    
    def delete_session(self, session_id: str):
        """
        Delete a session
        
        Args:
            session_id: The session identifier to delete
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def is_session_valid(self, session_id: str) -> bool:
        """
        Check if a session is valid (exists and not expired)
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if the session is valid, False otherwise
        """
        return self.get_session(session_id) is not None
    
    def extend_session(self, session_id: str) -> bool:
        """
        Extend a session's lifetime
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if the session was extended, False if it didn't exist
        """
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id].updated_at = datetime.utcnow()
        return True