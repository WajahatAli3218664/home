from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import enum


class ProgrammingLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)
    programming_level: str = Field(max_length=50)  # Changed from enum to string to align with existing auth models
    ai_experience: str = Field(max_length=50)  # Keep the ai_experience field for compatibility
    software_experience: str = Field(max_length=255, default="")  # Add the field from our spec
    hardware_background: str = Field(max_length=255, default="")  # Add the field from our spec
    gpu_available: bool = Field(default=False)  # Keep for compatibility
    ram_size: str = Field(max_length=50, default="")  # Keep for compatibility
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class BookContent(SQLModel, table=True):
    __tablename__ = "book_contents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    content: str = Field(nullable=False)
    chapter_number: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="published", max_length=50)  # draft, published, archived


class TranslationStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Translation(SQLModel, table=True):
    __tablename__ = "translations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content_id: UUID = Field(foreign_key="book_contents.id", nullable=False)
    language: str = Field(nullable=False, max_length=10)  # e.g. "ur" for Urdu
    translated_content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: TranslationStatus = Field(default=TranslationStatus.pending)


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")  # nullable for anonymous sessions
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    title: str = Field(max_length=255)


class QuestionContext(SQLModel, table=True):
    __tablename__ = "question_contexts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id", nullable=False)
    book_content_id: UUID = Field(foreign_key="book_contents.id", nullable=False)
    selected_text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_query: str = Field(nullable=False)


def create_db_and_tables():
    """Create database tables based on models"""
    # Implementation moved to session.py
    pass