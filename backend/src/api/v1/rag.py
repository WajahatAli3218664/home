from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

# Import the RAG service
from src.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()


class RAGQueryRequest(BaseModel):
    query: str
    book_id: str
    session_id: str
    selected_text: Optional[str] = None
    language: Optional[str] = "en"


class RAGQueryResponse(BaseModel):
    query_id: str
    response: str
    confidence_level: str
    session_id: str
    message_id: str
    retrieved_context: list
    response_time: float


@router.post("/rag/query")
async def rag_query(request: RAGQueryRequest):
    """
    Ask a question about book content and get an AI-generated response.

    Request Body:
    {
      "query": "string (question about the book content)",
      "book_id": "string (ID of the book to search in)",
      "session_id": "string (ID of the chat session)",
      "selected_text": "string (optional, if provided, only this text will be used as context)",
      "language": "string (optional, default: 'en')"
    }

    Response (200 OK):
    {
      "query_id": "string",
      "response": "string (AI-generated response)",
      "confidence_level": "string (HIGH|MEDIUM|LOW)",
      "session_id": "string",
      "message_id": "string",
      "retrieved_context": [
        {
          "chunk_id": "string",
          "text": "string",
          "similarity_score": "float"
        }
      ],
      "response_time": "float (time taken in seconds)"
    }
    """
    try:
        import time
        start_time = time.time()

        # Call the RAG service to get the answer
        result = rag_service.get_answer(
            query=request.query,
            book_id=request.book_id,
            session_id=request.session_id,
            selected_text=request.selected_text
        )

        response_time = time.time() - start_time

        # Add response time to the result
        result["response_time"] = round(response_time, 2)
        result["query_id"] = f"query_{request.session_id}_{int(time.time())}"

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing RAG query: {str(e)}")


class SelectedTextQueryRequest(BaseModel):
    query: str
    selected_text: str
    session_id: str
    book_id: str


@router.post("/rag/query-selected")
async def rag_query_selected(request: SelectedTextQueryRequest):
    """
    Ask a question about selected text only and get an AI-generated response.

    Request Body:
    {
      "query": "string (question about the selected text)",
      "selected_text": "string (the selected text to use as context)",
      "session_id": "string (ID of the chat session)",
      "book_id": "string (ID of the book)"
    }

    Response (200 OK):
    {
      "query_id": "string",
      "response": "string (AI-generated response)",
      "confidence_level": "string (HIGH|MEDIUM|LOW)",
      "session_id": "string",
      "message_id": "string",
      "retrieved_context": [
        {
          "chunk_id": "string",
          "text": "string",
          "similarity_score": "float"
        }
      ],
      "response_time": "float (time taken in seconds)"
    }
    """
    try:
        import time
        start_time = time.time()

        # Call the RAG service with selected text context
        result = rag_service.get_answer(
            query=request.query,
            book_id=request.book_id,
            session_id=request.session_id,
            selected_text=request.selected_text
        )

        response_time = time.time() - start_time

        # Add response time to the result
        result["response_time"] = round(response_time, 2)
        result["query_id"] = f"query_{request.session_id}_{int(start_time)}"

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")