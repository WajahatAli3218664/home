from fastapi import APIRouter
from . import textbook_routes, learning_module_routes, user_routes
from . import chapters, chat, learning_materials, progress, translation
from . import ask

# Create the main API router
api_router = APIRouter()

# Include health check
@api_router.get("/health")
def health_check():
    return {"status": "healthy", "message": "Textbook Generation API is running"}

# Include sub-routers
api_router.include_router(textbook_routes.router, prefix="/textbooks", tags=["Textbooks"])
api_router.include_router(learning_module_routes.router, prefix="/modules", tags=["Learning Modules"])
api_router.include_router(user_routes.router, prefix="/users", tags=["Users"])
api_router.include_router(chapters.router, prefix="/chapters", tags=["Chapters"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])  # This will include the chat routes with authentication
api_router.include_router(ask.router, prefix="/ask", tags=["AI Assistant"])  # This will include the AI assistant routes
api_router.include_router(learning_materials.router, prefix="/learning-materials", tags=["Learning Materials"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
api_router.include_router(translation.router, prefix="/translation", tags=["Translation"])