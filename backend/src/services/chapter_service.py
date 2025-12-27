from typing import List, Optional
from src.database import SessionLocal
from src.models.chapter import TextbookChapter as Chapter
from src.models.content_version import ContentVersion
from src.models.user_progress import UserProgress
from src.schemas.chapter import ChapterSchema
from src.services.personalization_service import PersonalizationService


class ChapterService:
    def __init__(self):
        self.db = SessionLocal()
        self.personalization_service = PersonalizationService()

    def get_all_chapters(self) -> List[ChapterSchema]:
        try:
            chapters = self.db.query(Chapter).order_by(Chapter.position).all()
            return [ChapterSchema.from_orm(chapter) for chapter in chapters]
        finally:
            self.db.close()

    def get_chapter_by_id(self, chapter_id: int) -> Optional[ChapterSchema]:
        try:
            chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if chapter:
                return ChapterSchema.from_orm(chapter)
            return None
        finally:
            self.db.close()

    def get_personalized_content(self, user_id: int, chapter_id: int) -> Optional[ChapterSchema]:
        """
        Retrieve chapter content with personalization based on user's progress
        """
        try:
            # Get the chapter
            chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not chapter:
                return None
            
            # Get user's progress for this chapter
            progress = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.chapter_id == chapter_id
            ).first()
            
            # Create the chapter schema
            chapter_schema = ChapterSchema.from_orm(chapter)
            
            # Personalize content based on user profile
            personalized_content = self.personalization_service.personalize_content(user_id, chapter)
            chapter_schema.content = personalized_content
            
            return chapter_schema
        finally:
            self.db.close()

    def get_personalized_content_by_level(self, user_id: int, chapter_id: int, background_level: str = None) -> Optional[ChapterSchema]:
        """
        Retrieve chapter content personalized based on the specified background level
        """
        try:
            # Get the chapter
            chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not chapter:
                return None
            
            # Create the chapter schema
            chapter_schema = ChapterSchema.from_orm(chapter)
            
            # If a specific background level is provided, use it for personalization
            if background_level:
                # Create temporary content based on background level
                if background_level == "beginner":
                    chapter_schema.content = self._adjust_content_for_beginner(chapter.content)
                elif background_level == "advanced":
                    chapter_schema.content = self._adjust_content_for_advanced(chapter.content)
                else:
                    # intermediate or default
                    chapter_schema.content = chapter.content
            else:
                # Use user's profile for personalization
                personalized_content = self.personalization_service.personalize_content(user_id, chapter)
                chapter_schema.content = personalized_content
            
            return chapter_schema
        finally:
            self.db.close()

    def _adjust_content_for_beginner(self, content: str) -> str:
        """
        Adjust content specifically for beginner level
        """
        # In a real implementation, this would simplify the content
        return content

    def _adjust_content_for_advanced(self, content: str) -> str:
        """
        Adjust content specifically for advanced level
        """
        # In a real implementation, this would add more detail
        return content