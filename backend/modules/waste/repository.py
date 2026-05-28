from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import WasteRecord, WasteStatusHistory

class WasteRepository(BaseRepository[WasteRecord]):
    """
    WasteRepository implements SQLAlchemy database access patterns
    for waste collection records and their historical logs.
    """
    def __init__(self, db: Session):
        super().__init__(WasteRecord, db)

    def get_user_records(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[WasteRecord]:
        """Queries paginated collection records logged under a specific citizen ID."""
        return self.db.query(self.model).filter(
            self.model.user_id == user_id
        ).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def get_user_records_count(self, user_id: UUID) -> int:
        """Queries the total count of collection records logged under a specific citizen ID."""
        return self.db.query(self.model).filter(self.model.user_id == user_id).count()

    def get_all_records(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> List[WasteRecord]:
        """
        Queries paginated, filtered waste collection records globally.
        Used primarily for administrative verification queues.
        """
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.verification_status == status)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def get_all_records_count(
        self,
        status: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> int:
        """Queries the total count of filtered waste collection records globally."""
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.verification_status == status)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.count()

    def add_status_history(
        self,
        record_id: UUID,
        status: str,
        comments: str,
        updater_id: Optional[UUID] = None
    ) -> WasteStatusHistory:
        """
        Appends a status transition log to the immutable waste_status_history table.
        This provides a secure administrative audit trail.
        """
        history = WasteStatusHistory(
            waste_record_id=record_id,
            status=status,
            comments=comments,
            updated_by=updater_id
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history
