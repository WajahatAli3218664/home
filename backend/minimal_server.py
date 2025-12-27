from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import random

# Get configuration from environment variables with defaults
API_TITLE = os.getenv("API_TITLE", "Textbook Generation API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API for generating textbooks using AI")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to the specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEXT_OPTIONS = [
    "Welcome to the Physical AI & Humanoid Robotics Textbook!",
    "Advanced robotics combines mechanical engineering, electrical engineering, and computer science.",
    "Machine learning algorithms enable robots to adapt to new environments.",
    "Humanoid robots represent one of the most challenging areas in robotics research.",
    "Kinematics and dynamics are fundamental concepts in robot motion planning.",
    "Artificial intelligence is revolutionizing the capabilities of autonomous systems.",
    "Sensor fusion allows robots to perceive their environment accurately.",
    "Control theory provides the mathematical foundation for robotic movement.",
    "Computer vision enables robots to interpret visual information from cameras.",
    "Natural language processing allows humans to interact with robots using speech."
]

@app.get("/")
def read_root():
    return {"message": "Textbook Generation API is running!"}

@app.get("/generate-text")
def generate_text():
    """Generate a random text related to robotics and AI"""
    text = random.choice(TEXT_OPTIONS)
    return {"text": text}

@app.get("/generate-text-multiple")
def generate_text_multiple(count: int = 5):
    """Generate multiple random texts related to robotics and AI"""
    texts = [random.choice(TEXT_OPTIONS) for _ in range(min(count, 10))]  # Limit to 10
    return {"texts": texts}

if __name__ == "__main__":
    import uvicorn
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "3000"))
    uvicorn.run("minimal_server:app", host=HOST, port=PORT, reload=DEBUG)