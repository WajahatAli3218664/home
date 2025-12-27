"""
Minimal Working Example for /api/v1/chat Endpoint

This file demonstrates a minimal working implementation of a chat endpoint
that will resolve the 404 error you're experiencing.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

# Define request/response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Create a new FastAPI app for demonstration
app = FastAPI(title="Minimal Chat API")

@app.post("/api/v1/chat/")
async def chat_endpoint(request: ChatRequest):
    """
    A minimal chat endpoint that responds to user queries.
    
    Why the 404 error occurs in the original setup:
    1. Authentication required: Many chat endpoints require authentication tokens
    2. Import errors: Missing dependencies can prevent routers from loading
    3. Incorrect mounting: Endpoints may not be mounted at the expected path
    4. Conditional loading: Routers might be conditionally included based on imports
    
    This endpoint avoids those issues by being simple and self-contained.
    """
    # Simple echo response - in a real implementation, this would connect to your LLM/RAG system
    response_text = f"Echo: {request.message}. This is a response from the working chat endpoint!"
    return ChatResponse(response=response_text)

@app.get("/")
def read_root():
    return {"message": "Minimal Chat API is running!"}

if __name__ == "__main__":
    # Run the server
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=HOST, port=PORT)