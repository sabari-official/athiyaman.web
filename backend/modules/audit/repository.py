from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import AuditLog

class AuditRepository(BaseRepository[AuditLog]):
    """
    AuditRepository implements database query patterns for
    immutable security and operational audit logs.
    """
    def __init__(self, db: Session):
        super().__init__(AuditLog, db)

    def search_audit_logs(
        self,
        skip: int = 0,
        limit: int = 50,
        action: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> List[AuditLog]:
        """Queries paginated, filtered audit logs ordered chronologically by created_at."""
        query = self.db.query(self.model)
        if action:
            query = query.filter(self.model.action == action)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.created_at.desc(), self.model.id.desc()).offset(skip).limit(limit).all()

    def search_audit_logs_count(
        self,
        action: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> int:
        """Queries the total count of filtered audit logs in the system."""
        query = self.db.query(self.model)
        if action:
            query = query.filter(self.model.action == action)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.count()
