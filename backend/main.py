import os
import sys
import random
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the Python path to allow imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.api.routers import api_router
    from src.auth.routes import router as auth_router
    # Import the RAG service to load textbook content
    from src.services.rag_service import load_textbook_content_from_docs
except ImportError as e:
    print(f"Import error: {e}")
    # If the modules don't exist, we'll continue without them
    api_router = None
    auth_router = None
    load_textbook_content_from_docs = None

# Import our simple chat endpoint
try:
    from simple_chat import router as simple_chat_router
except ImportError as e:
    print(f"Simple chat import error: {e}")
    simple_chat_router = None

# Get configuration from environment variables with defaults
API_TITLE = os.getenv("API_TITLE", "Textbook Generation API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API for generating textbooks using AI")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load textbook content when the application starts
    if load_textbook_content_from_docs:
        print("Loading textbook content into RAG system...")
        try:
            load_textbook_content_from_docs()
            print("Textbook content loaded successfully!")
        except Exception as e:
            print(f"Error loading textbook content: {e}")
    else:
        print("Could not load RAG service - dependencies may be missing")
    yield  # Clean up happens after yield if needed


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    debug=DEBUG,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Default Docusaurus development server
        "http://localhost:3001",      # Alternative Docusaurus development server
        "http://127.0.0.1:3000",      # Alternative localhost
        "http://127.0.0.1:8000",      # Backend server (for testing)
        "https://*.hf.space",         # Hugging Face Spaces
        "https://*.vercel.app",       # Vercel deployments
        "https://*.netlify.app",      # Netlify deployments
        "https://*.github.io",        # GitHub Pages
        "https://huggingface.co",      # Hugging Face main site
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers if they exist
if api_router:
    app.include_router(api_router, prefix="/api/v1")
if auth_router:
    app.include_router(auth_router)
if simple_chat_router:
    app.include_router(simple_chat_router, prefix="/api/v1")

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

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "message": "Textbook Generation API is running"}

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
    PORT = int(os.getenv("PORT", "8000"))  # Use PORT for Hugging Face Spaces compatibility
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)