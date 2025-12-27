import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the current directory to Python path to import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app as main_app
from src.services.rag_service import load_textbook_content_from_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load textbook content when the application starts
    print("Loading textbook content into RAG system...")
    load_textbook_content_from_docs()
    print("Textbook content loaded successfully!")
    yield
    # Shutdown logic can go here


# Create the FastAPI app with lifespan
app = FastAPI(
    title=os.getenv("API_TITLE", "Textbook Generation API"),
    description=os.getenv("API_DESCRIPTION", "API for generating textbooks using AI"),
    version=os.getenv("API_VERSION", "1.0.0"),
    lifespan=lifespan
)

# Add CORS middleware - configured for Hugging Face Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.hf.space",         # Hugging Face Spaces
        "https://huggingface.co",     # Hugging Face main site
        "http://localhost:3000",      # Local development
        "http://localhost:3001",      # Alternative local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from the main app
for route in main_app.router.routes:
    app.include_router(route.tags[0] if hasattr(route, 'tags') and route.tags else 'api', route)


# Alternative: Import and include specific routes if the above doesn't work
try:
    from src.api.routers import api_router
    from src.auth.routes import router as auth_router
    
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(auth_router)
except ImportError as e:
    print(f"Error importing routers: {e}")


# Include the main app's endpoints
@app.get("/")
def read_root():
    return {"message": "Textbook Generation API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Textbook Generation API is running"}


if __name__ == "__main__":
    import uvicorn
    # Use the environment-provided port or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)