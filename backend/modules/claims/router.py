from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.claims.schema import ClaimCreateRequest, ClaimResponse, ClaimRosterResponse
from backend.modules.claims.service import ClaimService
from backend.modules.waste.schema import AdminVerifyRequest  # Re-use AdminVerifyRequest for comments

router = APIRouter(tags=["Claims"])

# Role guards
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
user_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

def map_claim_to_response(claim) -> dict:
    """Helper to cleanly serialize DB RewardClaim model into the API schema shape."""
    return {
        "claim_id": claim.id,
        "user_id": claim.user_id,
        "claim_type": claim.claim_type,
        "level_number": claim.level_number,
        "amount": float(claim.amount),
        "status": claim.status,
        "is_locked": claim.is_locked,
        "reviewed_by": claim.reviewed_by,
        "reviewed_at": claim.reviewed_at,
        "rejection_reason": claim.rejection_reason,
        "requested_at": claim.requested_at
    }

@router.post("/rewards/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def create_claim(
    payload: ClaimCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Submits a new milestone reward claim request.
    Validates rules acceptance, 100% profile completion, bank verification,
    no other active claims, and verified completion of milestone level.
    """
    user_id = UUID(auth_user.get("sub"))
    service = ClaimService(db)
    try:
        claim = service.submit_claim(user_id, payload)
        return map_claim_to_response(claim)
    except ValueError as e:
        err = str(e)
        if err == "PROFILE_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "PROFILE_NOT_FOUND", "message": "No profile matches your user account."}
            )
        elif err == "PROFILE_INCOMPLETE":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "PROFILE_INCOMPLETE", "message": "You must complete your profile to 100% before claiming milestones."}
            )
        elif err == "RULES_NOT_ACCEPTED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "RULES_NOT_ACCEPTED", "message": "You must read and accept the platform rules click-wrap agreements."}
            )
        elif err == "BANK_NOT_VERIFIED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "BANK_NOT_VERIFIED", "message": "Your banking details must be verified by an administrator before processing disbursements."}
            )
        elif err == "LEVEL_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "LEVEL_NOT_FOUND", "message": "The specified milestone level does not exist in rules configuration."}
            )
        elif err == "INVALID_LEVEL_FOR_TEAM_CLAIM":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_LEVEL_FOR_TEAM_CLAIM", "message": "Team claims are restricted strictly to levels 1 through 6."}
            )
        elif err == "NOT_TEAM_LEADER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "NOT_TEAM_LEADER", "message": "Only designated Team Leaders can submit team level claims."}
            )
        elif err == "MILESTONE_INCOMPLETE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "MILESTONE_INCOMPLETE", "message": "You have not completed the required level milestone."}
            )
        elif err == "INVALID_LEVEL_FOR_PERSONAL_CLAIM":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_LEVEL_FOR_PERSONAL_CLAIM", "message": "Personal claims are restricted strictly to levels 7 through 11."}
            )
        elif err == "PENDING_CLAIM_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "PENDING_CLAIM_EXISTS", "message": "You already have another claim in PENDING status. Multiple simultaneous active claims are blocked."}
            )
        elif err == "CLAIM_ALREADY_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "CLAIM_ALREADY_EXISTS", "message": "A claim has already been submitted or processed for this specific milestone level."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "CLAIM_SUBMISSION_FAILED", "message": err}
        )

@router.get("/rewards/claims", response_model=ClaimRosterResponse)
def get_personal_claims(
    page: int = 1,
    limit: int = 20,
    status_filter: Optional[str] = None,
    claim_type: Optional[str] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Fetch paginated lists of reward claims.
    - Standard citizens strictly query their own submitted claims.
    - Admins query the global claims registry.
    """
    user_id = UUID(auth_user.get("sub"))
    role = auth_user.get("role")
    service = ClaimService(db)
    
    result = service.get_claims(
        user_id=user_id,
        role=role,
        page=page,
        limit=limit,
        status=status_filter,
        claim_type=claim_type
    )
    return {
        "items": [map_claim_to_response(c) for c in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"]
    }

@router.get("/admin/claims", response_model=ClaimRosterResponse)
def get_admin_claims(
    page: int = 1,
    limit: int = 20,
    status_filter: Optional[str] = None,
    claim_type: Optional[str] = None,
    filter_user_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Exposes paginated global lists of reward claims for administrative audits.
    Restricted strictly to administrators.
    """
    user_id = UUID(auth_user.get("sub"))
    role = auth_user.get("role")
    service = ClaimService(db)
    
    result = service.get_claims(
        user_id=user_id,
        role=role,
        page=page,
        limit=limit,
        status=status_filter,
        claim_type=claim_type,
        filter_user_id=filter_user_id
    )
    return {
        "items": [map_claim_to_response(c) for c in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"]
    }

@router.post("/admin/claims/{id}/approve", response_model=ClaimResponse)
def approve_reward_claim(
    id: UUID,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Approves a pending claim and instantiates a corresponding PaymentTransaction registry entry.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = ClaimService(db)
    try:
        claim = service.approve_claim(admin_id, id)
        return map_claim_to_response(claim)
    except ValueError as e:
        err = str(e)
        if err == "CLAIM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "CLAIM_NOT_FOUND", "message": "The specified claim record does not exist."}
            )
        elif err == "CLAIM_ALREADY_PROCESSED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "CLAIM_ALREADY_PROCESSED", "message": "This claim has already been approved or rejected."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "CLAIM_APPROVAL_FAILED", "message": err}
        )

@router.post("/admin/claims/{id}/reject", response_model=ClaimResponse)
def reject_reward_claim(
    id: UUID,
    payload: AdminVerifyRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Rejects a pending claim and unlocks it to allow correction.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = ClaimService(db)
    try:
        claim = service.reject_claim(admin_id, id, payload.comments)
        return map_claim_to_response(claim)
    except ValueError as e:
        err = str(e)
        if err == "CLAIM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "CLAIM_NOT_FOUND", "message": "The specified claim record does not exist."}
            )
        elif err == "CLAIM_ALREADY_PROCESSED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "CLAIM_ALREADY_PROCESSED", "message": "This claim has already been approved or rejected."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "CLAIM_REJECTION_FAILED", "message": err}
        )
