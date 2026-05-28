from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.audit.schema import AuditRosterResponse
from backend.modules.audit.service import AuditService

router = APIRouter(tags=["Audit"])

# Route guard restricted strictly to administrators
admin_guard = RoleChecker(allowed_roles=["ADMIN"])

@router.get("/admin/audits", response_model=AuditRosterResponse)
def get_global_audit_trail(
    page: int = 1,
    limit: int = 50,
    action: Optional[str] = None,
    filter_user_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Exposes paginated global lists of database mutation audit logs.
    Restricted strictly to administrators.
    """
    service = AuditService(db)
    result = service.get_audit_logs(
        page=page,
        limit=limit,
        action=action,
        filter_user_id=filter_user_id
    )
    return result
