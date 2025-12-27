"""
Unit tests for the AI service
"""
import unittest
from unittest.mock import Mock, patch
from src.services.ai_service import AIService
from src.models.ai_response import RetrievedContext, ConfidenceLevel, GroundingStatus


class TestAIService(unittest.TestCase):
    
    def setUp(self):
        self.ai_service = AIService()
    
    @patch('src.services.qdrant_service.QdrantRetrievalService.search_relevant_chunks')
    @patch('src.services.llm_service.LLMService.generate_response')
    def test_get_answer_with_general_query(self, mock_llm_generate, mock_qdrant_search):
        # Arrange
        mock_qdrant_search.return_value = [
            RetrievedContext(
                context_id="ctx1",
                query_id="query123",
                content_id="content1",
                text_chunk="This is relevant textbook content",
                similarity_score=0.85,
                chapter="Chapter 3",
                section="3.2",
                page_number=45
            )
        ]
        mock_llm_generate.return_value = "This is the generated response based on textbook content"
        
        # Act
        result = self.ai_service.get_answer(
            query="What is embodied cognition?",
            book_id="physical-ai-humanoid-textbook",
            session_id="session456"
        )
        
        # Assert
        self.assertEqual(result.response_text, "This is the generated response based on textbook content")
        self.assertEqual(result.confidence_level, ConfidenceLevel.MEDIUM)  # Based on similarity score
        self.assertEqual(result.grounding_status, GroundingStatus.VALID)
        self.assertEqual(len(result.citations), 1)
        self.assertIn("Chapter 3", result.citations[0])
    
    @patch('src.services.qdrant_service.QdrantRetrievalService.bypass_retrieval_for_selected_text')
    @patch('src.services.llm_service.LLMService.generate_response')
    def test_get_answer_with_selected_text(self, mock_llm_generate, mock_qdrant_bypass):
        # Arrange
        mock_qdrant_bypass.return_value = [
            RetrievedContext(
                context_id="selected_text",
                query_id="query123",
                content_id="selected_text",
                text_chunk="This is selected textbook content",
                similarity_score=1.0,
                chapter="Selected Text",
                section="User Selection",
                page_number=0
            )
        ]
        mock_llm_generate.return_value = "This is the response based on selected text"
        
        # Act
        result = self.ai_service.get_answer(
            query="Explain this concept?",
            book_id="physical-ai-humanoid-textbook",
            session_id="session456",
            selected_text="This is selected textbook content"
        )
        
        # Assert
        self.assertEqual(result.response_text, "This is the response based on selected text")
        self.assertEqual(result.confidence_level, ConfidenceLevel.HIGH)  # Perfect similarity score
        self.assertEqual(result.grounding_status, GroundingStatus.VALID)
        self.assertEqual(len(result.citations), 1)
        self.assertIn("Selected Text", result.citations[0])
    
    def test_calculate_confidence_high(self):
        # Arrange
        contexts = [
            RetrievedContext(
                context_id="ctx1",
                query_id="query123",
                content_id="content1",
                text_chunk="Content 1",
                similarity_score=0.85,
                chapter="Chapter 1",
                section="1.1",
                page_number=10
            ),
            RetrievedContext(
                context_id="ctx2",
                query_id="query123",
                content_id="content2",
                text_chunk="Content 2",
                similarity_score=0.90,
                chapter="Chapter 1",
                section="1.2",
                page_number=12
            )
        ]
        
        # Act
        confidence = self.ai_service._calculate_confidence(contexts)
        
        # Assert
        self.assertEqual(confidence, ConfidenceLevel.HIGH)
    
    def test_calculate_confidence_low(self):
        # Arrange
        contexts = [
            RetrievedContext(
                context_id="ctx1",
                query_id="query123",
                content_id="content1",
                text_chunk="Content 1",
                similarity_score=0.40,
                chapter="Chapter 1",
                section="1.1",
                page_number=10
            ),
            RetrievedContext(
                context_id="ctx2",
                query_id="query123",
                content_id="content2",
                text_chunk="Content 2",
                similarity_score=0.35,
                chapter="Chapter 1",
                section="1.2",
                page_number=12
            )
        ]
        
        # Act
        confidence = self.ai_service._calculate_confidence(contexts)
        
        # Assert
        self.assertEqual(confidence, ConfidenceLevel.LOW)


if __name__ == '__main__':
    unittest.main()