from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.learning_materials_service import LearningMaterialsService
from src.models.learning_materials import LearningMaterials
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{chapter_id}", response_model=None)
def get_learning_materials_by_chapter(
    chapter_id: int,
    material_type: str = None,
    learning_materials_service: LearningMaterialsService = Depends(LearningMaterialsService)
):
    try:
        materials = learning_materials_service.get_learning_materials_by_chapter(chapter_id, material_type)
        if not materials:
            raise HTTPException(status_code=404, detail="No learning materials found for this chapter")
        
        return materials
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving learning materials for chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving learning materials")