"""
Citation generation based on retrieved context
"""
from typing import List
from ..models.ai_response import RetrievedContext


class CitationService:
    """
    Service for generating and formatting citations based on retrieved context
    """
    
    @staticmethod
    def generate_citations_from_contexts(contexts: List[RetrievedContext]) -> List[str]:
        """
        Generate citation strings from a list of retrieved contexts
        
        Args:
            contexts: List of RetrievedContext objects
            
        Returns:
            List of formatted citation strings
        """
        citations = []
        for ctx in contexts:
            # Create a formatted citation string
            citation = f"Chapter {ctx.chapter} - {ctx.section} (p. {ctx.page_number})"
            if citation not in citations:  # Avoid duplicate citations
                citations.append(citation)
        return citations
    
    @staticmethod
    def format_citation(chapter: str, section: str, page_number: int) -> str:
        """
        Format a citation according to textbook standards
        
        Args:
            chapter: Chapter name/number
            section: Section name/number
            page_number: Page number
            
        Returns:
            Formatted citation string
        """
        return f"Chapter {chapter} - {section} (p. {page_number})"
    
    @staticmethod
    def validate_citation_format(citation: str) -> bool:
        """
        Validate if a citation follows the expected format
        
        Args:
            citation: Citation string to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # Check if citation contains expected elements
        if "Chapter" in citation and ("-" in citation or "(p." in citation):
            return True
        return False
    
    @staticmethod
    def extract_citation_parts(citation: str) -> dict:
        """
        Extract parts from a formatted citation string
        
        Args:
            citation: Formatted citation string
            
        Returns:
            Dictionary with chapter, section, and page_number
        """
        # This is a simplified extraction - in practice, you might need more robust parsing
        parts = {
            "chapter": "",
            "section": "",
            "page_number": 0
        }
        
        # Extract page number
        if "(p." in citation and ")" in citation:
            page_part = citation.split("(p.")[1].split(")")[0].strip()
            try:
                parts["page_number"] = int(page_part)
            except ValueError:
                parts["page_number"] = 0
        
        # Extract chapter and section
        if "Chapter" in citation and "-" in citation:
            chapter_part = citation.split("Chapter")[1].split("-")[0].strip()
            parts["chapter"] = chapter_part
            
            section_part = citation.split("-")[1].split("(p.")[0].strip()
            parts["section"] = section_part
        
        return parts