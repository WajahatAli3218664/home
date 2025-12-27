from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from src.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    chapter_id = Column(Integer, nullable=False, index=True)
    progress = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())