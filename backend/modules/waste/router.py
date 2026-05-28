from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.waste.schema import WasteCreateRequest, WasteResponse, WasteRosterResponse, AdminVerifyRequest
from backend.modules.waste.service import WasteService

router = APIRouter(tags=["Waste"])

# Route Guards: Define RBAC permissions for waste logging and query actions
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
user_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

@router.post("/waste", response_model=WasteResponse, status_code=status.HTTP_201_CREATED)
def log_waste_record(
    payload: WasteCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Log a new physical waste collection record for a verified citizen.
    This endpoint is restricted strictly to Collection Center Managers/Admins.
    """
    manager_id = UUID(auth_user.get("sub"))
    service = WasteService(db)
    try:
        record = service.log_waste_by_manager(manager_id, payload)
        return record
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "CENTER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CENTER_NOT_FOUND",
                    "message": "The selected collection center does not exist in the platform registry."
                }
            )
        elif error_msg == "CENTER_INACTIVE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "CENTER_INACTIVE",
                    "message": "The selected collection center is currently disabled/inactive."
                }
            )
        elif error_msg == "CITIZEN_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CITIZEN_NOT_FOUND",
                    "message": "No registered citizen account found matching the provided user_id."
                }
            )
        elif error_msg == "CITIZEN_NOT_VERIFIED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "CITIZEN_NOT_VERIFIED",
                    "message": "The citizen must have a 100% complete profile and accept platform click-wrap rules before depositing waste."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "WASTE_LOGGING_FAILED",
                "message": error_msg
            }
        )

@router.get("/waste", response_model=WasteRosterResponse)
def get_waste_history(
    page: int = 1,
    limit: int = 20,
    status_filter: Optional[str] = None,
    filter_user_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Fetch paginated lists of logged waste records.
    - Standard Citizens strictly view their own collection summaries.
    - Admins view global collection registers and can filter by citizen or status.
    """
    user_id = UUID(auth_user.get("sub"))
    role = auth_user.get("role")
    service = WasteService(db)
    
    result = service.get_waste_logs(
        user_id=user_id,
        role=role,
        page=page,
        limit=limit,
        status=status_filter,
        filter_user_id=filter_user_id
    )
    return result

@router.post("/admin/waste/{id}/reject", response_model=WasteResponse)
def reject_waste_record(
    id: UUID,
    payload: AdminVerifyRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Reject a pending waste collection record with comments.
    Restricted strictly to authenticated administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = WasteService(db)
    try:
        record = service.reject_waste(admin_id, id, payload.comments)
        return record
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "RECORD_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "RECORD_NOT_FOUND",
                    "message": "The target waste collection record does not exist."
                }
            )
        elif error_msg == "RECORD_ALREADY_PROCESSED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "RECORD_ALREADY_PROCESSED",
                    "message": "This record has already been audited/processed and cannot be rejected."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "REJECTION_FAILED",
                "message": error_msg
            }
        )
