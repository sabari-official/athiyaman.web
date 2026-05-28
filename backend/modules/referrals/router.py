from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.referrals.schema import ReferralCreateRequest, ReferralResponse
from backend.modules.referrals.service import ReferralService

router = APIRouter(prefix="/referrals", tags=["Referrals"])

# Route Guard: Enforces that caller must hold either ADMIN or LEADER credential roles
referral_guard = RoleChecker(allowed_roles=["ADMIN", "LEADER"])
leader_guard = RoleChecker(allowed_roles=["LEADER"])

@router.post("/", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
def create_referral_code(
    payload: ReferralCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(referral_guard)
):
    """
    Generate a secure random signup invitation code.
    - Admins create single-use LEADER codes.
    - Leaders create Level 1-6 member TEAM codes with slot bounds.
    """
    generator_id = UUID(auth_user.get("sub"))
    service = ReferralService(db)
    try:
        ref_code = service.create_referral(generator_id, payload)
        return ref_code
    except ValueError as e:
        error_msg = str(e)
        
        # Map specific business logic exceptions to HTTP status codes
        if error_msg in {
            "ONLY_ADMINS_CAN_GENERATE_LEADER_CODES",
            "ONLY_LEADERS_CAN_GENERATE_TEAM_CODES"
        }:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "INSUFFICIENT_PERMISSIONS",
                    "message": "You are unauthorized to generate this classification of invitation code."
                }
            )
        elif error_msg == "ACTIVE_REFERRAL_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "ACTIVE_REFERRAL_EXISTS",
                    "message": "Your team already has an active, unexpired invitation code. Expiry or usage limit reached is required to regenerate."
                }
            )
        elif error_msg == "LEVEL_NOT_COMPLETED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "LEVEL_NOT_COMPLETED",
                    "message": "Your team has not completed the prerequisite progress level to recruit for this tier."
                }
            )
        elif error_msg == "TEAM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "TEAM_NOT_FOUND",
                    "message": "No registered team found under this leader account to associate invitation codes."
                }
            )
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "REFERRAL_GENERATION_FAILED",
                "message": error_msg
            }
        )

@router.get("/active", response_model=ReferralResponse)
def get_active_referral_code(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(leader_guard)
):
    """
    Fetch the currently active unexpired member invitation code for the Leader's team.
    """
    leader_id = UUID(auth_user.get("sub"))
    service = ReferralService(db)
    try:
        ref_code = service.get_active_code(leader_id)
        return ref_code
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "NO_ACTIVE_REFERRAL_CODE":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "NO_ACTIVE_REFERRAL_CODE",
                    "message": "Your team has no active invitation code. Please generate a new code to recruit members."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FETCH_FAILED",
                "message": error_msg
            }
        )
