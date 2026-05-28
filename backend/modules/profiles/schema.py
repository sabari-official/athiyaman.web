from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class ProfileUpdateRequest(BaseModel):
    """Pydantic schema to validate incoming citizen profile updates."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    gender: Optional[str] = Field(None, min_length=1, max_length=20)
    dob: Optional[date] = None
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    profession: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=50)
    district: Optional[str] = Field(None, min_length=2, max_length=50)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)
    door_no: Optional[str] = Field(None, max_length=50)
    street_name: Optional[str] = Field(None, max_length=255)
    landmark: Optional[str] = Field(None, max_length=255)
    post_office: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    
    # Sensitive PII inputs - will be encrypted in the service layer
    aadhaar: Optional[str] = Field(None, min_length=12, max_length=12)
    bank_name: Optional[str] = Field(None, min_length=2, max_length=100)
    account_number: Optional[str] = Field(None, min_length=9, max_length=18)
    ifsc_code: Optional[str] = Field(None, min_length=11, max_length=11)
    
    # Nominee Details
    nominee_name: Optional[str] = Field(None, min_length=2, max_length=100)
    nominee_relationship: Optional[str] = Field(None, min_length=2, max_length=50)
    nominee_phone: Optional[str] = Field(None, min_length=10, max_length=10)
    nominee_door_no: Optional[str] = Field(None, max_length=50)
    nominee_street_name: Optional[str] = Field(None, max_length=255)
    nominee_landmark: Optional[str] = Field(None, max_length=255)
    nominee_post_office: Optional[str] = Field(None, max_length=255)
    nominee_city: Optional[str] = Field(None, max_length=100)
    nominee_district: Optional[str] = Field(None, max_length=100)
    nominee_state: Optional[str] = Field(None, max_length=100)
    nominee_pincode: Optional[str] = Field(None, min_length=6, max_length=6)

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.isdigit():
            raise ValueError("Pincode must contain only numeric digits.")
        return v

    @field_validator("aadhaar")
    @classmethod
    def validate_aadhaar(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.isdigit():
            raise ValueError("Aadhaar number must contain only numeric digits.")
        return v

    @field_validator("nominee_phone")
    @classmethod
    def validate_nominee_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.isdigit():
            raise ValueError("Nominee phone must contain only numeric digits.")
        return v

    @field_validator("ifsc_code")
    @classmethod
    def validate_ifsc(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.isalnum():
            raise ValueError("IFSC code must be alphanumeric.")
        return v

class RulesAcceptanceRequest(BaseModel):
    """Pydantic schema to validate rules acceptance clicks."""
    rules_version: str = Field(..., example="v1.0")

class ProfileResponse(BaseModel):
    """Pydantic schema to serialize user profile details for dashboards."""
    id: UUID
    user_id: UUID
    full_name: str
    gender: Optional[str] = None
    dob: Optional[date] = None
    email: Optional[str] = None
    profession: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    door_no: Optional[str] = None
    street_name: Optional[str] = None
    landmark: Optional[str] = None
    post_office: Optional[str] = None
    city: Optional[str] = None
    
    # Masked PII fields for safe UI exposure
    masked_aadhaar: Optional[str] = None
    aadhaar_verified: bool
    bank_verified: bool
    account_number_masked: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None
    
    nominee_name: Optional[str] = None
    nominee_relationship: Optional[str] = None
    nominee_phone: Optional[str] = None
    nominee_door_no: Optional[str] = None
    nominee_street_name: Optional[str] = None
    nominee_landmark: Optional[str] = None
    nominee_post_office: Optional[str] = None
    nominee_city: Optional[str] = None
    nominee_district: Optional[str] = None
    nominee_state: Optional[str] = None
    nominee_pincode: Optional[str] = None
    
    profile_completion: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
