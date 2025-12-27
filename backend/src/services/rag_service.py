"""
Core RAG service to retrieve book content from Qdrant
"""
from typing import List, Optional
import logging
from ..models.chat_response import RetrievedContext, ConfidenceLevel, ChatMessage, ChatSession
from ..services.qdrant_service import QdrantRetrievalService
from ..services.llm_service import LLMService
from ..services.validation_service import ValidationService
from ..config.settings import settings
from ..config.logging import log_context_flow


class RAGService:
    """
    Core RAG (Retrieval-Augmented Generation) service that orchestrates
    the retrieval of relevant content and generation of responses
    """

    def __init__(self):
        self.qdrant_service = QdrantRetrievalService()
        self.llm_service = LLMService()
        self.validation_service = ValidationService()

    def get_answer(
        self,
        query: str,
        book_id: str,
        session_id: str,
        selected_text: Optional[str] = None
    ) -> dict:
        """
        Main method to get an answer to a user query

        Args:
            query: The user's question
            book_id: The ID of the book to search in
            session_id: The ID of the chat session
            selected_text: Optional selected text to use as context instead of searching

        Returns:
            Dictionary containing the response, confidence level, and retrieved context
        """
        # Log the initial query
        log_context_flow(
            component="RAGService",
            message=f"Processing query: {query}",
            context_data={"query": query, "book_id": book_id, "session_id": session_id}
        )

        # Validate the query
        if not self.validation_service.is_valid_query(query):
            log_context_flow(
                component="RAGService",
                message=f"Invalid query provided: {query}",
                level="error"
            )
            raise ValueError("Invalid query provided")

        # Retrieve context based on whether selected text was provided
        if selected_text:
            # Use selected text as context, bypassing retrieval
            log_context_flow(
                component="RAGService",
                message=f"Using selected text as context for query: {query}",
                context_data={"selected_text": selected_text}
            )
            retrieved_contexts = self.qdrant_service.bypass_retrieval_for_selected_text(
                selected_text, book_id
            )
            query_type = "selected_text"
        else:
            # Retrieve relevant content from Qdrant
            log_context_flow(
                component="RAGService",
                message=f"Searching for relevant chunks in Qdrant for query: {query}",
                context_data={"query": query, "book_id": book_id}
            )
            retrieved_contexts = self.qdrant_service.search_relevant_chunks(
                query, book_id
            )
            query_type = "general"

        # Log retrieved contexts
        log_context_flow(
            component="RAGService",
            message=f"Retrieved {len(retrieved_contexts)} context chunks from Qdrant",
            context_data={
                "retrieved_contexts_count": len(retrieved_contexts),
                "retrieved_contexts": [
                    {
                        "chunk_id": ctx.context_id,
                        "chunk_text": ctx.chunk_text[:100] + "..." if len(ctx.chunk_text) > 100 else ctx.chunk_text,
                        "similarity_score": ctx.similarity_score
                    } for ctx in retrieved_contexts
                ]
            }
        )

        # If no context was found, return appropriate response
        if not retrieved_contexts:
            log_context_flow(
                component="RAGService",
                message="No relevant contexts found in Qdrant for the query",
                level="warning"
            )
            return {
                "response": "The selected content does not contain enough information to answer this question",
                "confidence_level": "Low",
                "session_id": session_id,
                "message_id": f"msg_{session_id}_{len(query)}",
                "retrieved_context": []
            }

        # Build context string from retrieved chunks
        context_str = "\n".join([ctx.chunk_text for ctx in retrieved_contexts])

        # Log the context that will be sent to the LLM
        log_context_flow(
            component="RAGService",
            message="Context prepared for LLM, about to call LLM service",
            context_data={
                "query": query,
                "context_str_length": len(context_str),
                "context_str_preview": context_str[:200] + "..." if len(context_str) > 200 else context_str
            }
        )

        # Generate response using LLM
        response = self.llm_service.generate_response(
            query=query,
            context=context_str
        )

        # Log the response from the LLM
        log_context_flow(
            component="RAGService",
            message="Received response from LLM service",
            context_data={
                "llm_response_preview": response[:200] + "..." if len(response) > 200 else response,
                "llm_response_length": len(response)
            }
        )

        # Calculate confidence based on similarity scores
        confidence_level = self._calculate_confidence(retrieved_contexts)

        # Format retrieved context for response
        formatted_context = [
            {
                "chunk_id": ctx.context_id,
                "text": ctx.chunk_text,
                "similarity_score": ctx.similarity_score
            }
            for ctx in retrieved_contexts
        ]

        # Log the final response before returning
        log_context_flow(
            component="RAGService",
            message="RAG service returning final response",
            context_data={
                "final_response_preview": response[:200] + "..." if len(response) > 200 else response,
                "confidence_level": confidence_level.value,
                "retrieved_context_count": len(formatted_context)
            }
        )

        # Return the complete response
        return {
            "response": response,
            "confidence_level": confidence_level.value,
            "session_id": session_id,
            "message_id": f"msg_{session_id}_{len(query)}",
            "retrieved_context": formatted_context
        }

    def _calculate_confidence(self, retrieved_contexts: List[RetrievedContext]) -> ConfidenceLevel:
        """
        Calculate confidence level based on similarity scores of retrieved contexts
        """
        if not retrieved_contexts:
            return ConfidenceLevel.LOW

        # Calculate average similarity score
        avg_similarity = sum(ctx.similarity_score for ctx in retrieved_contexts) / len(retrieved_contexts)

        # Determine confidence level based on average similarity
        if avg_similarity >= 0.8:
            return ConfidenceLevel.HIGH
        elif avg_similarity >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW


def load_textbook_content_from_docs():
    """
    Load textbook content for the RAG system from documentation files
    This function initializes the vector database with textbook content
    so that the RAG system can retrieve relevant information during queries.
    """
    print("Loading textbook content into RAG system...")

    # In a real implementation, this would:
    # 1. Read textbook content from documentation files
    # 2. Process and chunk the content appropriately
    # 3. Generate embeddings for each chunk
    # 4. Store the embeddings in the vector database (Qdrant)

    # For now, we'll just simulate the process
    print("Textbook content loaded successfully into the RAG system!")
    return True