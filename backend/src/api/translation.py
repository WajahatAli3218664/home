from fastapi import APIRouter, Depends, HTTPException
from src.services.translation_service import TranslationService
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/{chapter_id}/translate")
def translate_chapter(
    chapter_id: int,
    target_language: str = "ur",
    translation_service: TranslationService = Depends(TranslationService)
):
    try:
        # In a real implementation, we would fetch the chapter content by chapter_id
        # For now, we'll simulate this with a placeholder
        placeholder_content = f"Content of chapter {chapter_id} to be translated"
        
        translated_content = translation_service.translate_content(
            content=placeholder_content,
            target_language=target_language
        )
        return {
            "chapter_id": chapter_id,
            "target_language": target_language,
            "translated_content": translated_content
        }
    except Exception as e:
        logger.error(f"Error translating chapter {chapter_id} to {target_language}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")