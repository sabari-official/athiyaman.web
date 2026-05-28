from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class WasteCreateRequest(BaseModel):
    """Pydantic schema to validate new waste collection log requests from managers."""
    user_id: UUID = Field(..., description="The citizen (Member/Leader) UUID who deposited the waste")
    center_id: UUID = Field(..., description="The authorized Collection Center UUID where waste was physically weighed")
    weight_kg: float = Field(..., ge=0.1, le=50.0, description="The verified physical weight of collected waste in KG (0.1 - 50.0)")
    image_path: str = Field(..., description="The path or URL to the verified scale photo evidence")
    collection_date: date = Field(..., description="The physical calendar date of the collection event")
    location: Optional[str] = Field(None, description="Optional metadata describing collection desk or counter details")

class WasteResponse(BaseModel):
    """Pydantic schema to serialize waste collection record details."""
    id: UUID
    user_id: UUID
    center_id: UUID
    weight_kg: float
    image_path: Optional[str] = None
    collection_date: date
    location: Optional[str] = None
    verification_status: str
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    payment_status: str
    amount_paid: float
    created_at: datetime

    class Config:
        from_attributes = True

class WasteRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated list of waste collections."""
    items: List[WasteResponse]
    total: int
    page: int
    limit: int

class AdminVerifyRequest(BaseModel):
    """Pydantic schema to capture comments during administrative verification audits."""
    comments: str = Field(..., min_length=5, description="Auditor review notes explaining findings and confirmation references")
