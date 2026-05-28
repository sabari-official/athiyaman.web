from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

class AuditLogResponse(BaseModel):
    """Pydantic schema to serialize database mutation audit logs."""
    id: UUID
    user_id: Optional[UUID] = None
    role: Optional[str] = None
    action: str
    entity_type: str
    entity_id: Optional[UUID] = None
    old_values: Optional[Any] = None
    new_values: Optional[Any] = None
    ip_address: Optional[str] = None
    device: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AuditRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated lists of audit logs."""
    items: List[AuditLogResponse]
    total: int
    page: int
    limit: int
