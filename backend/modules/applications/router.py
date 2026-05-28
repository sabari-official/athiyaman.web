from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.applications.schema import (
    LeaderApplicationRequest, MemberApplicationRequest, ApplicationResponse, ApplicationApproveRequest
)
from backend.modules.applications.service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])
leader_guard = RoleChecker(allowed_roles=["LEADER"])

@router.post("/leader", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def submit_leader_application(payload: LeaderApplicationRequest, db: Session = Depends(get_db)):
    """Public endpoint to submit a Leader Application."""
    service = ApplicationService(db)
    try:
        app = service.submit_leader_application(payload)
        return app
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "APPLICATION_FAILED", "message": str(e)}
        )

@router.post("/member", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def submit_member_application(payload: MemberApplicationRequest, db: Session = Depends(get_db)):
    """Public endpoint to submit a Member Application."""
    service = ApplicationService(db)
    try:
        app = service.submit_member_application(payload)
        return app
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "APPLICATION_FAILED", "message": str(e)}
        )

@router.post("/member/{app_id}/review", response_model=ApplicationResponse)
def review_member_application(
    app_id: UUID,
    payload: ApplicationApproveRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(leader_guard)
):
    """Authenticated endpoint for Leaders to review Member Applications assigned to their team."""
    service = ApplicationService(db)
    try:
        leader_id = UUID(auth_user.get("sub"))
        app = service.approve_member_application(app_id, leader_id, payload.status)
        return app
    except ValueError as e:
        status_code = status.HTTP_403_FORBIDDEN if e.args[0] in ["UNAUTHORIZED", "UNAUTHORIZED_TEAM"] else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code,
            detail={"code": "REVIEW_FAILED", "message": str(e)}
        )
