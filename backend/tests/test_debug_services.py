"""
Unit tests for the debug services
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.services.debug_service import DebugService
from src.models.debug_log import DebugLog


class TestDebugService:
    """
    Test cases for the DebugService
    """
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.debug_service = DebugService()
    
    def test_initialization(self):
        """Test that the DebugService is properly initialized."""
        assert self.debug_service.recent_contexts == []
        assert self.debug_service.max_stored_contexts == 10
    
    def test_log_context_flow(self):
        """Test logging context flow."""
        component = "TestComponent"
        message = "Test message"
        context_data = {"test_key": "test_value"}
        
        log_entry = self.debug_service.log_context_flow(
            component=component,
            message=message,
            context_data=context_data,
            level="info"
        )
        
        # Verify the log entry is returned
        assert isinstance(log_entry, DebugLog)
        assert log_entry.component == component
        assert log_entry.message == message
        assert log_entry.level == "info"
        
        # Verify the context was stored
        recent_contexts = self.debug_service.get_recent_contexts()
        assert len(recent_contexts) == 1
        assert recent_contexts[0]["test_key"] == "test_value"
    
    def test_get_recent_contexts(self):
        """Test retrieving recent contexts."""
        # Add a context
        self.debug_service.log_context_flow(
            component="Test",
            message="Test message",
            context_data={"query": "test query", "response": "test response"}
        )
        
        recent_contexts = self.debug_service.get_recent_contexts()
        assert len(recent_contexts) == 1
        assert recent_contexts[0]["user_query"] == "test query"
        assert recent_contexts[0]["llm_response"] == "test response"
    
    def test_get_latest_context(self):
        """Test retrieving the latest context."""
        # Add two contexts
        self.debug_service.log_context_flow(
            component="Test1",
            message="Test message 1",
            context_data={"query": "query 1", "response": "response 1"}
        )
        
        self.debug_service.log_context_flow(
            component="Test2",
            message="Test message 2", 
            context_data={"query": "query 2", "response": "response 2"}
        )
        
        latest_context = self.debug_service.get_latest_context()
        assert latest_context["user_query"] == "query 2"
        assert latest_context["llm_response"] == "response 2"
    
    def test_clear_recent_contexts(self):
        """Test clearing recent contexts."""
        # Add a context
        self.debug_service.log_context_flow(
            component="Test",
            message="Test message",
            context_data={"query": "test", "response": "response"}
        )
        
        # Verify it was added
        assert len(self.debug_service.recent_contexts) == 1
        
        # Clear contexts
        self.debug_service.clear_recent_contexts()
        
        # Verify it's empty
        assert len(self.debug_service.recent_contexts) == 0
        assert self.debug_service.get_latest_context() is None


class TestPromptFormatter:
    """
    Test cases for the PromptFormatter utility
    """
    
    def test_format_rag_prompt(self):
        """Test formatting a RAG prompt."""
        from src.utils.prompt_formatter import PromptFormatter
        
        query = "What is robot kinematics?"
        context = "Robot kinematics is the study of motion in robotic systems."
        
        result = PromptFormatter.format_rag_prompt(query, context)
        
        assert "system" in result
        assert "user" in result
        assert query in result["user"]
        assert context in result["user"]
    
    def test_validate_prompt_components_valid(self):
        """Test validation of valid prompt components."""
        from src.utils.prompt_formatter import PromptFormatter
        
        query = "What is robot kinematics?"
        context = "Robot kinematics is the study of motion in robotic systems."
        
        validation = PromptFormatter.validate_prompt_components(query, context)
        
        assert validation["query_valid"] is True
        assert validation["context_valid"] is True
        assert len(validation["suggestions"]) == 0
    
    def test_validate_prompt_components_empty_context(self):
        """Test validation with empty context."""
        from src.utils.prompt_formatter import PromptFormatter
        
        query = "What is robot kinematics?"
        context = ""
        
        validation = PromptFormatter.validate_prompt_components(query, context)
        
        assert validation["query_valid"] is True
        assert validation["context_valid"] is False
        assert "Context is empty" in validation["suggestions"][0]
    
    def test_validate_prompt_components_empty_query(self):
        """Test validation with empty query."""
        from src.utils.prompt_formatter import PromptFormatter
        
        query = ""
        context = "Robot kinematics is the study of motion in robotic systems."
        
        validation = PromptFormatter.validate_prompt_components(query, context)
        
        assert validation["query_valid"] is False
        assert validation["context_valid"] is True
        assert "Query is empty" in validation["suggestions"][0]