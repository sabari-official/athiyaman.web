from sqlalchemy.orm import Session
from uuid import UUID
import datetime
from typing import Optional, List

from backend.database.models import User, RewardClaim, PaymentTransaction
from backend.modules.payments.repository import PaymentRepository
from backend.modules.payments.schema import PayoutLogRequest

class PaymentService:
    """
    PaymentService coordinates manual payouts, transaction ledgers,
    milestone release locks, and comprehensive payment audit trails.
    """
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)

    def disburse_manual_payout(self, admin_id: UUID, transaction_id: UUID, payload: PayoutLogRequest) -> PaymentTransaction:
        """
        Processes a manual ledger payment disbursement.
        Enforces:
        - Transaction existence check.
        - Already-paid verification block.
        - Atomic status transition to PAID on both transaction and claim records.
        - Milestone unlock (sets is_locked = False).
        - Generates immutable PaymentAuditLog record.
        """
        # 1. Fetch target transaction
        tx = self.payment_repo.get_by_id(transaction_id)
        if not tx:
            raise ValueError("TRANSACTION_NOT_FOUND")

        # 2. Check if already processed
        if tx.status == "PAID":
            raise ValueError("TRANSACTION_ALREADY_PAID")

        old_status = tx.status

        # 3. Update Transaction state
        tx.status = "PAID"
        tx.transaction_reference = payload.transaction_reference
        tx.paid_at = payload.paid_at if payload.paid_at else datetime.datetime.utcnow()

        # 4. Fetch and update the corresponding Claim milestone
        claim = self.db.query(RewardClaim).filter(RewardClaim.id == tx.claim_id).first()
        if claim:
            claim.status = "PAID"
            claim.is_locked = False  # Unlock the milestone progression!

        # 5. Add administrative audit trail record
        self.payment_repo.add_payment_audit_log(
            payment_id=tx.id,
            action="PAYMENT_DISBURSED",
            performer_id=admin_id,
            old_status=old_status,
            new_status="PAID",
            remarks=f"Manual ledger logged with commercial UTR reference: {payload.transaction_reference}."
        )

        self.db.commit()
        self.db.refresh(tx)
        return tx

    def get_payment_logs(
        self,
        user_id: UUID,
        role: str,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        filter_user_id: Optional[UUID] = None
    ) -> dict:
        """
        Fetches paginated, role-bounded lists of payment transactions.
        - Standard citizens strictly retrieve their own records.
        - Admins query global ledgers.
        """
        skip = (page - 1) * limit
        if skip < 0:
            skip = 0

        if role in {"MEMBER", "LEADER"}:
            items = self.payment_repo.get_user_payments(user_id=user_id, skip=skip, limit=limit)
            total = self.payment_repo.get_user_payments_count(user_id=user_id)
        else:
            items = self.payment_repo.get_all_payments(
                skip=skip,
                limit=limit,
                status=status,
                user_id=filter_user_id
            )
            total = self.payment_repo.get_all_payments_count(
                status=status,
                user_id=filter_user_id
            )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }
