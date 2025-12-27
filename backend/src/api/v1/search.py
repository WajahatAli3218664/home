from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from src.services.retrieval_service import retrieval_service

router = APIRouter()


class SemanticSearchRequest(BaseModel):
    query: str
    book_id: str
    limit: Optional[int] = 10
    filters: Optional[dict] = None


class SearchResult(BaseModel):
    chunk_id: str
    content: str
    similarity_score: float
    metadata: dict


class SemanticSearchResponse(BaseModel):
    results: List[SearchResult]
    search_time: float


@router.post("/search/semantic")
async def semantic_search(request: SemanticSearchRequest):
    """
    Perform semantic search within book content using vector similarity.

    Request Body:
    {
      "query": "string (search query)",
      "book_id": "string (ID of the book to search in)",
      "limit": "integer (optional, number of results to return, default: 10)",
      "filters": {
        "chapter": "string (optional, filter by chapter)",
        "section": "string (optional, filter by section)",
        "language": "string (optional, filter by language)"
      }
    }

    Response (200 OK):
    {
      "results": [
        {
          "chunk_id": "string",
          "content": "string",
          "similarity_score": "float (0.0-1.0)",
          "metadata": {
            "chapter": "string",
            "section": "string",
            "page": "string",
            "language": "string"
          }
        }
      ],
      "search_time": "float (time taken in seconds)"
    }
    """
    try:
        import time
        start_time = time.time()

        # Perform semantic search using the retrieval service
        results = retrieval_service.search_relevant_chunks(
            query=request.query,
            book_id=request.book_id,
            limit=request.limit or 10,
            filters=request.filters
        )

        search_time = time.time() - start_time

        # Format the results
        formatted_results = []
        for result in results:
            formatted_results.append(SearchResult(
                chunk_id=result.get('chunk_id', ''),
                content=result.get('content', ''),
                similarity_score=result.get('similarity_score', 0.0),
                metadata=result.get('metadata', {})
            ))

        return SemanticSearchResponse(
            results=formatted_results,
            search_time=round(search_time, 3)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing semantic search: {str(e)}")