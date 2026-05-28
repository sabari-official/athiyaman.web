from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class AnnouncementCreateRequest(BaseModel):
    """Pydantic schema to validate new public announcement creations."""
    title: str = Field(..., min_length=3, description="The title of the platform announcement")
    message: str = Field(..., min_length=10, description="The full click-wrap message content body")
    start_date: date = Field(..., description="Calendar date when announcement becomes active")
    end_date: date = Field(..., description="Calendar date when announcement automatically expires")

class AnnouncementResponse(BaseModel):
    """Pydantic schema to serialize public announcement details."""
    id: UUID
    title: str
    message: str
    start_date: date
    end_date: date
    is_active: bool

    class Config:
        from_attributes = True

class NotificationCreateRequest(BaseModel):
    """Pydantic schema to validate target broadcast notifications from administrators."""
    title: str = Field(..., min_length=3, description="The title of the targeted notification")
    message: str = Field(..., min_length=5, description="The main message body text")
    target_type: str = Field("ALL", description="Target user role scope: ALL, MEMBER, LEADER, ADMIN, DEVELOPER")

class NotificationResponse(BaseModel):
    """Pydantic schema to serialize broadcast notification details."""
    id: UUID
    title: str
    message: str
    target_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationLogResponse(BaseModel):
    """Pydantic schema to serialize individual user notification logs."""
    id: UUID
    notification_id: UUID
    notification: NotificationResponse
    delivered: bool
    delivered_at: Optional[datetime] = None
    is_read: bool
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NotificationRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated citizen notifications list."""
    items: List[NotificationLogResponse]
    total: int
    page: int
    limit: int
