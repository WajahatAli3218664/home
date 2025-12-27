from typing import List, Dict, Any
from src.services.embedding_service import embedding_service
from src.services.qdrant_service import qdrant_manager
from uuid import UUID

class RetrievalService:
    def __init__(self):
        self.embedding_service = embedding_service
        self.qdrant_manager = qdrant_manager
    
    def retrieve_relevant_chunks(self, query: str, book_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the most relevant chunks for a query from a specific book"""
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Retrieve similar chunks from Qdrant
        results = self.qdrant_manager.retrieve_similar(
            query_embedding=query_embedding,
            book_id=book_id,
            limit=limit
        )
        
        return results
    
    def retrieve_with_selected_text(self, selected_text: str, book_id: str) -> List[Dict[str, Any]]:
        """Retrieve chunks based only on selected/highlighted text"""
        # In this case, we'll return the selected text as the only relevant chunk
        # In a real implementation, you might want to do more sophisticated processing
        return [{
            "chunk_id": "selected_text",
            "text": selected_text,
            "score": 1.0,  # Perfect match since it's the selected text
            "metadata": {"book_id": book_id}
        }]

# Create a singleton instance
retrieval_service = RetrievalService()