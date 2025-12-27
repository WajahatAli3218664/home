import cohere
from typing import List
from .config import Config


class CohereClient:
    """Cohere client wrapper for embedding generation with error handling"""

    def __init__(self):
        """Initialize the Cohere client with API key from config"""
        if not Config.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is not set in environment variables")

        self.client = cohere.Client(Config.COHERE_API_KEY)
        self.model = "embed-multilingual-v2.0"  # Using the multilingual embedding model

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (lists of floats)

        Raises:
            Exception: If Cohere API call fails
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Appropriate for document search
            )
            return response.embeddings
        except Exception as e:
            print(f"Cohere embedding generation failed: {str(e)}")
            raise

    def embed_single(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string

        Args:
            text: Text string to embed

        Returns:
            Embedding vector (list of floats)

        Raises:
            Exception: If Cohere API call fails
        """
        return self.embed([text])[0]