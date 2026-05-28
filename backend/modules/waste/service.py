from sqlalchemy.orm import Session
from uuid import UUID
import datetime
from typing import Optional

from backend.database.models import User, CollectionCenter, WasteRecord
from backend.modules.waste.repository import WasteRepository
from backend.modules.waste.schema import WasteCreateRequest

class WasteService:
    """
    WasteService implements all business rules and progression constraints
    for waste collections, executing double-commits to trigger database milestone
    checks cleanly.
    """
    def __init__(self, db: Session):
        self.db = db
        self.waste_repo = WasteRepository(db)

    def log_waste_by_manager(self, manager_id: UUID, payload: WasteCreateRequest) -> WasteRecord:
        """
        Logs a new physical waste collection record for a citizen.
        Only called by authorized Waste Managers/Admins.
        Enforces:
        - Active collection center check.
        - Citizen existence and rules acceptance verification checks.
        - Weight constraints (0.1 - 50.0 KG).
        - Double-commit (Insert PENDING -> Update APPROVED) to ensure the
          PostgreSQL progression triggers fire successfully.
        """
        # 1. Verify that collection center exists and is active
        center = self.db.query(CollectionCenter).filter(
            CollectionCenter.id == payload.center_id
        ).first()
        if not center:
            raise ValueError("CENTER_NOT_FOUND")
        if not center.is_active:
            raise ValueError("CENTER_INACTIVE")

        # 2. Verify target citizen exists and is verified (has accepted click-wrap rules)
        citizen = self.db.query(User).filter(User.id == payload.user_id).first()
        if not citizen:
            raise ValueError("CITIZEN_NOT_FOUND")
        if not citizen.is_verified:
            raise ValueError("CITIZEN_NOT_VERIFIED")

        # 3. Create WasteRecord in PENDING state (Step 1 of trigger lifecycle)
        record = WasteRecord(
            user_id=payload.user_id,
            center_id=payload.center_id,
            weight_kg=payload.weight_kg,
            image_path=payload.image_path,
            collection_date=payload.collection_date,
            location=payload.location,
            verification_status="PENDING",
            payment_status="PENDING",
            amount_paid=0.0
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        # 4. Transition status to APPROVED immediately (Step 2 of trigger lifecycle)
        # This update triggers the PostgreSQL trg_personal_level_completion level calculations!
        record.verification_status = "APPROVED"
        record.verified_by = manager_id
        record.verified_at = datetime.datetime.utcnow()
        self.db.commit()
        self.db.refresh(record)

        # 5. Append transition audit history log
        self.waste_repo.add_status_history(
            record_id=record.id,
            status="APPROVED",
            comments=f"Waste collection logged and automatically verified by Waste Manager. Desk/Counter: {payload.location or 'Default'}",
            updater_id=manager_id
        )

        return record

    def get_waste_logs(
        self,
        user_id: UUID,
        role: str,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        filter_user_id: Optional[UUID] = None
    ) -> dict:
        """
        Fetches paginated, role-bounded lists of logged waste collections.
        - Standard Citizens strictly retrieve their own records.
        - Admins retrieve global records and can filter by citizen ID or status.
        """
        skip = (page - 1) * limit
        if skip < 0:
            skip = 0

        # Enforce Citizen security boundaries
        if role in {"MEMBER", "LEADER"}:
            items = self.waste_repo.get_user_records(user_id=user_id, skip=skip, limit=limit)
            total = self.waste_repo.get_user_records_count(user_id=user_id)
        else:
            # Admins or Developers see global records
            items = self.waste_repo.get_all_records(
                skip=skip,
                limit=limit,
                status=status,
                user_id=filter_user_id
            )
            total = self.waste_repo.get_all_records_count(
                status=status,
                user_id=filter_user_id
            )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }

    def reject_waste(self, admin_id: UUID, record_id: UUID, comments: str) -> WasteRecord:
        """
        Manually rejects a pending waste record.
        Restricted strictly to administrators.
        """
        record = self.waste_repo.get_by_id(record_id)
        if not record:
            raise ValueError("RECORD_NOT_FOUND")
        if record.verification_status != "PENDING":
            raise ValueError("RECORD_ALREADY_PROCESSED")

        record.verification_status = "REJECTED"
        record.verified_by = admin_id
        record.verified_at = datetime.datetime.utcnow()
        record.rejection_reason = comments
        self.db.commit()
        self.db.refresh(record)

        self.waste_repo.add_status_history(
            record_id=record.id,
            status="REJECTED",
            comments=comments,
            updater_id=admin_id
        )

        return record
