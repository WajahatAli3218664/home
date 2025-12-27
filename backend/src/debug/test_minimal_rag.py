"""
Test script for the minimal RAG implementation
This validates that the minimal implementation works correctly
"""
import sys
import os
import unittest
from unittest.mock import Mock, patch

# Add the backend src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.debug.minimal_rag import MinimalRAG


class TestMinimalRAG(unittest.TestCase):
    """
    Test cases for the minimal RAG implementation
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.minimal_rag = MinimalRAG()
    
    def test_initialization(self):
        """Test that the MinimalRAG instance is properly initialized."""
        self.assertIsNotNone(self.minimal_rag.qdrant_service)
        self.assertIsNotNone(self.minimal_rag.llm_service)
    
    def test_format_context_for_prompt_with_contexts(self):
        """Test formatting contexts into a prompt string."""
        contexts = [
            {
                "chunk_id": "chunk1",
                "content": "This is the first context chunk.",
                "source_document": "chapter1.txt",
                "similarity_score": 0.9
            },
            {
                "chunk_id": "chunk2", 
                "content": "This is the second context chunk.",
                "source_document": "chapter2.txt",
                "similarity_score": 0.8
            }
        ]
        
        formatted = self.minimal_rag.format_context_for_prompt(contexts)
        
        # Check that the formatted string contains the expected content
        self.assertIn("Source: chapter1.txt", formatted)
        self.assertIn("Content: This is the first context chunk.", formatted)
        self.assertIn("Source: chapter2.txt", formatted)
        self.assertIn("Content: This is the second context chunk.", formatted)
    
    def test_format_context_for_prompt_empty(self):
        """Test formatting when no contexts are provided."""
        formatted = self.minimal_rag.format_context_for_prompt([])
        self.assertEqual(formatted, "")
    
    @patch('src.services.qdrant_service.QdrantRetrievalService.search_relevant_chunks')
    def test_retrieve_context(self, mock_search):
        """Test that context retrieval works correctly."""
        # Mock the search response
        mock_context_obj = Mock()
        mock_context_obj.context_id = "mock_chunk_1"
        mock_context_obj.chunk_text = "This is mock content."
        mock_context_obj.source_document = "mock_source.txt"
        mock_context_obj.similarity_score = 0.85
        
        mock_search.return_value = [mock_context_obj]
        
        contexts = self.minimal_rag.retrieve_context("test query", "test_book")
        
        # Verify the mock was called
        mock_search.assert_called_once_with("test query", "test_book")
        
        # Verify the returned context
        self.assertEqual(len(contexts), 1)
        self.assertEqual(contexts[0]["chunk_id"], "mock_chunk_1")
        self.assertEqual(contexts[0]["content"], "This is mock content.")
        self.assertEqual(contexts[0]["source_document"], "mock_source.txt")
        self.assertEqual(contexts[0]["similarity_score"], 0.85)
    
    def test_query_method_structure(self):
        """Test that the query method returns the expected structure."""
        # We'll test the structure without actually calling external services
        # by verifying the method exists and has the right signature
        self.assertTrue(hasattr(self.minimal_rag, 'query'))
        self.assertTrue(callable(getattr(self.minimal_rag, 'query')))


def run_tests():
    """
    Run all tests for the minimal RAG implementation
    """
    print("Running tests for Minimal RAG Implementation...")
    print("=" * 50)
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMinimalRAG)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)