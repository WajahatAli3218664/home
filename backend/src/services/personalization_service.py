from typing import List, Optional
from src.database import SessionLocal
from src.models.user import UserProfile
from src.models.chapter import TextbookChapter as Chapter


class PersonalizationService:
    def __init__(self):
        self.db = SessionLocal()

    def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        """
        Retrieve the user's profile with personalization settings
        """
        try:
            profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            return profile
        finally:
            self.db.close()

    def personalize_content(self, user_id: int, chapter: Chapter) -> str:
        """
        Adjust content based on user's profile
        """
        try:
            profile = self.get_user_profile(user_id)
            if not profile:
                return chapter.content  # Return original content if no profile exists
            
            # Adjust content based on the user's background level
            content = chapter.content
            
            # For example, simplify content for beginners, add more detail for advanced users
            background_level = profile.background_level or "intermediate"
            
            if background_level == "beginner":
                # Simplify content for beginners
                # This would involve actual content transformation in a real implementation
                content = self._simplify_content(content)
            elif background_level == "advanced":
                # Add more depth for advanced users
                content = self._enrich_content(content)
            
            return content
        finally:
            self.db.close()

    def _simplify_content(self, content: str) -> str:
        """
        Simplify content for beginner users (placeholder implementation)
        """
        # In a real implementation, this would use NLP techniques to simplify text
        return content

    def _enrich_content(self, content: str) -> str:
        """
        Enrich content for advanced users (placeholder implementation)
        """
        # In a real implementation, this would add more technical details
        return content