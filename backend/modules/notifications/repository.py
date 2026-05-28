from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import Notification, NotificationLog

class NotificationRepository(BaseRepository[Notification]):
    """
    NotificationRepository implements database access layers for
    broadcast notifications and user-specific logs.
    """
    def __init__(self, db: Session):
        super().__init__(Notification, db)

    def get_user_notification_logs(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[NotificationLog]:
        """Queries paginated notification logs delivered to a specific user, preloading notification metadata."""
        return self.db.query(NotificationLog).filter(
            NotificationLog.user_id == user_id
        ).options(
            joinedload(NotificationLog.notification)
        ).order_by(
            NotificationLog.delivered_at.desc(), NotificationLog.id.desc()
        ).offset(skip).limit(limit).all()

    def get_user_notification_logs_count(self, user_id: UUID) -> int:
        """Queries the total count of notifications delivered to a specific user."""
        return self.db.query(NotificationLog).filter(NotificationLog.user_id == user_id).count()
