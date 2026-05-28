from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class BaseApplicationRequest(BaseModel):
    full_name: str = Field(..., max_length=255)
    phone: str = Field(..., min_length=10, max_length=10)
    email: str = Field(..., max_length=255)
    aadhaar: str = Field(..., min_length=12, max_length=12)
    state: str = Field(..., max_length=100)
    district: str = Field(..., max_length=100)
    pincode: str = Field(..., min_length=6, max_length=6)
    door_no: str = Field(..., max_length=50)
    street_name: str = Field(..., max_length=255)
    landmark: Optional[str] = Field(None, max_length=255)
    post_office: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    reason: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain only numeric digits.")
        return v

    @field_validator("aadhaar")
    @classmethod
    def validate_aadhaar(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Aadhaar number must contain only numeric digits.")
        return v

class LeaderApplicationRequest(BaseApplicationRequest):
    pass

class MemberApplicationRequest(BaseApplicationRequest):
    pass

class ApplicationResponse(BaseModel):
    id: UUID
    full_name: str
    phone: str
    email: str
    city: str
    district: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ApplicationApproveRequest(BaseModel):
    status: str = Field(..., description="APPROVED or REJECTED")
