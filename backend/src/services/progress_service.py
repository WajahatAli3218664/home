from typing import List
from src.database import SessionLocal
from src.models.user_progress import UserProgress


class ProgressService:
    def __init__(self):
        self.db = SessionLocal()

    def get_progress_by_user(self, user_id: int) -> List[UserProgress]:
        try:
            progress_records = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).all()
            return progress_records
        finally:
            self.db.close()

    def update_progress(self, user_id: int, chapter_id: int, progress: float) -> UserProgress:
        try:
            progress_record = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.chapter_id == chapter_id
            ).first()
            
            if progress_record:
                progress_record.progress = progress
            else:
                progress_record = UserProgress(
                    user_id=user_id,
                    chapter_id=chapter_id,
                    progress=progress
                )
                self.db.add(progress_record)
            
            self.db.commit()
            self.db.refresh(progress_record)
            return progress_record
        finally:
            self.db.close()