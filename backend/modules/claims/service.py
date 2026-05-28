from sqlalchemy.orm import Session
from uuid import UUID
import datetime
from typing import Optional, List

from backend.database.models import User, UserProfile, RulesAcceptance, Team, TeamLevelProgress, PersonalLevelProgress, Level, RewardClaim, PaymentTransaction
from backend.modules.claims.repository import ClaimRepository
from backend.modules.claims.schema import ClaimCreateRequest

# Import uuidv7 typo-safely
from backend.utils.uuid import uuidv7

class ClaimService:
    """
    ClaimService manages all business rules, checks, sequential milestone requirements,
    and review transitions for reward claims.
    """
    def __init__(self, db: Session):
        self.db = db
        self.claim_repo = ClaimRepository(db)

    def submit_claim(self, user_id: UUID, payload: ClaimCreateRequest) -> RewardClaim:
        """
        Submits a new reward milestone claim for a citizen.
        Enforces:
        - Citizen profile is 100% complete.
        - Click-wrap terms and conditions are accepted.
        - Bank details are verified.
        - No active claims are in PENDING state globally for this user.
        - Unique constraint check for exact level & type.
        - Target milestone level exists and is completed.
        - Lock progress weights (setting is_locked = True).
        """
        # 1. Fetch user profile
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise ValueError("PROFILE_NOT_FOUND")

        # 2. Check profile completion
        if profile.profile_completion != 100:
            raise ValueError("PROFILE_INCOMPLETE")

        # 3. Check rules acceptance
        rules = self.db.query(RulesAcceptance).filter(RulesAcceptance.user_id == user_id).first()
        if not rules:
            raise ValueError("RULES_NOT_ACCEPTED")

        # 4. Check bank verification
        if not profile.bank_verified:
            raise ValueError("BANK_NOT_VERIFIED")

        # Normalize claim type input
        input_type = payload.claim_type.upper()
        if input_type in {"PERSONAL", "PERSONAL_REWARD"}:
            db_claim_type = "PERSONAL"
        elif input_type in {"TEAM", "TEAM_REWARD"}:
            db_claim_type = "TEAM"
        else:
            raise ValueError("INVALID_CLAIM_TYPE")

        level_num = payload.level_number

        # 5. Retrieve Level Master rule configuration
        level_master = self.db.query(Level).filter(Level.level_number == level_num).first()
        if not level_master:
            raise ValueError("LEVEL_NOT_FOUND")

        # 6. Enforce role-based milestone level boundaries
        if db_claim_type == "TEAM":
            if not (1 <= level_num <= 6):
                raise ValueError("INVALID_LEVEL_FOR_TEAM_CLAIM")
            
            # Verify user leads a team
            team = self.db.query(Team).filter(
                Team.leader_id == user_id,
                Team.status == "ACTIVE"
            ).first()
            if not team:
                raise ValueError("NOT_TEAM_LEADER")

            # Check if milestone completed
            progress = self.db.query(TeamLevelProgress).filter(
                TeamLevelProgress.team_id == team.id,
                TeamLevelProgress.level_number == level_num
            ).first()
            if not progress or not progress.completed:
                raise ValueError("MILESTONE_INCOMPLETE")

        else: # PERSONAL
            if not (7 <= level_num <= 11):
                raise ValueError("INVALID_LEVEL_FOR_PERSONAL_CLAIM")

            # Check if milestone completed
            progress = self.db.query(PersonalLevelProgress).filter(
                PersonalLevelProgress.user_id == user_id,
                PersonalLevelProgress.level_number == level_num
            ).first()
            if not progress or not progress.completed:
                raise ValueError("MILESTONE_INCOMPLETE")

        # 7. Check if any claim in PENDING state exists globally for the user
        pending_exists = self.db.query(RewardClaim).filter(
            RewardClaim.user_id == user_id,
            RewardClaim.status == "PENDING"
        ).first()
        if pending_exists:
            raise ValueError("PENDING_CLAIM_EXISTS")

        # 8. Check for duplicate claims for this specific level (unique constraint guard)
        duplicate = self.db.query(RewardClaim).filter(
            RewardClaim.user_id == user_id,
            RewardClaim.level_number == level_num,
            RewardClaim.claim_type == db_claim_type
        ).first()
        if duplicate:
            raise ValueError("CLAIM_ALREADY_EXISTS")

        # 9. All validations passed, create the Claim
        claim = RewardClaim(
            id=uuidv7(),
            user_id=user_id,
            claim_type=db_claim_type,
            level_number=level_num,
            amount=level_master.reward_amount,
            status="PENDING",
            is_locked=True
        )
        self.db.add(claim)
        self.db.commit()
        self.db.refresh(claim)
        return claim

    def get_claims(
        self,
        user_id: UUID,
        role: str,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        claim_type: Optional[str] = None,
        filter_user_id: Optional[UUID] = None
    ) -> dict:
        """
        Fetches paginated, role-bounded lists of reward claims.
        - Standard citizens view their own claims.
        - Admins view global claims queues.
        """
        skip = (page - 1) * limit
        if skip < 0:
            skip = 0

        if role in {"MEMBER", "LEADER"}:
            items = self.claim_repo.get_user_claims(user_id=user_id, skip=skip, limit=limit)
            total = self.claim_repo.get_user_claims_count(user_id=user_id)
        else:
            items = self.claim_repo.get_all_claims(
                skip=skip,
                limit=limit,
                status=status,
                claim_type=claim_type,
                user_id=filter_user_id
            )
            total = self.claim_repo.get_all_claims_count(
                status=status,
                claim_type=claim_type,
                user_id=filter_user_id
            )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }

    def approve_claim(self, admin_id: UUID, claim_id: UUID) -> RewardClaim:
        """
        Approves a pending claim.
        Generates the corresponding PaymentTransaction record in PENDING state.
        Restricted to admins.
        """
        claim = self.claim_repo.get_by_id(claim_id)
        if not claim:
            raise ValueError("CLAIM_NOT_FOUND")
        if claim.status != "PENDING":
            raise ValueError("CLAIM_ALREADY_PROCESSED")

        # 1. Update Claim Status
        claim.status = "APPROVED"
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.datetime.utcnow()

        # 2. Instantiate PaymentTransaction
        tx = PaymentTransaction(
            id=uuidv7(),
            claim_id=claim.id,
            user_id=claim.user_id,
            amount=claim.amount,
            status="PENDING"
        )
        self.db.add(tx)

        self.db.commit()
        self.db.refresh(claim)
        return claim

    def reject_claim(self, admin_id: UUID, claim_id: UUID, reason: str) -> RewardClaim:
        """
        Rejects a pending claim.
        Unlocks is_locked to allow citizen correction/re-submitting.
        Restricted to admins.
        """
        claim = self.claim_repo.get_by_id(claim_id)
        if not claim:
            raise ValueError("CLAIM_NOT_FOUND")
        if claim.status != "PENDING":
            raise ValueError("CLAIM_ALREADY_PROCESSED")

        claim.status = "REJECTED"
        claim.reviewed_by = admin_id
        claim.reviewed_at = datetime.datetime.utcnow()
        claim.rejection_reason = reason
        claim.is_locked = False  # Unlock

        self.db.commit()
        self.db.refresh(claim)
        return claim
