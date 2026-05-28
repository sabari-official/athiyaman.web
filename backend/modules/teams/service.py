import random
import string
from sqlalchemy.orm import Session
from uuid import UUID

from backend.database.models import Team, User, TeamMember, UserProfile
from backend.modules.teams.repository import TeamRepository
from backend.modules.teams.schema import TeamCreateRequest

class TeamService:
    """
    TeamService coordinates all Team boundaries including One-Leader-One-Team rules,
    random code collisions, and team member roster mapping.
    """
    def __init__(self, db: Session):
        self.db = db
        self.team_repo = TeamRepository(db)

    def create_team(self, leader_id: UUID, payload: TeamCreateRequest) -> Team:
        """
        Creates a new local Team in an atomic database transaction.
        Enforces:
        - Authenticated user role strictly matches LEADER.
        - One Leader, One Team rule (no leader can own multiple teams).
        - Unique Team name across the platform.
        - Dynamic 8-character unique alphanumeric team_code (collison-proof retry loop).
        """
        # 1. Verify user role is strictly LEADER
        leader = self.db.query(User).filter(User.id == leader_id).first()
        if not leader or leader.role != "LEADER":
            raise ValueError("USER_NOT_A_LEADER")

        # 2. Enforce One Leader, One Team rule
        existing_leader_team = self.team_repo.get_by_leader_id(leader_id)
        if existing_leader_team:
            raise ValueError("LEADER_ALREADY_HAS_TEAM")

        # 3. Enforce Unique Team Name and City
        existing_name_team = self.team_repo.get_by_name(payload.team_name)
        if existing_name_team:
            raise ValueError("TEAM_NAME_TAKEN")

        existing_city_team = self.db.query(Team).filter(Team.city == payload.city).first()
        if existing_city_team:
            raise ValueError("CITY_TAKEN")

        # 4. Generate unique, collision-proof 8-character alphanumeric team_code
        team_code = self._generate_unique_team_code()

        # 5. Insert Team record
        team = Team(
            team_code=team_code,
            team_name=payload.team_name,
            leader_id=leader_id,
            state=payload.state,
            district=payload.district,
            pincode=payload.pincode,
            door_no=payload.door_no,
            street_name=payload.street_name,
            landmark=payload.landmark,
            post_office=payload.post_office,
            city=payload.city,
            member_count=0,
            current_level=1,
            status="ACTIVE"
        )
        
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def get_team_by_leader(self, leader_id: UUID) -> Team:
        """Fetch team owned by the leader."""
        team = self.team_repo.get_by_leader_id(leader_id)
        if not team:
            raise ValueError("TEAM_NOT_FOUND")
        return team

    def get_team_roster(self, leader_id: UUID) -> dict:
        """
        Fetches the complete member list linked to the leader's team.
        Returns aggregated usernames, phones, and join timestamps.
        """
        team = self.get_team_by_leader(leader_id)

        # Joint query: Fetch all team members with user and profile details
        roster_items = self.db.query(
            User.id,
            User.username,
            User.phone_number,
            TeamMember.joined_at
        ).join(
            TeamMember, User.id == TeamMember.member_id
        ).filter(
            TeamMember.team_id == team.id
        ).order_by(
            TeamMember.joined_at.desc()
        ).all()

        # Get leader profile details
        leader_profile = self.db.query(UserProfile).filter(UserProfile.user_id == leader_id).first()
        leader_name = leader_profile.full_name if leader_profile else "Leader"

        members = []
        for item in roster_items:
            members.append({
                "id": item.id,
                "username": item.username,
                "phone_number": item.phone_number,
                "joined_at": item.joined_at
            })

        return {
            "team_id": team.id,
            "team_name": team.team_name,
            "leader_name": leader_name,
            "members": members
        }

    def _generate_unique_team_code(self) -> str:
        """Generates a random collision-free 'ATH-XXXX' upper-case alphanumeric identifier."""
        attempts = 0
        while attempts < 100:
            random_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
            team_code = f"ATH-{random_key}"
            
            # Check DB collision
            if not self.team_repo.get_by_code(team_code):
                return team_code
            attempts += 1
            
        raise ValueError("COULD_NOT_GENERATE_UNIQUE_CODE")
