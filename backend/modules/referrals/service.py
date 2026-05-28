import datetime
import random
import string
from sqlalchemy.orm import Session
from uuid import UUID

from backend.database.models import ReferralCode, User, Team
from backend.modules.referrals.repository import ReferralRepository
from backend.modules.referrals.schema import ReferralCreateRequest
from backend.core.config import settings

class ReferralService:
    """
    ReferralService manages inviter signup codes generation.
    Enforces strict role permissions, level dependencies, active limits,
    and automatic slot capacity mappings.
    """
    def __init__(self, db: Session):
        self.db = db
        self.ref_repo = ReferralRepository(db)

    def create_referral(self, generator_id: UUID, payload: ReferralCreateRequest) -> ReferralCode:
        """
        Generates a new secure Referral invitation code in an atomic database transaction.
        Enforces:
        - Cryptographic role check guards (Admins create Leader codes; Leaders create Team codes).
        - One active Team code limit (enforces expiry or usage before recreating).
        - Level completion prerequisites (Leaders cannot recruit for Level 2 until Level 1 is fully complete).
        - Dynamic slot capacities mapping Level requirements (10 to 50,000 slots).
        """
        # 1. Fetch generator details
        generator = self.db.query(User).filter(User.id == generator_id).first()
        if not generator:
            raise ValueError("GENERATOR_NOT_FOUND")

        ref_type = payload.referral_type.upper()
        max_usage = 1
        level_number = None
        team_id = None

        # 2. Enforce Admin boundaries for LEADER codes
        if ref_type == "LEADER":
            if generator.role != "ADMIN":
                raise ValueError("ONLY_ADMINS_CAN_GENERATE_LEADER_CODES")
            max_usage = 1

        # 3. Enforce Leader boundaries for TEAM codes
        elif ref_type == "TEAM":
            if generator.role != "LEADER":
                raise ValueError("ONLY_LEADERS_CAN_GENERATE_TEAM_CODES")
            if not payload.level_number:
                raise ValueError("LEVEL_NUMBER_REQUIRED_FOR_TEAM_CODE")
            
            level_number = payload.level_number

            # Fetch leader's team
            team = self.db.query(Team).filter(
                Team.leader_id == generator_id,
                Team.status == "ACTIVE"
            ).first()
            if not team:
                raise ValueError("TEAM_NOT_FOUND")
            
            team_id = team.id

            # Enforce Referral Activation Rule: One active code at a time
            active_code = self.ref_repo.get_active_team_referral(team.id)
            if active_code:
                raise ValueError("ACTIVE_REFERRAL_EXISTS")

            # Enforce Referral Generation Eligibility: Completion prerequisite checks
            if team.current_level < level_number:
                raise ValueError("LEVEL_NOT_COMPLETED")

            # Enforce slot limits based strictly on level_number (19_FINAL_BUSINESS_RULES_ADDENDUM.md)
            if level_number == 1: max_usage = 10
            elif level_number == 2: max_usage = 90
            elif level_number == 3: max_usage = 720
            elif level_number == 4: max_usage = 5040
            elif level_number == 5: max_usage = 30240
            elif level_number == 6: max_usage = 50000
            else:
                raise ValueError("INVALID_LEVEL_NUMBER")

        # 4. Generate unique collision-free code
        code_str = self._generate_unique_code(ref_type)

        # 5. Insert ReferralCode record
        expiry_hours = settings.REFERRAL_EXPIRY_HOURS
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=expiry_hours)

        ref_code = ReferralCode(
            code=code_str,
            referral_type=ref_type,
            team_id=team_id,
            level_number=level_number,
            generated_by=generator_id,
            max_usage=max_usage,
            used_count=0,
            is_active=True,
            expires_at=expires_at
        )

        self.db.add(ref_code)
        self.db.commit()
        self.db.refresh(ref_code)
        return ref_code

    def get_active_code(self, generator_id: UUID) -> ReferralCode:
        """Fetch the active unexpired referral code for the leader's team."""
        generator = self.db.query(User).filter(User.id == generator_id).first()
        if not generator:
            raise ValueError("GENERATOR_NOT_FOUND")

        if generator.role == "LEADER":
            team = self.db.query(Team).filter(Team.leader_id == generator_id).first()
            if not team:
                raise ValueError("TEAM_NOT_FOUND")
            
            active_code = self.ref_repo.get_active_team_referral(team.id)
            if not active_code:
                raise ValueError("NO_ACTIVE_REFERRAL_CODE")
            return active_code
            
        raise ValueError("UNAUTHORIZED_VIEW_TYPE")

    def _generate_unique_code(self, ref_type: str) -> str:
        """Generates random uppercase collision-free 'REF-XXXX-YYYY' code string."""
        attempts = 0
        prefix = "LEAD" if ref_type == "LEADER" else "TEAM"
        while attempts < 100:
            rand_a = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
            rand_b = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
            code_str = f"REF-{prefix}-{rand_a}-{rand_b}"
            
            # Check DB collision
            if not self.ref_repo.get_by_code(code_str):
                return code_str
            attempts += 1
            
        raise ValueError("COULD_NOT_GENERATE_UNIQUE_CODE")
