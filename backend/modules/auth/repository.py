from typing import Optional
from sqlalchemy.orm import Session
from backend.repositories.base import BaseRepository
from backend.database.models import User

class UserRepository(BaseRepository[User]):
    """UserRepository implements database query operations for user entities."""
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> Optional[User]:
        """Fetch user record matching the unique username."""
        return self.db.query(self.model).filter(self.model.username == username).first()

    def get_by_phone_number(self, phone_number: str) -> Optional[User]:
        """Fetch user record matching the unique phone number."""
        return self.db.query(self.model).filter(self.model.phone_number == phone_number).first()
