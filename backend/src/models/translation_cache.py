from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.database import Base


class TranslationCache(Base):
    __tablename__ = "translation_cache"

    id = Column(Integer, primary_key=True, index=True)
    source_content_hash = Column(String(128), nullable=False, index=True)
    source_language = Column(String(10), default="en")
    target_language = Column(String(10), nullable=False)
    translated_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
