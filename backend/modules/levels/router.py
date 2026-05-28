from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.levels.schema import TeamLevelProgressResponse, PersonalLevelProgressResponse
from backend.modules.levels.service import LevelService

router = APIRouter(prefix="/levels", tags=["Levels"])

# Route Guards: Define RBAC permissions for levels progression endpoints
team_guard = RoleChecker(allowed_roles=["LEADER", "ADMIN"])
personal_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

@router.get("/team", response_model=List[TeamLevelProgressResponse])
def get_team_progression(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(team_guard)
):
    """
    Fetch the progressive Team Levels (1-6) progress tracker.
    Restricted strictly to Leaders or Admins.
    """
    leader_id = UUID(auth_user.get("sub"))
    service = LevelService(db)
    try:
        progress = service.get_team_level_progress(leader_id)
        return progress
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "TEAM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "TEAM_NOT_FOUND",
                    "message": "No active team found under this leader account to compile milestones."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FETCH_FAILED",
                "message": error_msg
            }
        )

@router.get("/personal", response_model=List[PersonalLevelProgressResponse])
def get_personal_progression(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(personal_guard)
):
    """
    Fetch the progressive Personal Levels (7-11) progress tracker.
    Available to all authenticated platform participants.
    """
    user_id = UUID(auth_user.get("sub"))
    service = LevelService(db)
    try:
        progress = service.get_personal_level_progress(user_id)
        return progress
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "USER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_NOT_FOUND",
                    "message": "The requesting user account does not exist."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FETCH_FAILED",
                "message": error_msg
            }
        )
