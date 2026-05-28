from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.profiles.schema import ProfileUpdateRequest, ProfileResponse, RulesAcceptanceRequest
from backend.modules.profiles.service import ProfileService

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Route Guard: Enforces that caller must be a registered Citizen/Member/Leader/Admin
citizen_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(citizen_guard)
):
    """
    Retrieve the current authenticated user's profile details.
    """
    user_id = UUID(auth_user.get("sub"))
    service = ProfileService(db)
    profile = service.get_profile(user_id)
    return profile

@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(citizen_guard)
):
    """
    Update personal biographical, geocoded address, encrypted bank routing,
    and nominee configurations on the authenticated user's profile.
    """
    user_id = UUID(auth_user.get("sub"))
    service = ProfileService(db)
    try:
        profile = service.update_profile(user_id, payload)
        return profile
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "AADHAAR_ALREADY_USED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "AADHAAR_ALREADY_USED",
                    "message": "The Aadhaar number entered is already registered under another account."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "PROFILE_UPDATE_FAILED",
                "message": error_msg
            }
        )

@router.post("/me/accept-rules", status_code=status.HTTP_200_OK)
def accept_rules(
    payload: RulesAcceptanceRequest,
    request: Request,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(citizen_guard)
):
    """
    Accept the platform click-wrap legal rules version.
    This action requires that the profile is exactly 100% complete.
    """
    user_id = UUID(auth_user.get("sub"))
    service = ProfileService(db)
    
    # Extract client IP address for audit logs
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    try:
        service.accept_platform_rules(user_id, payload.rules_version, client_ip)
        return {
            "status": "success",
            "message": "Platform click-wrap legal rules accepted successfully. Dashboard unlocked."
        }
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "PROFILE_INCOMPLETE_RULES":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "PROFILE_INCOMPLETE",
                    "message": "You cannot accept platform rules until your profile completion progress is exactly 100%."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "RULES_ACCEPTANCE_FAILED",
                "message": error_msg
            }
        )
