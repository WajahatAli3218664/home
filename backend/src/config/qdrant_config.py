import os
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class QdrantConfig:
    """Configuration class for Qdrant client"""
    
    # Qdrant connection parameters
    HOST = os.getenv("QDRANT_HOST", "localhost")
    PORT = int(os.getenv("QDRANT_PORT", "6333"))
    HTTPS = os.getenv("QDRANT_HTTPS", "False").lower() == "true"
    
    # For cloud instances
    URL = os.getenv("QDRANT_URL")  # e.g., https://your-cluster.example.com
    API_KEY = os.getenv("QDRANT_API_KEY")
    
    # Collections configuration
    COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_vectors")
    VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", "1536"))  # Default for OpenAI embeddings
    DISTANCE = os.getenv("QDRANT_DISTANCE", "Cosine")


def get_qdrant_client() -> QdrantClient:
    """
    Creates and returns a Qdrant client instance based on environment configuration.
    
    Returns:
        QdrantClient: Configured Qdrant client instance
    """
    # If using cloud-hosted Qdrant with URL
    if QdrantConfig.URL:
        if QdrantConfig.API_KEY:
            client = QdrantClient(
                url=QdrantConfig.URL,
                api_key=QdrantConfig.API_KEY,
                https=True
            )
        else:
            client = QdrantClient(url=QdrantConfig.URL)
    # If using local Qdrant instance
    else:
        client = QdrantClient(
            host=QdrantConfig.HOST,
            port=QdrantConfig.PORT,
            https=QdrantConfig.HTTPS
        )
    
    return client


def init_qdrant_collection(client: QdrantClient, collection_name: str = None) -> bool:
    """
    Initializes the Qdrant collection with proper configuration for textbook vectors.
    
    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to create (optional, uses default if not provided)
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    collection_name = collection_name or QdrantConfig.COLLECTION_NAME
    
    try:
        # Check if collection already exists
        collections = client.get_collections()
        collection_names = [collection.name for collection in collections.collections]
        
        if collection_name not in collection_names:
            # Create collection with specified vector configuration
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=QdrantConfig.VECTOR_SIZE,
                    distance=models.Distance(QdrantConfig.DISTANCE)
                )
            )
            print(f"Created Qdrant collection: {collection_name}")
        else:
            print(f"Qdrant collection already exists: {collection_name}")
        
        return True
    except Exception as e:
        print(f"Error initializing Qdrant collection: {e}")
        return False