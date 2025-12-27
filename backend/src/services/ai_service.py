"""
Core AI service to retrieve textbook content from Qdrant
"""
from typing import List, Optional
from ..models.ai_response import RetrievedContext, AIResponse, Citation, ConfidenceLevel, GroundingStatus
from ..services.qdrant_service import QdrantRetrievalService
from ..services.llm_service import LLMService
from ..services.validation_service import ValidationService
from ..config.settings import settings


class AIService:
    """
    Core AI service that orchestrates the retrieval of relevant content and generation of responses
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
    ) -> AIResponse:
        """
        Main method to get an answer to a user query
        
        Args:
            query: The user's question
            book_id: The ID of the textbook to search in
            session_id: The ID of the user session
            selected_text: Optional selected text to use as context instead of searching
        
        Returns:
            AIResponse object containing the response, confidence level, citations, and grounding status
        """
        # Validate the query
        if not self.validation_service.is_valid_query(query):
            raise ValueError("Invalid query provided")
        
        # Retrieve context based on whether selected text was provided
        if selected_text:
            # Use selected text as context, bypassing retrieval
            retrieved_contexts = self.qdrant_service.bypass_retrieval_for_selected_text(
                selected_text, book_id
            )
            query_type = "selected_text"
        else:
            # Retrieve relevant content from Qdrant
            retrieved_contexts = self.qdrant_service.search_relevant_chunks(
                query, book_id
            )
            query_type = "general"
        
        # If no context was found, return appropriate response
        if not retrieved_contexts:
            return AIResponse(
                response_id=f"resp_{session_id}_{len(query)}",
                query_id="",  # Will be set when processing the full query
                response_text="This information is not available in the textbook.",
                timestamp=None,  # Will be set when creating the response
                citations=[],
                confidence_level=ConfidenceLevel.LOW,
                grounding_status=GroundingStatus.NOT_FOUND
            )
        
        # Build context string from retrieved chunks
        context_str = "\n".join([ctx.text_chunk for ctx in retrieved_contexts])
        
        # Generate response using LLM
        response = self.llm_service.generate_response(
            query=query,
            context=context_str
        )
        
        # Calculate confidence based on similarity scores
        confidence_level = self._calculate_confidence(retrieved_contexts)
        
        # Generate citations from retrieved contexts
        citations = self._generate_citations(retrieved_contexts)
        
        # Validate the response for grounding
        grounding_status = self._validate_response_grounding(query, context_str, response)
        
        # Return the complete response
        return AIResponse(
            response_id=f"resp_{session_id}_{len(query)}",
            query_id="",  # Will be set when processing the full query
            response_text=response,
            timestamp=None,  # Will be set when creating the response
            citations=citations,
            confidence_level=confidence_level,
            grounding_status=grounding_status
        )
    
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
    
    def _generate_citations(self, retrieved_contexts: List[RetrievedContext]) -> List[str]:
        """
        Generate citation strings from retrieved contexts
        """
        citations = []
        for ctx in retrieved_contexts:
            citation = f"Chapter {ctx.chapter} - {ctx.section} (p. {ctx.page_number})"
            if citation not in citations:  # Avoid duplicate citations
                citations.append(citation)
        return citations
    
    def _validate_response_grounding(self, query: str, context: str, response: str) -> GroundingStatus:
        """
        Validate if the response is properly grounded in the provided context
        """
        if self.validation_service.detect_external_knowledge(query, response):
            return GroundingStatus.EXTERNAL
        elif self.validation_service.is_valid_response(response, context):
            return GroundingStatus.VALID
        else:
            return GroundingStatus.NOT_FOUND