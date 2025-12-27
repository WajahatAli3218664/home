"""
Ask API endpoint with question, book_id, session_id parameters
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from ..services.ai_service import AIService
from ..api.errors import handle_validation_error, ExternalKnowledgeError, InvalidQueryError
from ..middleware.rate_limit import check_rate_limit


router = APIRouter(prefix="/api/v1")

# Request models
class AskRequest(BaseModel):
    question: str
    book_id: str
    session_id: str
    selected_text: Optional[str] = None


class AskResponse(BaseModel):
    response: str
    citations: List[str]
    session_id: str
    response_id: str
    grounding_status: str


class CitationsResponse(BaseModel):
    citations: List[dict]


class ValidationRequest(BaseModel):
    response_text: str
    context_chunks: List[dict]


class ValidationResponse(BaseModel):
    is_valid: bool
    confidence: float
    message: str


# Initialize AI service
ai_service = AIService()


@router.post("/ask", response_model=AskResponse)
async def process_ask_request(request: AskRequest, req: Request):
    """
    Process a user question and return a response based on textbook content with citations.
    """
    # Check rate limit
    check_rate_limit(req)
    
    try:
        # Validate input parameters
        if not request.question or len(request.question.strip()) == 0:
            raise InvalidQueryError("Question cannot be empty")
        
        if not request.book_id:
            raise HTTPException(
                status_code=422,
                detail={
                    "loc": ["body", "book_id"],
                    "msg": "Book ID is required",
                    "type": "value_error.missing"
                }
            )
        
        if not request.session_id:
            raise HTTPException(
                status_code=422,
                detail={
                    "loc": ["body", "session_id"],
                    "msg": "Session ID is required",
                    "type": "value_error.missing"
                }
            )
        
        # If selected text is provided, validate it
        if request.selected_text:
            if len(request.selected_text.strip()) < 5:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "loc": ["body", "selected_text"],
                        "msg": "Selected text is too short to be meaningful",
                        "type": "value_error.too_short"
                    }
                )
        
        # Process the question using AI service
        result = ai_service.get_answer(
            query=request.question,
            book_id=request.book_id,
            session_id=request.session_id,
            selected_text=request.selected_text
        )
        
        # Create response
        response = AskResponse(
            response=result.response_text,
            citations=result.citations,
            session_id=request.session_id,
            response_id=result.response_id,
            grounding_status=result.grounding_status.value
        )
        
        return response
    
    except InvalidQueryError as e:
        # Re-raise our custom exception
        raise e
    except ExternalKnowledgeError as e:
        # Re-raise our custom exception
        raise e
    except HTTPException:
        # Re-raise FastAPI HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/citations", response_model=CitationsResponse)
async def get_citations(content_id: str, book_id: str, req: Request):
    """
    Retrieve citation information for textbook content.
    """
    # Check rate limit
    check_rate_limit(req)
    
    # This would typically fetch from a database
    # For now, we'll return a placeholder response as a demonstration
    # In a real implementation, this would retrieve actual citation data
    return CitationsResponse(
        citations=[
            {
                "content_id": content_id,
                "chapter": "Chapter 3",
                "section": "3.2 Embodied Cognition Principles",
                "page": 45,
                "citation_format": "Chapter 3 - Embodied Cognition Principles"
            }
        ]
    )


@router.post("/validate", response_model=ValidationResponse)
async def validate_response(request: ValidationRequest, req: Request):
    """
    Validate if a response is properly grounded in textbook content.
    """
    # Check rate limit
    check_rate_limit(req)
    
    # This would typically perform semantic validation
    # For now, we'll return a placeholder response as a demonstration
    # In a real implementation, this would validate against the actual textbook content
    
    # Simple heuristic: if response contains phrases indicating lack of information, mark as invalid
    if "not available in the textbook" in request.response_text.lower():
        return ValidationResponse(
            is_valid=False,
            confidence=0.95,
            message="Response correctly indicates information is not available in the textbook"
        )
    
    # For demonstration purposes, we'll assume the response is valid if it's not empty
    if request.response_text.strip():
        return ValidationResponse(
            is_valid=True,
            confidence=0.85,
            message="Response appears to be grounded in textbook content"
        )
    else:
        return ValidationResponse(
            is_valid=False,
            confidence=0.1,
            message="Response is empty or invalid"
        )