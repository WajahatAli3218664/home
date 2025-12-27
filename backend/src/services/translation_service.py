import hashlib
from datetime import datetime, timedelta
from typing import Optional
import os
import google.generativeai as genai
from ..database import SessionLocal
from ..models.translation_cache import TranslationCache


class TranslationService:
    def __init__(self, cache_duration_hours: int = 24):
        # Initialize Google Gemini API for translations
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')  # Using the Gemini Pro model for translations

        self.db = SessionLocal()
        self.cache_duration = timedelta(hours=cache_duration_hours)

    def translate_content(self, content: str, target_language: str = "ur") -> str:
        """
        Translate content to the target language with caching
        """
        try:
            # Generate hash of source content to use as cache key
            content_hash = hashlib.sha256(f"{content}:{target_language}".encode()).hexdigest()

            # Check if translation is already cached
            cached_translation = self._get_cached_translation(content_hash, target_language)

            if cached_translation and cached_translation.expires_at > datetime.utcnow():
                # Return cached translation if it's still valid
                return cached_translation.translated_content

            # If not cached or expired, perform translation
            translated_content = self._perform_translation(content, target_language)

            # Cache the new translation
            self._cache_translation(content_hash, content, target_language, translated_content)

            return translated_content
        finally:
            self.db.close()

    def _get_cached_translation(self, content_hash: str, target_language: str) -> Optional[TranslationCache]:
        """
        Retrieve cached translation if it exists
        """
        translation = self.db.query(TranslationCache).filter(
            TranslationCache.source_content_hash == content_hash,
            TranslationCache.target_language == target_language
        ).first()

        return translation

    def _cache_translation(self, content_hash: str, source_content: str, target_language: str, translated_content: str):
        """
        Store translation in cache
        """
        # Check if a cache entry already exists and update it, or create a new one
        existing_cache = self.db.query(TranslationCache).filter(
            TranslationCache.source_content_hash == content_hash,
            TranslationCache.target_language == target_language
        ).first()

        if existing_cache:
            # Update existing cache entry
            existing_cache.translated_content = translated_content
            existing_cache.created_at = datetime.utcnow()
            existing_cache.expires_at = datetime.utcnow() + self.cache_duration
        else:
            # Create new cache entry
            cache_entry = TranslationCache(
                source_content_hash=content_hash,
                source_language="en",  # Assuming English source
                target_language=target_language,
                translated_content=translated_content,
                expires_at=datetime.utcnow() + self.cache_duration
            )
            self.db.add(cache_entry)

        self.db.commit()

    def _perform_translation(self, content: str, target_language: str) -> str:
        """
        Perform the actual translation using Google Gemini
        """
        try:
            # Create a translation prompt for Gemini
            if target_language.lower() == "ur":
                prompt = f"Translate the following English text to Urdu. Preserve formatting and structure as much as possible:\n\n{content}"
            elif target_language.lower() == "en":
                prompt = f"Translate the following text to English. Preserve formatting and structure as much as possible:\n\n{content}"
            else:
                # Default to translating to the target language
                prompt = f"Translate the following English text to {target_language}. Preserve formatting and structure as much as possible:\n\n{content}"

            # Generate the translation using Gemini
            response = self.model.generate_content(prompt)

            # Extract the translated content from the response
            translated_content = response.text if response.text else content

            return translated_content
        except Exception as e:
            print(f"Translation service error: {e}")
            # Fallback behavior when Gemini translation fails
            return self._fallback_translation(content, target_language)

    def _fallback_translation(self, content: str, target_language: str) -> str:
        """
        Fallback translation when primary service is unavailable
        """
        # Return the original content with a note that translation is unavailable
        return f"[TRANSLATION UNAVAILABLE] Original: {content}"