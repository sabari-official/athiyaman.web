from sqlalchemy.orm import Session
from uuid import UUID
import datetime

from backend.database.models import LeaderApplication, MemberApplication, Team, User
from backend.modules.applications.schema import LeaderApplicationRequest, MemberApplicationRequest
from backend.utils.security import aadhaar_security
from backend.utils.verhoeff import validate_aadhaar

class ApplicationService:
    def __init__(self, db: Session):
        self.db = db

    def submit_leader_application(self, payload: LeaderApplicationRequest) -> LeaderApplication:
        if not validate_aadhaar(payload.aadhaar):
            raise ValueError("INVALID_AADHAAR")

        # 1. Enforce City Uniqueness Check: Is there already a team or approved leader in this city?
        existing_team = self.db.query(Team).filter(Team.city == payload.city).first()
        if existing_team:
            raise ValueError("CITY_ALREADY_TAKEN")
            
        existing_leader_app = self.db.query(LeaderApplication).filter(
            LeaderApplication.city == payload.city,
            LeaderApplication.status.in_(["PENDING", "APPROVED"])
        ).first()
        if existing_leader_app:
            raise ValueError("CITY_ALREADY_HAS_LEADER_APP")

        # Process Aadhaar
        masked = "XXXX-XXXX-" + payload.aadhaar[-4:]
        aadhaar_hash = aadhaar_security.generate_sha256_hash(payload.aadhaar)

        # Ensure aadhaar is unique
        if self.db.query(LeaderApplication).filter(LeaderApplication.aadhaar_hash == aadhaar_hash).first():
            raise ValueError("AADHAAR_ALREADY_USED")

        app = LeaderApplication(
            full_name=payload.full_name,
            phone=payload.phone,
            email=payload.email,
            masked_aadhaar=masked,
            aadhaar_hash=aadhaar_hash,
            state=payload.state,
            district=payload.district,
            pincode=payload.pincode,
            door_no=payload.door_no,
            street_name=payload.street_name,
            landmark=payload.landmark,
            post_office=payload.post_office,
            city=payload.city,
            reason=payload.reason
        )
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def submit_member_application(self, payload: MemberApplicationRequest) -> MemberApplication:
        if not validate_aadhaar(payload.aadhaar):
            raise ValueError("INVALID_AADHAAR")

        # 1. Find the target Team for this city
        target_team = self.db.query(Team).filter(
            Team.city == payload.city,
            Team.status == "ACTIVE"
        ).first()
        
        if not target_team:
            raise ValueError("NO_ACTIVE_TEAM_IN_CITY")

        # Process Aadhaar
        masked = "XXXX-XXXX-" + payload.aadhaar[-4:]
        aadhaar_hash = aadhaar_security.generate_sha256_hash(payload.aadhaar)

        # Ensure aadhaar is unique
        if self.db.query(MemberApplication).filter(MemberApplication.aadhaar_hash == aadhaar_hash).first():
            raise ValueError("AADHAAR_ALREADY_USED")

        app = MemberApplication(
            full_name=payload.full_name,
            phone=payload.phone,
            email=payload.email,
            masked_aadhaar=masked,
            aadhaar_hash=aadhaar_hash,
            state=payload.state,
            district=payload.district,
            pincode=payload.pincode,
            door_no=payload.door_no,
            street_name=payload.street_name,
            landmark=payload.landmark,
            post_office=payload.post_office,
            city=payload.city,
            assigned_team_id=target_team.id
        )
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def approve_member_application(self, app_id: UUID, leader_id: UUID, status: str):
        app = self.db.query(MemberApplication).filter(MemberApplication.id == app_id).first()
        if not app:
            raise ValueError("APPLICATION_NOT_FOUND")
            
        leader = self.db.query(User).filter(User.id == leader_id).first()
        if not leader or leader.role != "LEADER":
            raise ValueError("UNAUTHORIZED")

        # Ensure the leader owns the team this application is assigned to
        team = self.db.query(Team).filter(Team.id == app.assigned_team_id).first()
        if not team or team.leader_id != leader_id:
            raise ValueError("UNAUTHORIZED_TEAM")

        if status not in ["APPROVED", "REJECTED"]:
            raise ValueError("INVALID_STATUS")

        app.status = status
        app.reviewed_by = leader_id
        app.reviewed_at = datetime.datetime.utcnow()
        self.db.commit()
        return app
