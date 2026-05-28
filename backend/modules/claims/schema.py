from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ClaimTypeInput(str, Enum):
    PERSONAL_REWARD = "PERSONAL_REWARD"
    PERSONAL = "PERSONAL"
    TEAM_REWARD = "TEAM_REWARD"
    TEAM = "TEAM"

class ClaimCreateRequest(BaseModel):
    """Pydantic schema to validate new reward milestone claim requests from citizens."""
    claim_type: ClaimTypeInput = Field(..., description="The type of claim: PERSONAL or TEAM")
    level_number: int = Field(..., description="The completed milestone level number (1-6 for TEAM, 7-11 for PERSONAL)")

class ClaimResponse(BaseModel):
    """Pydantic schema to serialize reward claim record details."""
    claim_id: UUID = Field(..., description="The reward claim record UUID")
    user_id: UUID
    claim_type: str
    level_number: int
    amount: float
    status: str
    is_locked: bool
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    requested_at: datetime

    class Config:
        from_attributes = True

class ClaimRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated lists of reward claims."""
    items: List[ClaimResponse]
    total: int
    page: int
    limit: int
