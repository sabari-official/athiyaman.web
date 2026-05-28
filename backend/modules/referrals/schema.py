from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class ReferralCreateRequest(BaseModel):
    """Pydantic schema to validate new referral code generation requests."""
    referral_type: str = Field(..., description="Invitation type strictly: LEADER or TEAM")
    level_number: Optional[int] = Field(None, ge=1, le=6, description="Team progress Level number required if TEAM referral")

    @field_validator("referral_type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Enforces that referral types strictly match designated roles."""
        upper_v = v.upper()
        if upper_v not in {"LEADER", "TEAM"}:
            raise ValueError("referral_type must be either LEADER or TEAM.")
        return upper_v

class ReferralResponse(BaseModel):
    """Pydantic schema to serialize referral configuration parameters."""
    id: UUID
    code: str
    referral_type: str
    team_id: Optional[UUID] = None
    level_number: Optional[int] = None
    generated_by: UUID
    max_usage: int
    used_count: int
    is_active: bool
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
