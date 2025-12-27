from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Response (200 OK):
    {
      "status": "healthy",
      "timestamp": "datetime"
    }
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }