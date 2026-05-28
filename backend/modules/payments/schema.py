from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class PayoutLogRequest(BaseModel):
    """Pydantic schema to capture manual payout details logged by administrators."""
    transaction_reference: str = Field(..., min_length=3, description="The unique commercial bank transaction reference or UTR")
    paid_at: Optional[datetime] = Field(None, description="The actual calendar timestamp of the disbursement (defaults to UTC now)")

class PayoutResponse(BaseModel):
    """Pydantic schema to serialize manual payout transaction record details."""
    transaction_id: UUID = Field(..., description="The payment transaction record UUID")
    claim_id: UUID
    user_id: UUID
    amount: float
    transaction_reference: Optional[str] = None
    status: str
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated lists of payment transactions."""
    items: List[PayoutResponse]
    total: int
    page: int
    limit: int
