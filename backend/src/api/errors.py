"""
Base API error handling for textbook AI assistant
"""
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional


class APIError(BaseModel):
    """
    Standard API error response model
    """
    detail: str
    error_code: Optional[str] = None
    additional_info: Optional[dict] = None


class TextbookAIException(HTTPException):
    """
    Custom exception for textbook AI assistant specific errors
    """
    def __init__(
        self, 
        status_code: int, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "detail": detail,
                "error_code": error_code,
                "additional_info": additional_info
            }
        )


# Specific exception classes for different error scenarios
class ContentNotFoundError(TextbookAIException):
    """
    Raised when no relevant textbook content is found for a query
    """
    def __init__(self, detail: str = "No relevant textbook content found for the query"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="CONTENT_NOT_FOUND"
        )


class InvalidQueryError(TextbookAIException):
    """
    Raised when a query is invalid or malformed
    """
    def __init__(self, detail: str = "Invalid query provided"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="INVALID_QUERY"
        )


class ExternalKnowledgeError(TextbookAIException):
    """
    Raised when a query requires external knowledge not available in the textbook
    """
    def __init__(self, detail: str = "This information is not available in the textbook."):
        super().__init__(
            status_code=status.HTTP_200_OK,  # 200 because it's a valid response indicating lack of info
            detail=detail,
            error_code="EXTERNAL_KNOWLEDGE_REQUIRED"
        )


class ConfigurationError(TextbookAIException):
    """
    Raised when there's a configuration issue
    """
    def __init__(self, detail: str = "Configuration error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="CONFIGURATION_ERROR"
        )


# Error handling middleware/utils
def handle_validation_error(errors):
    """
    Format validation errors in a consistent way
    """
    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            "loc": error.get("loc", []),
            "msg": error.get("msg", "Validation error"),
            "type": error.get("type", "value_error")
        })
    
    return {
        "detail": formatted_errors
    }