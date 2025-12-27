from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.chapter_service import ChapterService
from src.schemas.chapter import ChapterSchema
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ChapterSchema])
def get_chapters(chapter_service: ChapterService = Depends(ChapterService)):
    try:
        return chapter_service.get_all_chapters()
    except Exception as e:
        logger.error(f"Error retrieving chapters: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving chapters")


@router.get("/{chapter_id}", response_model=ChapterSchema)
def get_chapter_by_id(
    chapter_id: int,
    background_level: str = None,
    user_id: int = None,
    chapter_service: ChapterService = Depends(ChapterService)
):
    try:
        if user_id is not None:
            # Get personalized content based on user profile or specified background level
            chapter = chapter_service.get_personalized_content_by_level(
                user_id=user_id,
                chapter_id=chapter_id,
                background_level=background_level
            )
        else:
            # Get standard content
            chapter = chapter_service.get_chapter_by_id(chapter_id)
        
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return chapter
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving chapter")