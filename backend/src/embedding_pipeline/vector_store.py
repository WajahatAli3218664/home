from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
from .config import Config


class QdrantStore:
    """Qdrant client wrapper for vector storage with error handling"""

    def __init__(self):
        """Initialize the Qdrant client with connection details from config"""
        if not Config.QDRANT_URL or not Config.QDRANT_API_KEY:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY are required in environment variables")

        self.client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            prefer_grpc=False  # Using HTTP for simplicity
        )
        self.collection_name = Config.COLLECTION_NAME

    def create_collection(self, collection_name: Optional[str] = None) -> bool:
        """
        Create a Qdrant collection for storing embeddings

        Args:
            collection_name: Name of the collection to create (uses default if not provided)

        Returns:
            True if collection was created successfully, False otherwise
        """
        collection_name = collection_name or self.collection_name

        try:
            # The Cohere embed-multilingual-v2.0 model returns 768-dimension vectors
            vector_size = 768  # Updated for the multilingual-v2.0 model

            # Create the collection with the correct vector size
            # If it already exists with wrong dimensions, we'll delete and recreate
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Collection {collection_name} created successfully")
                return True
            except Exception as creation_error:
                # If creation fails because collection already exists with wrong dimensions,
                # delete it and try again
                print(f"Failed to create collection, likely already exists with wrong dimensions: {str(creation_error)}")
                print(f"Deleting existing collection {collection_name}...")
                try:
                    self.client.delete_collection(collection_name)
                    print(f"Successfully deleted collection {collection_name}")
                except Exception as delete_error:
                    print(f"Error deleting collection: {str(delete_error)}")
                    # If we can't delete, return False
                    return False

                # Now recreate with correct dimensions
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Collection {collection_name} recreated successfully with correct dimensions")
                return True

        except Exception as e:
            print(f"Failed to create collection {collection_name}: {str(e)}")
            return False

    def save_chunks_to_qdrant(self, chunks: List[Dict], collection_name: Optional[str] = None) -> bool:
        """
        Store document chunks with embeddings in Qdrant

        Args:
            chunks: List of chunks (with text, embedding, and metadata)
            collection_name: Name of the collection to store in (uses default if not provided)

        Returns:
            True if chunks were saved successfully, False otherwise
        """
        collection_name = collection_name or self.collection_name

        try:
            # Prepare points for Qdrant
            points = []
            for i, chunk in enumerate(chunks):
                point = models.PointStruct(
                    id=i,
                    vector=chunk.get('embedding', []),
                    payload={
                        'content': chunk.get('content', ''),
                        'source_url': chunk.get('source_url', ''),
                        'chunk_index': chunk.get('chunk_index', 0),
                        'metadata': chunk.get('metadata', {}),
                        **chunk.get('metadata', {})  # Additional metadata
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )

            print(f"Successfully saved {len(chunks)} chunks to collection {collection_name}")
            return True
        except Exception as e:
            print(f"Failed to save chunks to collection {collection_name}: {str(e)}")
            return False

    def validate_retrieval(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Test retrieval accuracy by performing similarity search

        Args:
            query: Query string to search for
            top_k: Number of results to return

        Returns:
            List of relevant chunks with similarity scores
        """
        try:
            from .embedder import CohereClient

            # Generate embedding for the query
            cohere_client = CohereClient()
            query_embedding = cohere_client.embed_single(query)

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            results = []
            for result in search_results:
                results.append({
                    'content': result.payload.get('content', ''),
                    'source_url': result.payload.get('source_url', ''),
                    'score': result.score,
                    'metadata': result.payload.get('metadata', {})
                })

            return results
        except Exception as e:
            print(f"Failed to validate retrieval: {str(e)}")
            return []