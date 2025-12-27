from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.progress_service import ProgressService
from src.schemas.progress import ProgressSchema, ProgressUpdateRequest
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ProgressSchema])
def get_progress(user_id: int, progress_service: ProgressService = Depends(ProgressService)):
    try:
        return progress_service.get_progress_by_user(user_id)
    except Exception as e:
        logger.error(f"Error retrieving progress for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving progress")


@router.get("/{chapter_id}", response_model=ProgressSchema)
def get_progress_by_chapter(user_id: int, chapter_id: int, progress_service: ProgressService = Depends(ProgressService)):
    try:
        progress_records = progress_service.get_progress_by_user(user_id)
        for record in progress_records:
            if record.chapter_id == chapter_id:
                return record
        raise HTTPException(status_code=404, detail="Progress record not found for this chapter")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving progress for user {user_id} and chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving progress")


@router.put("/{chapter_id}", response_model=ProgressSchema)
def update_progress(
    user_id: int, 
    chapter_id: int, 
    progress_update: ProgressUpdateRequest,
    progress_service: ProgressService = Depends(ProgressService)
):
    try:
        if chapter_id != progress_update.chapter_id:
            raise HTTPException(status_code=400, detail="Path chapter_id does not match request body chapter_id")
            
        progress_record = progress_service.update_progress(
            user_id=user_id,
            chapter_id=chapter_id,
            progress=progress_update.progress
        )
        return progress_record
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error updating progress for user {user_id} and chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while updating progress")