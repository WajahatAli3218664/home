from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.database import Base


class LearningMaterials(Base):
    __tablename__ = "learning_materials"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, nullable=False)
    material_type = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
