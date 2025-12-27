from fastapi import APIRouter, Depends, HTTPException
from src.database import SessionLocal
from src.models.user import UserProfile


router = APIRouter()


@router.put("/{user_id}")
def update_user_profile(user_id: int, profile_data: dict):
    db = SessionLocal()
    try:
        # Check if profile exists
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        if profile:
            # Update existing profile
            for field, value in profile_data.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)
        else:
            # Create new profile
            profile = UserProfile(user_id=user_id, **{k: v for k, v in profile_data.items() if hasattr(UserProfile, k)})
            db.add(profile)
        
        db.commit()
        db.refresh(profile)
        
        return {"message": "User profile updated successfully", "profile_id": profile.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user profile: {str(e)}")
    finally:
        db.close()