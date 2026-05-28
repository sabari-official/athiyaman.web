from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from backend.repositories.base import BaseRepository
from backend.database.models import Team

class TeamRepository(BaseRepository[Team]):
    """TeamRepository handles database CRUD and custom lookups for Team entities."""
    def __init__(self, db: Session):
        super().__init__(Team, db)

    def get_by_code(self, team_code: str) -> Optional[Team]:
        """Fetch team record matching the unique alphanumeric team code."""
        return self.db.query(self.model).filter(self.model.team_code == team_code).first()

    def get_by_name(self, team_name: str) -> Optional[Team]:
        """Fetch team record matching the unique team name."""
        return self.db.query(self.model).filter(self.model.team_name == team_name).first()

    def get_by_leader_id(self, leader_id: UUID) -> Optional[Team]:
        """Fetch team record matching the unique Leader user ID."""
        return self.db.query(self.model).filter(self.model.leader_id == leader_id).first()
