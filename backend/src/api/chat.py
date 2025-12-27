"""
Chat API endpoint with query, book_id, session_id parameters
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from ..services.rag_service import RAGService
from ..api.errors import handle_validation_error, ExternalKnowledgeError, InvalidQueryError
from ..models.chat_response import ConfidenceLevel
from ..middleware.rate_limit import check_rate_limit


router = APIRouter(prefix="/api/v1")

# Request models
class ChatRequest(BaseModel):
    query: str
    book_id: str
    session_id: str
    selected_text: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    confidence_level: str
    session_id: str
    message_id: str
    retrieved_context: List[dict]


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[dict]


# Initialize RAG service
rag_service = RAGService()


@router.post("/chat", response_model=ChatResponse)
async def process_chat_request(request: ChatRequest, req: Request):
    """
    Process a user query and return a response based on book content.
    """
    # Check rate limit
    check_rate_limit(req)

    try:
        # Validate input parameters
        if not request.query or len(request.query.strip()) == 0:
            raise InvalidQueryError("Query cannot be empty")

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

        # Process the query using RAG service
        result = rag_service.get_answer(
            query=request.query,
            book_id=request.book_id,
            session_id=request.session_id,
            selected_text=request.selected_text
        )

        return ChatResponse(**result)

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


@router.get("/chat/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str, req: Request):
    """
    Retrieve the chat history for a specific session.
    """
    # Check rate limit
    check_rate_limit(req)

    # This would typically fetch from a database
    # For now, we'll return an empty history as a placeholder
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[]
    )


@router.post("/chat/{session_id}/feedback")
async def submit_feedback(session_id: str, req: Request, message_id: str, feedback_type: str, comment: Optional[str] = None):
    """
    Submit feedback on a specific chat response.
    """
    # Check rate limit
    check_rate_limit(req)

    # This would typically store feedback in a database
    # For now, we'll just return a success message
    return {"status": "Feedback received", "message_id": message_id}