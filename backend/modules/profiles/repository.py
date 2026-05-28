from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from backend.repositories.base import BaseRepository
from backend.database.models import UserProfile

class UserProfileRepository(BaseRepository[UserProfile]):
    """UserProfileRepository handles database CRUD and custom lookups for user profiles."""
    def __init__(self, db: Session):
        super().__init__(UserProfile, db)

    def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        """Fetch user profile record linked to the specific User UUID."""
        return self.db.query(self.model).filter(self.model.user_id == user_id).first()

    def get_by_aadhaar_hash(self, aadhaar_hash: str) -> Optional[UserProfile]:
        """Fetch profile matching the Aadhaar crypt-hash to identify duplicate accounts."""
        return self.db.query(self.model).filter(self.model.aadhaar_hash == aadhaar_hash).first()
