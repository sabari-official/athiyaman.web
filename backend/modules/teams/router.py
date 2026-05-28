from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.teams.schema import TeamCreateRequest, TeamResponse, TeamRosterResponse
from backend.modules.teams.service import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])

# Route Guard: Enforces that caller must hold a validated LEADER credential role
leader_guard = RoleChecker(allowed_roles=["LEADER"])

@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    payload: TeamCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(leader_guard)
):
    """
    Onboard/Register a new localized Team.
    This endpoint is restricted strictly to authenticated Team Leaders.
    """
    leader_id = UUID(auth_user.get("sub"))
    service = TeamService(db)
    try:
        team = service.create_team(leader_id, payload)
        return team
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "USER_NOT_A_LEADER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "USER_NOT_A_LEADER",
                    "message": "Only verified leaders can register teams."
                }
            )
        elif error_msg == "LEADER_ALREADY_HAS_TEAM":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "LEADER_ALREADY_HAS_TEAM",
                    "message": "You are already leading an active team. Leadership is limited to one team."
                }
            )
        elif error_msg == "TEAM_NAME_TAKEN":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "TEAM_NAME_TAKEN",
                    "message": "The team name entered has already been taken. Please choose another unique name."
                }
            )
        elif error_msg == "CITY_TAKEN":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "CITY_TAKEN",
                    "message": "A team already exists in this city. Only one team per city is allowed."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "TEAM_CREATION_FAILED",
                "message": error_msg
            }
        )

@router.get("/my-team", response_model=TeamResponse)
def get_my_team(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(leader_guard)
):
    """
    Fetch the complete team profile details owned by the authenticated Leader.
    """
    leader_id = UUID(auth_user.get("sub"))
    service = TeamService(db)
    try:
        team = service.get_team_by_leader(leader_id)
        return team
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "TEAM_NOT_FOUND",
                "message": "You have not registered a team under this leader account."
            }
        )

@router.get("/my-team/roster", response_model=TeamRosterResponse)
def get_my_team_roster(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(leader_guard)
):
    """
    Fetch the complete active member list recruited under the Leader's team.
    """
    leader_id = UUID(auth_user.get("sub"))
    service = TeamService(db)
    try:
        roster = service.get_team_roster(leader_id)
        return roster
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "TEAM_NOT_FOUND",
                "message": "No active team found to compile member rosters."
            }
        )
