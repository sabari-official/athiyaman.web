from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List, Any

from backend.database.models import AuditLog
from backend.modules.audit.repository import AuditRepository
from backend.utils.uuid import uuidv7

class AuditService:
    """
    AuditService coordinates permanent transaction tracking,
    asynchronous mutation logs logging, and admin explorer views.
    """
    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditRepository(db)

    def log_system_action(
        self,
        user_id: Optional[UUID],
        role: Optional[str],
        action: str,
        entity_type: str,
        entity_id: Optional[UUID] = None,
        old_values: Optional[Any] = None,
        new_values: Optional[Any] = None,
        ip_address: Optional[str] = None,
        device: Optional[str] = None
    ) -> AuditLog:
        """
        Permanently registers a database mutating action to the immutable audit_logs trail.
        This provides absolute compliance, audit support, and transaction tracing.
        """
        log = AuditLog(
            id=uuidv7(),
            user_id=user_id,
            role=role,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            device=device
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_audit_logs(
        self,
        page: int = 1,
        limit: int = 50,
        action: Optional[str] = None,
        filter_user_id: Optional[UUID] = None
    ) -> dict:
        """Fetches paginated global audit logs for administrative explorers."""
        skip = (page - 1) * limit
        if skip < 0:
            skip = 0

        items = self.audit_repo.search_audit_logs(
            skip=skip,
            limit=limit,
            action=action,
            user_id=filter_user_id
        )
        total = self.audit_repo.search_audit_logs_count(
            action=action,
            user_id=filter_user_id
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }
