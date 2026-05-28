from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from backend.database.models import User, Team, Level
from backend.modules.levels.repository import LevelRepository
from backend.modules.levels.schema import TeamLevelProgressResponse, PersonalLevelProgressResponse

class LevelService:
    """
    LevelService coordinates progression checks, sequential milestone calculations,
    and returns formatted progression statuses.
    """
    def __init__(self, db: Session):
        self.db = db
        self.level_repo = LevelRepository(db)

    def get_team_level_progress(self, leader_id: UUID) -> List[TeamLevelProgressResponse]:
        """
        Retrieves Team Progression details (Levels 1-6) for a leader's team.
        Combines active database milestone rows with master requirements.
        """
        # 1. Fetch team associated with leader
        team = self.db.query(Team).filter(
            Team.leader_id == leader_id,
            Team.status == "ACTIVE"
        ).first()
        if not team:
            raise ValueError("TEAM_NOT_FOUND")

        # 2. Fetch Level master rules and filter Team Levels (1-6)
        levels_master = self.level_repo.get_levels_master()
        team_levels_master = [lvl for lvl in levels_master if 1 <= lvl.level_number <= 6]

        # 3. Fetch existing progress rows for the team
        progress_rows = self.level_repo.get_team_progress(team.id)
        progress_map = {row.level_number: row for row in progress_rows}

        responses = []
        for master in team_levels_master:
            lvl_num = master.level_number
            reward = float(master.reward_amount)
            req_val = master.requirement_value

            if lvl_num in progress_map:
                row = progress_map[lvl_num]
                responses.append(TeamLevelProgressResponse(
                    level_number=lvl_num,
                    current_progress=row.current_progress,
                    requirement_value=req_val,
                    completed=row.completed,
                    completed_at=row.completed_at,
                    reward_amount=reward
                ))
            else:
                # Robust Fallback Logic for unpopulated progress levels
                completed = lvl_num < team.current_level
                
                if completed:
                    curr_prog = req_val
                elif lvl_num == team.current_level:
                    curr_prog = team.member_count
                else:
                    curr_prog = 0

                responses.append(TeamLevelProgressResponse(
                    level_number=lvl_num,
                    current_progress=curr_prog,
                    requirement_value=req_val,
                    completed=completed,
                    completed_at=None,
                    reward_amount=reward
                ))

        return responses

    def get_personal_level_progress(self, user_id: UUID) -> List[PersonalLevelProgressResponse]:
        """
        Retrieves Individual Progression details (Levels 7-11) for a user.
        Combines active database milestone rows with master requirements.
        """
        # 1. Fetch user to verify active account
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("USER_NOT_FOUND")

        # 2. Fetch Level master rules and filter Personal Levels (7-11)
        levels_master = self.level_repo.get_levels_master()
        personal_levels_master = [lvl for lvl in levels_master if 7 <= lvl.level_number <= 11]

        # 3. Fetch existing progress rows for the user
        progress_rows = self.level_repo.get_personal_progress(user_id)
        progress_map = {row.level_number: row for row in progress_rows}

        responses = []
        for master in personal_levels_master:
            lvl_num = master.level_number
            reward = float(master.reward_amount)
            req_val = float(master.requirement_value)

            if lvl_num in progress_map:
                row = progress_map[lvl_num]
                responses.append(PersonalLevelProgressResponse(
                    level_number=lvl_num,
                    waste_kg=float(row.waste_kg),
                    requirement_value=req_val,
                    completed=row.completed,
                    completed_at=row.completed_at,
                    reward_amount=reward
                ))
            else:
                # Default fallback details for personal levels without database rows yet
                responses.append(PersonalLevelProgressResponse(
                    level_number=lvl_num,
                    waste_kg=0.0,
                    requirement_value=req_val,
                    completed=False,
                    completed_at=None,
                    reward_amount=reward
                ))

        return responses
