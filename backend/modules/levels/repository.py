from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import Level, TeamLevelProgress, PersonalLevelProgress

class LevelRepository(BaseRepository[Level]):
    """
    LevelRepository implements direct SQL access using SQLAlchemy ORM
    for levels, team progression, and personal progression models.
    """
    def __init__(self, db: Session):
        super().__init__(Level, db)

    def get_levels_master(self) -> List[Level]:
        """Queries all Level master entries ordered by level number."""
        return self.db.query(self.model).order_by(self.model.level_number).all()

    def get_level_by_number(self, level_number: int) -> Optional[Level]:
        """Queries master level definitions matching a specific level number."""
        return self.db.query(self.model).filter(self.model.level_number == level_number).first()

    def get_team_progress(self, team_id: UUID) -> List[TeamLevelProgress]:
        """Queries all team level progression entries matching the team ID."""
        return self.db.query(TeamLevelProgress).filter(
            TeamLevelProgress.team_id == team_id
        ).order_by(TeamLevelProgress.level_number).all()

    def get_personal_progress(self, user_id: UUID) -> List[PersonalLevelProgress]:
        """Queries all personal level progression entries matching the user ID."""
        return self.db.query(PersonalLevelProgress).filter(
            PersonalLevelProgress.user_id == user_id
        ).order_by(PersonalLevelProgress.level_number).all()

    def get_single_team_progress(self, team_id: UUID, level_number: int) -> Optional[TeamLevelProgress]:
        """Queries single team progression entry for a specific level."""
        return self.db.query(TeamLevelProgress).filter(
            TeamLevelProgress.team_id == team_id,
            TeamLevelProgress.level_number == level_number
        ).first()

    def get_single_personal_progress(self, user_id: UUID, level_number: int) -> Optional[PersonalLevelProgress]:
        """Queries single personal progression entry for a specific level."""
        return self.db.query(PersonalLevelProgress).filter(
            PersonalLevelProgress.user_id == user_id,
            PersonalLevelProgress.level_number == level_number
        ).first()
