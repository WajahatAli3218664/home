from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.auth.authentication import get_current_active_user, get_db
from src.models.textbook_models import User, Textbook, LearningModule
from src.auth.authentication import get_current_user

router = APIRouter()


@router.get("/", response_model=List[LearningModule])
def get_learning_modules(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get a list of learning modules for the current user's textbooks."""
    modules = db.query(LearningModule).join(Textbook).filter(
        Textbook.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return modules


@router.get("/{module_id}", response_model=LearningModule)
def get_learning_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific learning module by ID."""
    module = db.query(LearningModule).join(Textbook).filter(
        LearningModule.id == module_id,
        Textbook.owner_id == current_user.id
    ).first()
    
    if not module:
        raise HTTPException(status_code=404, detail="Learning module not found")
    return module


@router.post("/", response_model=LearningModule)
def create_learning_module(
    title: str,
    content: str,
    textbook_id: int,
    position: Optional[int] = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new learning module."""
    # Verify that the textbook belongs to the current user
    textbook = db.query(Textbook).filter(
        Textbook.id == textbook_id,
        Textbook.owner_id == current_user.id
    ).first()
    
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found or access denied")
    
    module = LearningModule(
        title=title,
        content=content,
        textbook_id=textbook_id,
        author_id=current_user.id,
        position=position
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


@router.put("/{module_id}", response_model=LearningModule)
def update_learning_module(
    module_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    position: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing learning module."""
    module = db.query(LearningModule).join(Textbook).filter(
        LearningModule.id == module_id,
        Textbook.owner_id == current_user.id
    ).first()
    
    if not module:
        raise HTTPException(status_code=404, detail="Learning module not found")
    
    if title is not None:
        module.title = title
    if content is not None:
        module.content = content
    if position is not None:
        module.position = position
    
    db.commit()
    db.refresh(module)
    return module


@router.delete("/{module_id}")
def delete_learning_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a learning module."""
    module = db.query(LearningModule).join(Textbook).filter(
        LearningModule.id == module_id,
        Textbook.owner_id == current_user.id
    ).first()
    
    if not module:
        raise HTTPException(status_code=404, detail="Learning module not found")
    
    db.delete(module)
    db.commit()
    return {"message": "Learning module deleted successfully"}