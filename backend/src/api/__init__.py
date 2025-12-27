from fastapi import APIRouter

# Main API router
api_router = APIRouter()

# Import and include sub-routers
from .v1 import router as v1_router
from .chapters import router as chapters_router
from .progress import router as progress_router
from .chat import router as chat_router
from .translation import router as translation_router
from .learning_materials import router as learning_materials_router
from .user import router as user_router

# Include the routers
api_router.include_router(v1_router, prefix="/v1", tags=["v1"])
api_router.include_router(chapters_router, prefix="/chapters", tags=["chapters"])
api_router.include_router(progress_router, prefix="/progress", tags=["progress"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(translation_router, prefix="/translation", tags=["translation"])
api_router.include_router(learning_materials_router, prefix="/learning-materials", tags=["learning-materials"])
api_router.include_router(user_router, prefix="/user", tags=["user"])