"""
Database migration for AI responses with citations
"""
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# For this example, we'll define the models using SQLAlchemy
# In a real implementation, you would use Alembic for migrations

Base = declarative_base()


class TextbookContentDB(Base):
    """
    Database model for textbook content
    """
    __tablename__ = "textbook_content"

    content_id = Column(String, primary_key=True, index=True)
    book_id = Column(String, nullable=False)
    chapter = Column(String, nullable=False)
    section = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)
    content_text = Column(Text, nullable=False)
    embedding_id = Column(String, nullable=False)
    metadata_json = Column(Text)  # JSON metadata as text


class UserQueryDB(Base):
    """
    Database model for user queries
    """
    __tablename__ = "user_queries"

    query_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    query_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    selected_text = Column(Text, nullable=True)
    source_context = Column(String, nullable=True)


class RetrievedContextDB(Base):
    """
    Database model for retrieved context chunks
    """
    __tablename__ = "retrieved_contexts"

    context_id = Column(String, primary_key=True, index=True)
    query_id = Column(String, index=True, nullable=False)
    content_id = Column(String, nullable=False)
    text_chunk = Column(Text, nullable=False)
    similarity_score = Column(Float, nullable=False)
    chapter = Column(String, nullable=False)
    section = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)


class AIResponseDB(Base):
    """
    Database model for AI responses
    """
    __tablename__ = "ai_responses"

    response_id = Column(String, primary_key=True, index=True)
    query_id = Column(String, nullable=False)
    response_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    citations = Column(Text)  # JSON array of citations as text
    confidence_level = Column(String, default='Medium')  # 'High', 'Medium', 'Low'
    grounding_status = Column(String, default='Valid')  # 'Valid', 'Not Found', 'External'


class CitationDB(Base):
    """
    Database model for citations
    """
    __tablename__ = "citations"

    citation_id = Column(String, primary_key=True, index=True)
    response_id = Column(String, nullable=False)
    content_id = Column(String, nullable=False)
    chapter = Column(String, nullable=False)
    section = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)
    citation_format = Column(String, nullable=False)


class UserSessionDB(Base):
    """
    Database model for user sessions
    """
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)  # Optional for anonymous sessions
    book_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata_json = Column(Text)  # JSON metadata as text


def create_database_tables():
    """
    Create all database tables
    This function would typically be called during application startup
    """
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./textbook_ai.db")
    
    # Create engine
    engine = create_engine(database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully")


if __name__ == "__main__":
    create_database_tables()