from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.collection_centers.schema import (
    CenterCreateRequest,
    CenterUpdateRequest,
    CenterResponse,
    CenterRosterResponse,
)
from backend.modules.collection_centers.service import CenterService

router = APIRouter(tags=["Collection Centers"])

# Route Guards: Define RBAC permissions for public and administrative center actions
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
user_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

@router.get("/centers", response_model=CenterRosterResponse)
def search_collection_centers(
    pincode: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Search active collection centers filtered by pincode or district region.
    Exposes map locations and helpline details to all authenticated roles.
    """
    service = CenterService(db)
    result = service.search_centers(pincode=pincode, district=district)
    return result

@router.get("/admin/centers", response_model=CenterRosterResponse)
def get_all_collection_centers(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Fetch paginated lists of all collection centers (active and inactive).
    Restricted strictly to Administrators.
    """
    service = CenterService(db)
    skip = (page - 1) * limit
    if skip < 0:
        skip = 0
    result = service.get_all_centers(skip=skip, limit=limit)
    return result

@router.post("/admin/centers", response_model=CenterResponse, status_code=status.HTTP_201_CREATED)
def register_collection_center(
    payload: CenterCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Register a new localized Collection Center.
    Restricted strictly to Administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = CenterService(db)
    try:
        center = service.create_center(admin_id, payload)
        return center
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "CENTER_NAME_DUPLICATE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "CENTER_NAME_DUPLICATE",
                    "message": "A collection center with this name has already been registered."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "CREATION_FAILED",
                "message": error_msg
            }
        )

@router.put("/admin/centers/{id}", response_model=CenterResponse)
def edit_collection_center(
    id: UUID,
    payload: CenterUpdateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Modify details for a registered collection center.
    Restricted strictly to Administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = CenterService(db)
    try:
        center = service.update_center(admin_id, id, payload)
        return center
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "CENTER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CENTER_NOT_FOUND",
                    "message": "The targeted collection center does not exist."
                }
            )
        elif error_msg == "CENTER_NAME_DUPLICATE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "CENTER_NAME_DUPLICATE",
                    "message": "Another collection center is already registered under this updated name."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "UPDATE_FAILED",
                "message": error_msg
            }
        )

@router.post("/admin/centers/{id}/toggle", response_model=CenterResponse)
def toggle_center_visibility(
    id: UUID,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Toggle the active/inactive status of a collection center.
    Restricted strictly to Administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = CenterService(db)
    try:
        center = service.toggle_center(admin_id, id)
        return center
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "CENTER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CENTER_NOT_FOUND",
                    "message": "The targeted collection center does not exist."
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "TOGGLE_FAILED",
                "message": error_msg
            }
        )
