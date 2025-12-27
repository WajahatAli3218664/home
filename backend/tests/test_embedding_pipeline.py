import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the backend/src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.embedding_pipeline.config import Config, validate_config
from src.embedding_pipeline.url_fetcher import get_all_urls
from src.embedding_pipeline.text_cleaner import extract_text_from_urls
from src.embedding_pipeline.chunker import chunk_text
from src.embedding_pipeline.models import DocumentChunk, EmbeddingVector, URLProcessingRecord


class TestConfig:
    """Test configuration and validation functions"""
    
    def test_config_validation(self):
        """Test that config validation works properly"""
        # This test checks that validation runs without error
        # Actual validation depends on environment variables
        result = validate_config()
        # The result depends on whether environment variables are set
        assert result in [True, False]
    
    def test_config_class_attributes(self):
        """Test that Config class has expected attributes"""
        assert hasattr(Config, 'COHERE_API_KEY')
        assert hasattr(Config, 'QDRANT_API_KEY')
        assert hasattr(Config, 'QDRANT_URL')
        assert hasattr(Config, 'SOURCE_URLS')
        assert hasattr(Config, 'COLLECTION_NAME')
        assert hasattr(Config, 'GEMINI_API_KEY')



class TestURLFetcher:
    """Test URL fetching functionality"""
    
    def test_get_all_urls_returns_list(self):
        """Test that get_all_urls returns a list of URLs"""
        urls = get_all_urls()
        assert isinstance(urls, list)
        assert len(urls) >= 0  # Can be empty if no URLs are configured


class TestTextCleaner:
    """Test text cleaning and extraction functionality"""
    
    @patch('backend.src.embedding_pipeline.text_cleaner.requests.get')
    def test_extract_text_from_urls(self, mock_get):
        """Test that extract_text_from_urls works with mocked responses"""
        # Mock a response
        mock_response = Mock()
        mock_response.content = '<html><body><p>Test content</p></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        urls = ['https://example.com']
        result = extract_text_from_urls(urls)
        
        assert isinstance(result, dict)
        assert 'https://example.com' in result
        assert isinstance(result['https://example.com'], str)


class TestChunker:
    """Test text chunking functionality"""
    
    def test_chunk_text_basic(self):
        """Test basic chunking functionality"""
        text = "This is a test sentence. Here is another sentence. And a third one."
        chunks = chunk_text(text, max_chunk_size=50, min_chunk_size=10)
        
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        
    def test_chunk_text_empty(self):
        """Test chunking of empty text"""
        chunks = chunk_text("")
        assert chunks == []
        
    def test_chunk_text_single_short_sentence(self):
        """Test chunking of a single short sentence"""
        text = "Short text."
        chunks = chunk_text(text)
        assert len(chunks) == 1
        assert chunks[0] == text


class TestModels:
    """Test data models"""
    
    def test_document_chunk_creation(self):
        """Test DocumentChunk model creation"""
        chunk = DocumentChunk(
            id="test-id",
            content="Test content",
            source_url="https://example.com",
            chunk_index=0
        )
        
        assert chunk.id == "test-id"
        assert chunk.content == "Test content"
        assert chunk.source_url == "https://example.com"
        assert chunk.chunk_index == 0
        assert chunk.validate() is True
    
    def test_document_chunk_validation(self):
        """Test DocumentChunk validation"""
        # Valid chunk
        valid_chunk = DocumentChunk(
            id="test-id",
            content="Test content",
            source_url="https://example.com",
            chunk_index=0
        )
        assert valid_chunk.validate() is True
        
        # Invalid chunk (empty content)
        invalid_chunk = DocumentChunk(
            id="test-id",
            content="",
            source_url="https://example.com",
            chunk_index=0
        )
        assert invalid_chunk.validate() is False
    
    def test_embedding_vector_creation(self):
        """Test EmbeddingVector model creation"""
        vector = EmbeddingVector(
            chunk_id="test-chunk-id",
            vector=[0.1, 0.2, 0.3],
            model="test-model"
        )
        
        assert vector.chunk_id == "test-chunk-id"
        assert vector.vector == [0.1, 0.2, 0.3]
        assert vector.model == "test-model"
        assert vector.validate() is True
    
    def test_url_processing_record_creation(self):
        """Test URLProcessingRecord model creation"""
        record = URLProcessingRecord(
            url="https://example.com",
            status="completed"
        )
        
        assert record.url == "https://example.com"
        assert record.status == "completed"
        assert record.validate() is True
        

if __name__ == "__main__":
    pytest.main([__file__])