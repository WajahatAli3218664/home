from sqlalchemy import Column, Integer, String, Text
from src.database import Base


class TextbookChapter(Base):
    __tablename__ = "textbook_chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    version = Column(String(20), default='1.0.0')
    position = Column(Integer, unique=True, nullable=False)
    word_count = Column(Integer, default=0)
    estimated_reading_time = Column(Integer, default=0)  # in minutes
    metadata_json = Column(Text)  # JSON string for additional metadata