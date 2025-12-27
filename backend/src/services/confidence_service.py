"""
Confidence level calculation based on similarity scores
"""
from typing import List
from ..models.chat_response import RetrievedContext, ConfidenceLevel


class ConfidenceService:
    """
    Service for calculating confidence levels based on similarity scores
    and context relevance
    """
    
    @staticmethod
    def calculate_confidence(retrieved_contexts: List[RetrievedContext]) -> ConfidenceLevel:
        """
        Calculate confidence level based on similarity scores of retrieved contexts
        
        Args:
            retrieved_contexts: List of retrieved context chunks with similarity scores
            
        Returns:
            ConfidenceLevel enum value (HIGH, MEDIUM, LOW)
        """
        if not retrieved_contexts:
            return ConfidenceLevel.LOW
        
        # Calculate average similarity score
        avg_similarity = sum(ctx.similarity_score for ctx in retrieved_contexts) / len(retrieved_contexts)
        
        # Calculate score variance to determine consistency
        variance = sum((ctx.similarity_score - avg_similarity) ** 2 for ctx in retrieved_contexts) / len(retrieved_contexts)
        std_dev = variance ** 0.5
        
        # Determine confidence level based on average similarity and consistency
        if avg_similarity >= 0.8:
            return ConfidenceLevel.HIGH
        elif avg_similarity >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    @staticmethod
    def calculate_contextual_confidence(
        query: str, 
        retrieved_contexts: List[RetrievedContext], 
        response: str
    ) -> ConfidenceLevel:
        """
        Calculate confidence based on how well the response addresses the query
        given the retrieved context
        
        Args:
            query: The original user query
            retrieved_contexts: List of retrieved context chunks
            response: The generated response
            
        Returns:
            ConfidenceLevel enum value
        """
        # This would involve more sophisticated NLP analysis in a real implementation
        # For now, we'll use the similarity-based approach
        return ConfidenceService.calculate_confidence(retrieved_contexts)
    
    @staticmethod
    def get_confidence_thresholds() -> dict:
        """
        Get the confidence thresholds used for classification
        """
        return {
            "high_threshold": 0.8,
            "medium_threshold": 0.6,
            "low_threshold": 0.0
        }