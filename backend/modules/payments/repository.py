from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import PaymentTransaction, PaymentAuditLog
from backend.utils.uuid import uuidv7

class PaymentRepository(BaseRepository[PaymentTransaction]):
    """
    PaymentRepository implements SQLAlchemy database access patterns
    for payment transactions and their audit trail.
    """
    def __init__(self, db: Session):
        super().__init__(PaymentTransaction, db)

    def get_user_payments(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[PaymentTransaction]:
        """Queries paginated payment transactions matching a specific citizen ID."""
        return self.db.query(self.model).filter(
            self.model.user_id == user_id
        ).order_by(self.model.paid_at.desc(), self.model.id.desc()).offset(skip).limit(limit).all()

    def get_user_payments_count(self, user_id: UUID) -> int:
        """Queries the total count of payment transactions matching a specific citizen ID."""
        return self.db.query(self.model).filter(self.model.user_id == user_id).count()

    def get_all_payments(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> List[PaymentTransaction]:
        """
        Queries paginated global payment transactions.
        Used by administrators to manage disbursements.
        """
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.status == status)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.paid_at.desc(), self.model.id.desc()).offset(skip).limit(limit).all()

    def get_all_payments_count(
        self,
        status: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> int:
        """Queries the total count of global payment transactions."""
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.status == status)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.count()

    def add_payment_audit_log(
        self,
        payment_id: UUID,
        action: str,
        performer_id: UUID,
        old_status: Optional[str],
        new_status: str,
        remarks: Optional[str] = None
    ) -> PaymentAuditLog:
        """Appends a secure record to the payment_audit_logs table."""
        audit = PaymentAuditLog(
            id=uuidv7(),
            payment_id=payment_id,
            action=action,
            performed_by=performer_id,
            old_status=old_status,
            new_status=new_status,
            remarks=remarks
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)
        return audit
