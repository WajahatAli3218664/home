from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    textbooks = relationship("Textbook", back_populates="owner")
    learning_modules = relationship("LearningModule", back_populates="author")


class Textbook(Base):
    __tablename__ = "textbooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    content = Column(Text)  # Entire textbook content
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    
    # Relationships
    owner = relationship("User", back_populates="textbooks")
    modules = relationship("LearningModule", back_populates="textbook")


class LearningModule(Base):
    __tablename__ = "learning_modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text)  # Detailed content of the learning module
    textbook_id = Column(Integer, ForeignKey("textbooks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    position = Column(Integer, default=0)  # Order of the module in the textbook
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    textbook = relationship("Textbook", back_populates="modules")
    author = relationship("User", back_populates="learning_modules")


class Context7Session(Base):
    __tablename__ = "context7_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, nullable=False)  # Session ID from Context7
    user_id = Column(Integer, ForeignKey("users.id"))
    textbook_id = Column(Integer, ForeignKey("textbooks.id"))
    context_data = Column(Text)  # JSON or serialized context data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    textbook = relationship("Textbook")