from sqlalchemy.orm import Session
from uuid import UUID
import datetime
from typing import Optional, List

from backend.database.models import User, Notification, NotificationLog, Announcement
from backend.modules.notifications.repository import NotificationRepository
from backend.modules.notifications.schema import AnnouncementCreateRequest, NotificationCreateRequest
from backend.utils.uuid import uuidv7

class NotificationService:
    """
    NotificationService coordinates system announcements, targeted broadcast notifications,
    delivered notification triggers, and user read confirmations.
    """
    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(db)

    def create_announcement(self, admin_id: UUID, payload: AnnouncementCreateRequest) -> Announcement:
        """
        Creates a new public platform announcement.
        Restricted to admins.
        """
        announcement = Announcement(
            id=uuidv7(),
            title=payload.title,
            message=payload.message,
            start_date=payload.start_date,
            end_date=payload.end_date,
            created_by=admin_id,
            is_active=True
        )
        self.db.add(announcement)
        self.db.commit()
        self.db.refresh(announcement)
        return announcement

    def broadcast_notification(self, admin_id: UUID, payload: NotificationCreateRequest) -> Notification:
        """
        Broadcasts a new targeted notification.
        Automatically triggers a delivery process in Python, generating
        NotificationLog entries for all active users matching the target role in the same transaction.
        """
        target_role = payload.target_type.upper()

        # 1. Create central Notification record
        notification = Notification(
            id=uuidv7(),
            title=payload.title,
            message=payload.message,
            target_type=target_role,
            created_by=admin_id
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)

        # 2. Query target user audience
        user_query = self.db.query(User).filter(User.user_status == "ACTIVE")
        if target_role != "ALL":
            user_query = user_query.filter(User.role == target_role)
        
        target_users = user_query.all()

        # 3. Bulk insert NotificationLog entries in the same session (Delivered Trigger)
        now = datetime.datetime.utcnow()
        for u in target_users:
            log_entry = NotificationLog(
                id=uuidv7(),
                notification_id=notification.id,
                user_id=u.id,
                delivered=True,
                delivered_at=now,
                is_read=False
            )
            self.db.add(log_entry)

        self.db.commit()
        return notification

    def get_notifications(self, user_id: UUID, page: int = 1, limit: int = 20) -> dict:
        """Fetches paginated personal notification logs delivered to the citizen."""
        skip = (page - 1) * limit
        if skip < 0:
            skip = 0

        items = self.notification_repo.get_user_notification_logs(user_id=user_id, skip=skip, limit=limit)
        total = self.notification_repo.get_user_notification_logs_count(user_id=user_id)

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }

    def mark_as_read(self, user_id: UUID, log_id: UUID) -> NotificationLog:
        """Marks an individual delivered notification log as read by the citizen."""
        log = self.db.query(NotificationLog).filter(NotificationLog.id == log_id).first()
        if not log:
            raise ValueError("NOTIFICATION_NOT_FOUND")
        
        # Security Guard: Citizen can only mutate their own log
        if log.user_id != user_id:
            raise ValueError("ACCESS_DENIED")

        log.is_read = True
        log.read_at = datetime.datetime.utcnow()
        self.db.commit()
        self.db.refresh(log)
        return log
