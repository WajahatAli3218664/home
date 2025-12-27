"""
Unit tests for the RAG service
"""
import unittest
from unittest.mock import Mock, patch
from src.services.rag_service import RAGService
from src.models.chat_response import RetrievedContext, ConfidenceLevel


class TestRAGService(unittest.TestCase):
    
    def setUp(self):
        self.rag_service = RAGService()
    
    @patch('src.services.qdrant_service.QdrantRetrievalService.search_relevant_chunks')
    @patch('src.services.llm_service.LLMService.generate_response')
    def test_get_answer_with_general_query(self, mock_llm_generate, mock_qdrant_search):
        # Arrange
        mock_qdrant_search.return_value = [
            RetrievedContext(
                context_id="ctx1",
                book_id="book123",
                chunk_text="This is relevant content",
                chunk_metadata={"page": 10},
                similarity_score=0.85,
                embedding_id="emb1"
            )
        ]
        mock_llm_generate.return_value = "This is the generated response"
        
        # Act
        result = self.rag_service.get_answer(
            query="What is this book about?",
            book_id="book123",
            session_id="session456"
        )
        
        # Assert
        self.assertEqual(result["response"], "This is the generated response")
        self.assertEqual(result["confidence_level"], "High")
        self.assertEqual(result["session_id"], "session456")
        self.assertEqual(len(result["retrieved_context"]), 1)
        self.assertEqual(result["retrieved_context"][0]["similarity_score"], 0.85)
    
    @patch('src.services.qdrant_service.QdrantRetrievalService.bypass_retrieval_for_selected_text')
    @patch('src.services.llm_service.LLMService.generate_response')
    def test_get_answer_with_selected_text(self, mock_llm_generate, mock_qdrant_bypass):
        # Arrange
        mock_qdrant_bypass.return_value = [
            RetrievedContext(
                context_id="selected_text",
                book_id="book123",
                chunk_text="This is selected text",
                chunk_metadata={"source": "user_selection"},
                similarity_score=1.0,
                embedding_id="selected_text"
            )
        ]
        mock_llm_generate.return_value = "This is the response based on selected text"
        
        # Act
        result = self.rag_service.get_answer(
            query="Explain this concept?",
            book_id="book123",
            session_id="session456",
            selected_text="This is selected text"
        )
        
        # Assert
        self.assertEqual(result["response"], "This is the response based on selected text")
        self.assertEqual(result["confidence_level"], "High")
        self.assertEqual(result["session_id"], "session456")
        self.assertEqual(len(result["retrieved_context"]), 1)
        self.assertEqual(result["retrieved_context"][0]["similarity_score"], 1.0)
    
    def test_calculate_confidence_high(self):
        # Arrange
        contexts = [
            RetrievedContext(
                context_id="ctx1",
                book_id="book123",
                chunk_text="Content 1",
                chunk_metadata={},
                similarity_score=0.85,
                embedding_id="emb1"
            ),
            RetrievedContext(
                context_id="ctx2",
                book_id="book123",
                chunk_text="Content 2",
                chunk_metadata={},
                similarity_score=0.90,
                embedding_id="emb2"
            )
        ]
        
        # Act
        confidence = self.rag_service._calculate_confidence(contexts)
        
        # Assert
        self.assertEqual(confidence, ConfidenceLevel.HIGH)
    
    def test_calculate_confidence_medium(self):
        # Arrange
        contexts = [
            RetrievedContext(
                context_id="ctx1",
                book_id="book123",
                chunk_text="Content 1",
                chunk_metadata={},
                similarity_score=0.65,
                embedding_id="emb1"
            ),
            RetrievedContext(
                context_id="ctx2",
                book_id="book123",
                chunk_text="Content 2",
                chunk_metadata={},
                similarity_score=0.70,
                embedding_id="emb2"
            )
        ]
        
        # Act
        confidence = self.rag_service._calculate_confidence(contexts)
        
        # Assert
        self.assertEqual(confidence, ConfidenceLevel.MEDIUM)
    
    def test_calculate_confidence_low(self):
        # Arrange
        contexts = [
            RetrievedContext(
                context_id="ctx1",
                book_id="book123",
                chunk_text="Content 1",
                chunk_metadata={},
                similarity_score=0.40,
                embedding_id="emb1"
            ),
            RetrievedContext(
                context_id="ctx2",
                book_id="book123",
                chunk_text="Content 2",
                chunk_metadata={},
                similarity_score=0.35,
                embedding_id="emb2"
            )
        ]
        
        # Act
        confidence = self.rag_service._calculate_confidence(contexts)
        
        # Assert
        self.assertEqual(confidence, ConfidenceLevel.LOW)


if __name__ == '__main__':
    unittest.main()