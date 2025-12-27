from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.auth.authentication import get_current_active_user, get_db
from src.models.textbook_models import User
from src.auth.authentication import get_current_user

router = APIRouter()


@router.get("/me", response_model=dict)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get the current user's profile information."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }


@router.put("/me", response_model=dict)
def update_current_user_profile(
    username: str = None,
    email: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update the current user's profile information."""
    if username is not None:
        current_user.username = username
    if email is not None:
        current_user.email = email
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }


@router.get("/{user_id}", response_model=dict)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific user by ID (for admin functionality or future extensions)."""
    # For now, only allow users to get their own information
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }