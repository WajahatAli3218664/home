import os
from typing import List, Optional
from dotenv import load_dotenv
import cohere

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to store and validate environment variables"""

    # Cohere configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant configuration
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")

    # Source URLs configuration
    SOURCE_URLS: List[str] = os.getenv("SOURCE_URLS", "https://areejshaikh.github.io/book/").split(",")

    # Collection name
    COLLECTION_NAME: str = "rag_embeddings"

    @classmethod
    def validate(cls) -> List[str]:
        """Validate that all required configuration values are present"""
        errors = []

        if not cls.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required")

        if not cls.QDRANT_API_KEY:
            errors.append("QDRANT_API_KEY is required")

        if not cls.QDRANT_URL:
            errors.append("QDRANT_URL is required")

        if not cls.SOURCE_URLS or len(cls.SOURCE_URLS) == 0:
            errors.append("SOURCE_URLS must contain at least one URL")

        return errors

    @classmethod
    def validate_cohere_connection(cls) -> bool:
        """
        Validate connection to Cohere service by attempting to make a simple API call

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Create a temporary client to test the connection
            client = cohere.Client(cls.COHERE_API_KEY)
            # Do a simple operation like listing models to test the connection
            client.list_models()
            return True
        except Exception as e:
            print(f"Failed to connect to Cohere: {str(e)}")
            return False

    @classmethod
    def validate_qdrant_connection(cls) -> bool:
        """
        Validate connection to Qdrant service by attempting to connect and list collections

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            from qdrant_client import QdrantClient

            # Create a temporary client to test the connection
            client = QdrantClient(
                url=cls.QDRANT_URL,
                api_key=cls.QDRANT_API_KEY,
                prefer_grpc=False
            )

            # Try to list collections to test the connection
            client.get_collections()
            return True
        except Exception as e:
            print(f"Failed to connect to Qdrant: {str(e)}")
            return False


def validate_config() -> bool:
    """Validate the configuration and return True if all required values are present"""
    errors = Config.validate()
    if errors:
        for error in errors:
            print(f"Configuration error: {error}")
        return False
    return True


def validate_cohere_connection() -> bool:
    """Validate Cohere connection"""
    return Config.validate_cohere_connection()


def validate_qdrant_connection() -> bool:
    """Validate Qdrant connection"""
    return Config.validate_qdrant_connection()


def test_configuration_loading() -> bool:
    """
    Test configuration loading with valid and invalid credentials

    Returns:
        True if validation correctly identifies valid/invalid credentials, False otherwise
    """
    # Check if we have valid configuration
    has_valid_config = validate_config()

    # Test Cohere connection if API key exists
    cohere_valid = True
    if Config.COHERE_API_KEY:
        cohere_valid = validate_cohere_connection()

    # Test Qdrant connection if credentials exist
    qdrant_valid = True
    if Config.QDRANT_API_KEY and Config.QDRANT_URL:
        qdrant_valid = validate_qdrant_connection()

    print(f"Configuration validation: {'PASS' if has_valid_config else 'FAIL'}")
    print(f"Cohere connection test: {'PASS' if cohere_valid else 'FAIL'}")
    print(f"Qdrant connection test: {'PASS' if qdrant_valid else 'FAIL'}")

    # Return True if configuration is properly set up (all tests pass)
    return has_valid_config and cohere_valid and qdrant_valid