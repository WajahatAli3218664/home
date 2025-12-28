import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import groq

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Physical AI Textbook API",
    description="API for Physical AI & Humanoid Robotics Textbook with RAG Chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "https://*.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    confidence: float = 0.8

@app.get("/")
def read_root():
    return {"message": "Physical AI Textbook API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Simple chat endpoint using Groq"""
    try:
        # Create a context-aware prompt for Physical AI textbook
        system_prompt = """You are an AI assistant for a Physical AI & Humanoid Robotics textbook. 
        You help students understand concepts related to:
        - Humanoid robot design and mechanics
        - Locomotion and bipedal walking
        - Manipulation and grasping
        - Perception and sensing systems
        - AI planning and decision making
        - Control systems and dynamics
        - Machine learning for robotics
        - Human-robot interaction
        
        Provide clear, educational responses in both English and Urdu when requested.
        Keep responses concise but informative."""
        
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chat_message.message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return ChatResponse(
            response=response.choices[0].message.content,
            confidence=0.8
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/api/v1/chapters")
def get_chapters():
    """Get list of textbook chapters"""
    chapters = [
        {"id": 1, "title": "Foundations of Physical AI", "slug": "foundations-of-physical-ai"},
        {"id": 2, "title": "Humanoid Robot Design Principles", "slug": "humanoid-robot-design-principles"},
        {"id": 3, "title": "Locomotion and Bipedal Walking", "slug": "locomotion-and-bipedal-walking"},
        {"id": 4, "title": "Manipulation and Grasping", "slug": "manipulation-and-grasping"},
        {"id": 5, "title": "Perception and Sensing", "slug": "perception-and-sensing"},
        {"id": 6, "title": "Planning and Decision Making", "slug": "planning-and-decision-making"},
        {"id": 7, "title": "Control Systems and Dynamics", "slug": "control-systems-and-dynamics"},
        {"id": 8, "title": "Learning and Adaptation", "slug": "learning-and-adaptation"},
        {"id": 9, "title": "Human-Robot Interaction", "slug": "human-robot-interaction"},
        {"id": 10, "title": "Applications and Use Cases", "slug": "applications-and-use-cases"},
        {"id": 11, "title": "Ethics and Society", "slug": "ethics-and-society"},
        {"id": 12, "title": "Future Directions", "slug": "future-directions-and-conclusions"}
    ]
    return {"chapters": chapters}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)