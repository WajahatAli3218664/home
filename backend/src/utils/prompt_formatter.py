"""
Utility for formatting prompts for the LLM with context
"""
from typing import List, Dict, Any, Optional
import json


class PromptFormatter:
    """
    Utility class for formatting prompts with context for LLM requests
    """
    
    @staticmethod
    def format_rag_prompt(
        query: str, 
        context: str, 
        system_prompt: Optional[str] = None,
        include_citations: bool = True
    ) -> str:
        """
        Format a RAG prompt with context and query
        
        Args:
            query: The user's question
            context: The retrieved context to include
            system_prompt: Optional system prompt to prepend
            include_citations: Whether to include citation instructions
        
        Returns:
            Formatted prompt string
        """
        if system_prompt is None:
            system_prompt = (
                "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. "
                "You MUST answer ONLY based on the information provided in the context. "
                "If the context does not contain enough information to answer the question, "
                "clearly state: 'This information is not available in the textbook.' "
                "Do NOT use external knowledge, training data, or assumptions beyond the provided context. "
                "Do NOT mention technical implementation details like vector search or system architecture. "
                "Provide concise, clear, and helpful answers. Use bullet points when appropriate. "
                "Use simple language suitable for readers of the textbook. Do NOT quote large passages unless explicitly asked. "
                + ("Include proper citations with each response indicating the source chapter and section." if include_citations else "")
            )
        
        # Format the user message with context and query
        user_message = f"Context: {context}\n\nQuestion: {query}\n\nPlease provide an answer based only on the provided context. If the context does not contain enough information to answer the question, respond with 'This information is not available in the textbook.'"
        
        if include_citations:
            user_message += " Include proper citations indicating the source chapter and section."
        
        return {
            "system": system_prompt,
            "user": user_message
        }
    
    @staticmethod
    def format_context_with_metadata(
        context_chunks: List[Dict[str, Any]], 
        max_length: int = 2000
    ) -> str:
        """
        Format context chunks with metadata for inclusion in prompts
        
        Args:
            context_chunks: List of context chunks with metadata
            max_length: Maximum length of the formatted context
        
        Returns:
            Formatted context string
        """
        formatted_chunks = []
        
        for chunk in context_chunks:
            chunk_text = chunk.get("text", "")
            source = chunk.get("source_document", "Unknown source")
            similarity_score = chunk.get("similarity_score", 0.0)
            
            formatted_chunk = f"[Source: {source} | Similarity: {similarity_score:.2f}]\n{chunk_text}\n"
            formatted_chunks.append(formatted_chunk)
        
        # Combine all chunks
        full_context = "\n".join(formatted_chunks)
        
        # Truncate if necessary
        if len(full_context) > max_length:
            full_context = full_context[:max_length]
            # Try to break at a sentence boundary
            last_sentence_end = max(
                full_context.rfind('.'),
                full_context.rfind('!'),
                full_context.rfind('?')
            )
            if last_sentence_end > max_length * 0.8:  # Only truncate at sentence if it's reasonably close
                full_context = full_context[:last_sentence_end + 1]
        
        return full_context
    
    @staticmethod
    def validate_prompt_components(
        query: str,
        context: str,
        max_context_length: int = 4000  # Typical max for most models
    ) -> Dict[str, Any]:
        """
        Validate that prompt components are appropriate for LLM
        
        Args:
            query: The user's query
            context: The context to include
            max_context_length: Maximum allowed context length
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "query_valid": len(query.strip()) > 0,
            "context_valid": len(context.strip()) > 0,
            "context_length_ok": len(context) <= max_context_length,
            "total_length": len(query) + len(context),
            "suggestions": []
        }
        
        if not validation_results["query_valid"]:
            validation_results["suggestions"].append("Query is empty or contains only whitespace")
        
        if not validation_results["context_valid"]:
            validation_results["suggestions"].append("Context is empty or contains only whitespace")
        
        if not validation_results["context_length_ok"]:
            validation_results["suggestions"].append(f"Context is too long ({len(context)} chars), consider truncating to {max_context_length} chars")
        
        if validation_results["total_length"] > max_context_length * 1.5:  # Arbitrary threshold
            validation_results["suggestions"].append("Total prompt might be too long for effective processing")
        
        return validation_results