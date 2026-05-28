from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.notifications.schema import (
    AnnouncementCreateRequest, AnnouncementResponse,
    NotificationCreateRequest, NotificationResponse,
    NotificationLogResponse, NotificationRosterResponse
)
from backend.modules.notifications.service import NotificationService

router = APIRouter(tags=["Notifications"])

# Role guards
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
user_guard = RoleChecker(allowed_roles=["MEMBER", "LEADER", "ADMIN", "DEVELOPER"])

@router.get("/notifications", response_model=NotificationRosterResponse)
def get_personal_notifications(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Fetch paginated lists of delivered notifications for the authenticated citizen.
    Includes full notification titles and messages preloaded from the database.
    """
    user_id = UUID(auth_user.get("sub"))
    service = NotificationService(db)
    result = service.get_notifications(user_id=user_id, page=page, limit=limit)
    return result

@router.put("/notifications/{id}/read", response_model=NotificationLogResponse)
def mark_notification_read(
    id: UUID,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(user_guard)
):
    """
    Marks a delivered notification log as read.
    Validates ownership of the notification trace.
    """
    user_id = UUID(auth_user.get("sub"))
    service = NotificationService(db)
    try:
        log = service.mark_as_read(user_id, id)
        return log
    except ValueError as e:
        err = str(e)
        if err == "NOTIFICATION_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "NOTIFICATION_NOT_FOUND", "message": "The specified notification record was not delivered or does not exist."}
            )
        elif err == "ACCESS_DENIED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "ACCESS_DENIED", "message": "You do not own or have permission to read this notification trace."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "NOTIFICATION_MUTATION_FAILED", "message": err}
        )

@router.post("/admin/announcements", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
def create_announcement(
    payload: AnnouncementCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Creates a new platform announcement.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = NotificationService(db)
    announcement = service.create_announcement(admin_id, payload)
    return announcement

@router.post("/admin/notifications", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def broadcast_notification(
    payload: NotificationCreateRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Broadcasts a targeted role-scoped notification.
    Generates time-ordered notification logs immediately for all target active users.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = NotificationService(db)
    notification = service.broadcast_notification(admin_id, payload)
    return notification
