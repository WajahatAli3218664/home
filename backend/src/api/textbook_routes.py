from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.auth.authentication import get_current_active_user, get_db
from src.models.textbook_models import User, Textbook
from src.models.textbook_models import LearningModule
from src.auth.authentication import get_current_user

router = APIRouter()


@router.get("/", response_model=None)
def get_textbooks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get a list of textbooks for the current user."""
    textbooks = db.query(Textbook).filter(Textbook.owner_id == current_user.id).offset(skip).limit(limit).all()
    return textbooks


@router.get("/{textbook_id}", response_model=None)
def get_textbook(
    textbook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific textbook by ID."""
    textbook = db.query(Textbook).filter(Textbook.id == textbook_id, Textbook.owner_id == current_user.id).first()
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    return textbook


@router.post("/", response_model=None)
def create_textbook(
    title: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new textbook."""
    textbook = Textbook(
        title=title,
        description=description,
        owner_id=current_user.id
    )
    db.add(textbook)
    db.commit()
    db.refresh(textbook)
    return textbook


@router.put("/{textbook_id}", response_model=None)
def update_textbook(
    textbook_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    content: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing textbook."""
    textbook = db.query(Textbook).filter(Textbook.id == textbook_id, Textbook.owner_id == current_user.id).first()
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    if title is not None:
        textbook.title = title
    if description is not None:
        textbook.description = description
    if content is not None:
        textbook.content = content
    
    db.commit()
    db.refresh(textbook)
    return textbook


@router.delete("/{textbook_id}")
def delete_textbook(
    textbook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a textbook."""
    textbook = db.query(Textbook).filter(Textbook.id == textbook_id, Textbook.owner_id == current_user.id).first()
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    db.delete(textbook)
    db.commit()
    return {"message": "Textbook deleted successfully"}