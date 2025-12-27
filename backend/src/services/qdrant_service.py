"""
Qdrant retrieval service for textbook content
"""
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import google.generativeai as genai
from ..models.ai_response import RetrievedContext


class QdrantRetrievalService:
    """
    Service for retrieving relevant textbook content chunks from Qdrant vector database
    """

    def __init__(self):
        # Initialize Qdrant client with configuration from environment
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url:
            # Use a default local Qdrant if not configured
            qdrant_url = "http://localhost:6333"
            print("WARNING: QDRANT_URL not set, using default: http://localhost:6333")

        if qdrant_api_key:
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                prefer_grpc=True
            )
        else:
            print("WARNING: QDRANT_API_KEY not set, connecting without API key")
            self.client = QdrantClient(
                url=qdrant_url,
                prefer_grpc=True
            )

        # Initialize Google Gemini API for embeddings
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY not set, RAG functionality may be limited")
            self.gemini_available = False
            return
        else:
            self.gemini_available = True

        genai.configure(api_key=api_key)
        self.model_name = "models/embedding-001"

    def search_relevant_chunks(
        self,
        query: str,
        book_id: str,
        top_k: int = 5,
        similarity_threshold: float = 0.6
    ) -> List[RetrievedContext]:
        """
        Search for relevant textbook content chunks based on the query

        Args:
            query: The user's query to find relevant content for
            book_id: The ID of the textbook to search within
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score threshold

        Returns:
            List of RetrievedContext objects with relevant content
        """
        # Check if Gemini is available before generating embeddings
        if not self.gemini_available:
            print("Gemini API not available, returning empty results")
            return []

        # Generate embedding for the query using Google Gemini
        try:
            query_result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query",  # Using query task type for search queries
                title="Query"  # Optional title
            )
            query_embedding = query_result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []

        # Search in Qdrant collection
        # Using the configured collection name from settings
        try:
            from src.config.qdrant_config import QdrantConfig
            collection_name = QdrantConfig.COLLECTION_NAME

            search_results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=book_id),
                        ),
                    ]
                ),
                limit=top_k,
                score_threshold=similarity_threshold  # Apply similarity threshold
            )
        except Exception as e:
            print(f"Error searching in Qdrant: {str(e)}")
            return []

        # Convert search results to RetrievedContext objects
        retrieved_contexts = []
        for result in search_results:
            context = RetrievedContext(
                context_id=result.id,
                query_id="",  # Will be set when processing the query
                content_id=result.id,
                text_chunk=result.payload.get("content", ""),
                similarity_score=result.score,
                chapter=result.payload.get("chapter", "Unknown"),
                section=result.payload.get("section", "Unknown"),
                page_number=result.payload.get("page_number", 0)
            )
            retrieved_contexts.append(context)

        return retrieved_contexts

    def bypass_retrieval_for_selected_text(
        self,
        selected_text: str,
        book_id: str,
        chapter: str = "Selected Text",
        section: str = "User Selection",
        page_number: int = 0
    ) -> List[RetrievedContext]:
        """
        Create a RetrievedContext from selected text without performing vector search

        Args:
            selected_text: The text selected by the user
            book_id: The ID of the book the text comes from
            chapter: Chapter information for the selected text
            section: Section information for the selected text
            page_number: Page number for the selected text

        Returns:
            List containing a single RetrievedContext with the selected text
        """
        # Create a RetrievedContext with the selected text and a perfect similarity score
        context = RetrievedContext(
            context_id="selected_text",
            query_id="",  # Will be set when processing the query
            content_id="selected_text",
            text_chunk=selected_text,
            similarity_score=1.0,  # Perfect match since it's the exact selected text
            chapter=chapter,
            section=section,
            page_number=page_number
        )

        return [context]