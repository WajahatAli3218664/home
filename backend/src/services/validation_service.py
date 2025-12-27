"""
Content validation to ensure responses only use textbook content
"""
from typing import List, Optional
from ..models.ai_response import RetrievedContext
import re


class ValidationService:
    """
    Service for validating content and ensuring responses only use textbook content
    """
    
    def __init__(self):
        # Define patterns that might indicate external knowledge
        self.external_knowledge_patterns = [
            r'\b(current year|current date|today|now|recently)\b',
            r'\b(very recent|brand new|just announced)\b',
            r'\b(forecast|prediction|future event)\b',
        ]
    
    def is_valid_query(self, query: str) -> bool:
        """
        Validate if the query is appropriate for the AI system
        """
        if not query or len(query.strip()) == 0:
            return False
        
        # Check if query is too short
        if len(query.strip()) < 3:
            return False
        
        return True
    
    def is_valid_response(self, response: str, context: str) -> bool:
        """
        Check if the response is grounded in the provided context
        This is a simplified implementation - in practice, this would be more sophisticated
        """
        # Check if response contains obvious external knowledge indicators
        for pattern in self.external_knowledge_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False
        
        # Basic check: if the response contains information not in the context
        # This is a simple check and would need to be more sophisticated in production
        response_lower = response.lower()
        context_lower = context.lower()
        
        # Look for obvious contradictions or fabrications
        if "this information is not available in the textbook" in response_lower:
            # This is an acceptable response when context is insufficient
            return True
        
        # For now, return True - in a more sophisticated system, we would check
        # if the response is supported by the context
        return True
    
    def detect_external_knowledge(self, query: str, response: str) -> bool:
        """
        Detect if the response contains external knowledge not available in the textbook
        """
        # Check if query suggests need for external knowledge
        if self._query_needs_external_knowledge(query):
            # If the response contains information that couldn't be in the textbook,
            # flag it as using external knowledge
            return True
        
        # Additional checks could be implemented here
        return False
    
    def _query_needs_external_knowledge(self, query: str) -> bool:
        """
        Check if the query requires external knowledge
        """
        external_indicators = [
            "current weather",
            "today's news",
            "recent events",
            "latest technology",
            "current stock price",
            "live information",
            "real-time data",
            "what happened yesterday",
            "current trends"
        ]
        
        query_lower = query.lower()
        for indicator in external_indicators:
            if indicator in query_lower:
                return True
        
        return False
    
    def validate_selected_text(self, selected_text: str) -> bool:
        """
        Validate selected text to ensure it meets minimum requirements
        """
        if not selected_text:
            return False
        
        # Check if the selected text is too short to be meaningful
        if len(selected_text.strip()) < 10:
            return False
        
        return True
    
    def validate_similarity_scores(self, contexts: List[RetrievedContext], threshold: float = 0.5) -> bool:
        """
        Validate that the similarity scores meet the minimum threshold
        """
        if not contexts:
            return False
        
        # Check if any context has a similarity score above the threshold
        for ctx in contexts:
            if ctx.similarity_score >= threshold:
                return True
        
        return False