from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json

from ..services.debug_service import DebugService
from ..models.retrieved_context import RetrievedContext

# Initialize the debug service
debug_service = DebugService()

router = APIRouter(prefix="/debug", tags=["debug"])


class DebugContextResponse(BaseModel):
    """Response model for debug context endpoint"""
    recent_context: Optional[Dict[str, Any]] = None


class ContextFlowRequest(BaseModel):
    """Request model for context flow testing"""
    query: str
    debug: bool = False


class ContextFlowResponse(BaseModel):
    """Response model for context flow testing"""
    query: str
    retrieved_context: List[RetrievedContext]
    llm_prompt: str
    llm_response: str
    debug_info: Optional[Dict[str, Any]] = None


class TestPromptRequest(BaseModel):
    """Request model for prompt testing"""
    user_query: str
    retrieved_context: List[Dict[str, str]]
    custom_prompt_template: Optional[str] = "Based on the following context: {context} Answer the question: {query}"


class TestPromptResponse(BaseModel):
    """Response model for prompt testing"""
    input_prompt: str
    llm_response: str
    processing_time: int


@router.get("/log-context", response_model=DebugContextResponse)
async def get_recent_context():
    """
    Retrieve the most recent context sent to the LLM for debugging purposes.
    """
    latest_context = debug_service.get_latest_context()
    
    if not latest_context:
        raise HTTPException(status_code=404, detail="No recent context found")
    
    return DebugContextResponse(recent_context=latest_context)


@router.get("/context-flow", response_model=ContextFlowResponse)
async def test_context_flow(query: str, debug: bool = False):
    """
    Test the complete flow from query to context retrieval to LLM response.
    """
    from ..services.rag_service import RAGService
    
    rag_service = RAGService()
    
    # For this endpoint, we'll simulate the flow by using a generic book_id
    # In a real implementation, you'd need to specify the book_id
    try:
        result = rag_service.get_answer(query=query, book_id="default_book", session_id="debug_session")
        
        response = ContextFlowResponse(
            query=query,
            retrieved_context=[],  # This would need to be properly mapped from the result
            llm_prompt="N/A",  # This would be the actual prompt sent to the LLM
            llm_response=result.get("response", ""),
            debug_info={"processing_completed": True} if debug else None
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during context flow: {str(e)}")


@router.post("/test-prompt", response_model=TestPromptResponse)
async def test_prompt(request: TestPromptRequest):
    """
    Test a specific prompt with the LLM to verify proper context injection.
    """
    from ..services.llm_service import LLMService
    
    llm_service = LLMService()
    
    # Construct the prompt using the provided template
    context_text = " ".join([ctx["content"] for ctx in request.retrieved_context])
    input_prompt = request.custom_prompt_template.format(
        context=context_text,
        query=request.user_query
    )
    
    import time
    start_time = time.time()
    
    # Generate response using LLM
    llm_response = llm_service.generate_response(
        query=request.user_query,
        context=context_text
    )
    
    processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
    
    return TestPromptResponse(
        input_prompt=input_prompt,
        llm_response=llm_response,
        processing_time=processing_time
    )