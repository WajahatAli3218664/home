"""
Chat history persistence in Neon Postgres
"""
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..database.migrations import ChatMessageDB, ChatSessionDB
from ..models.chat_response import ChatMessage, ChatSession
from datetime import datetime
import json
import os


class DBService:
    """
    Service for database operations related to chat history
    """
    
    def __init__(self):
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL", "sqlite:///./rag_chatbot.db")
        
        # Create engine and session
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def save_message(self, message: ChatMessage) -> bool:
        """
        Save a chat message to the database
        
        Args:
            message: The ChatMessage object to save
            
        Returns:
            True if successful, False otherwise
        """
        db = self.SessionLocal()
        try:
            # Convert ChatMessage to ChatMessageDB
            db_message = ChatMessageDB(
                message_id=message.message_id,
                session_id=message.session_id,
                role=message.role.value if hasattr(message.role, 'value') else message.role,
                content=message.content,
                timestamp=message.timestamp,
                confidence_level=message.confidence_level.value if message.confidence_level and hasattr(message.confidence_level, 'value') 
                             else (message.confidence_level if message.confidence_level else None),
                retrieved_context_ids=json.dumps(message.retrieved_context_ids) if message.retrieved_context_ids else None,
                query_type=message.query_type.value if hasattr(message.query_type, 'value') else message.query_type
            )
            
            db.add(db_message)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error saving message: {e}")
            return False
        finally:
            db.close()
    
    def save_session(self, session: ChatSession) -> bool:
        """
        Save a chat session to the database
        
        Args:
            session: The ChatSession object to save
            
        Returns:
            True if successful, False otherwise
        """
        db = self.SessionLocal()
        try:
            # Convert ChatSession to ChatSessionDB
            db_session = ChatSessionDB(
                session_id=session.session_id,
                user_id=session.user_id,
                book_id=session.book_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
                metadata_json=json.dumps(session.metadata) if session.metadata else None
            )
            
            db.add(db_session)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error saving session: {e}")
            return False
        finally:
            db.close()
    
    def get_session_history(self, session_id: str) -> List[ChatMessage]:
        """
        Retrieve chat history for a specific session
        
        Args:
            session_id: The session identifier
            
        Returns:
            List of ChatMessage objects
        """
        db = self.SessionLocal()
        try:
            # Query messages for the session
            db_messages = db.query(ChatMessageDB).filter(
                ChatMessageDB.session_id == session_id
            ).order_by(ChatMessageDB.timestamp).all()
            
            # Convert DB objects to ChatMessage models
            messages = []
            for db_msg in db_messages:
                # Parse retrieved_context_ids from JSON
                retrieved_context_ids = json.loads(db_msg.retrieved_context_ids) if db_msg.retrieved_context_ids else []
                
                message = ChatMessage(
                    message_id=db_msg.message_id,
                    session_id=db_msg.session_id,
                    role=db_msg.role,
                    content=db_msg.content,
                    timestamp=db_msg.timestamp,
                    confidence_level=db_msg.confidence_level,
                    retrieved_context_ids=retrieved_context_ids,
                    query_type=db_msg.query_type
                )
                messages.append(message)
            
            return messages
        except Exception as e:
            print(f"Error retrieving session history: {e}")
            return []
        finally:
            db.close()
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Retrieve a chat session from the database
        
        Args:
            session_id: The session identifier
            
        Returns:
            ChatSession object if found, None otherwise
        """
        db = self.SessionLocal()
        try:
            # Query session
            db_session = db.query(ChatSessionDB).filter(
                ChatSessionDB.session_id == session_id
            ).first()
            
            if not db_session:
                return None
            
            # Convert DB object to ChatSession model
            metadata = json.loads(db_session.metadata_json) if db_session.metadata_json else None
            
            session = ChatSession(
                session_id=db_session.session_id,
                user_id=db_session.user_id,
                book_id=db_session.book_id,
                created_at=db_session.created_at,
                updated_at=db_session.updated_at,
                metadata=metadata
            )
            
            return session
        except Exception as e:
            print(f"Error retrieving session: {e}")
            return None
        finally:
            db.close()
    
    def create_tables(self):
        """
        Create database tables if they don't exist
        """
        from ..database.migrations import Base
        Base.metadata.create_all(bind=self.engine)