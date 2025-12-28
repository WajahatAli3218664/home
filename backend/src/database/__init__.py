"""
Database package initialization. Provide `engine`, `SessionLocal`, and `Base`
so other modules can import them as `from src.database import SessionLocal`.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config.settings import settings

# Determine effective database URL from settings or environment
DATABASE_URL = settings.effective_database_url or os.getenv("DATABASE_URL", "sqlite:///./textbook_app.db")

# Create engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()

__all__ = ["engine", "SessionLocal", "Base"]