from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class TeamCreateRequest(BaseModel):
    """Pydantic schema to validate new team creation payloads."""
    team_name: str = Field(..., min_length=2, max_length=100, description="Unique and distinct name of the team")
    state: str = Field(..., min_length=2, max_length=50)
    district: str = Field(..., min_length=2, max_length=50)
    pincode: str = Field(..., min_length=6, max_length=6)
    door_no: Optional[str] = Field(None, max_length=50)
    street_name: str = Field(..., min_length=2, max_length=255)
    landmark: Optional[str] = Field(None, max_length=255)
    post_office: str = Field(..., min_length=2, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: str) -> str:
        """Enforces that pincodes consist strictly of 6 numeric digits."""
        if not v.isdigit():
            raise ValueError("Pincode must contain only numeric digits.")
        return v

class TeamResponse(BaseModel):
    """Pydantic schema to serialize complete team configurations."""
    id: UUID
    team_code: str
    team_name: str
    leader_id: UUID
    state: str
    district: str
    pincode: str
    door_no: Optional[str] = None
    street_name: str
    landmark: Optional[str] = None
    post_office: str
    city: str
    member_count: int
    current_level: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class MemberRosterItem(BaseModel):
    """Pydantic schema to serialize individual member details in the team roster."""
    id: UUID
    username: str
    phone_number: str
    joined_at: datetime

class TeamRosterResponse(BaseModel):
    """Pydantic schema to return the list of members in a team roster."""
    team_id: UUID
    team_name: str
    leader_name: str
    members: List[MemberRosterItem]
