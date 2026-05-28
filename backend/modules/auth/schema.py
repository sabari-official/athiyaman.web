from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional

class UserLoginRequest(BaseModel):
    """Pydantic schema to validate credentials submitted during login."""
    username: str = Field(..., description="Username or registered phone number", min_length=3, max_length=50)
    password: str = Field(..., description="Plain text password", min_length=6)

class UserSignupRequest(BaseModel):
    """Pydantic schema to validate inputs submitted during registration."""
    username: str = Field(..., description="Unique user profile name", min_length=3, max_length=50)
    phone_number: str = Field(..., description="Registered Indian phone number", min_length=10, max_length=10)
    password: str = Field(..., description="Plain text password", min_length=6)
    referral_code: str = Field(..., description="Inviter referral code validating signup permissions")

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Enforces that phone numbers consist strictly of 10 digits."""
        if not v.isdigit():
            raise ValueError("Phone number must contain only numeric digits.")
        return v

class TokenResponse(BaseModel):
    """Pydantic schema to serialize JWT token credentials returned to client."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    must_change_password: bool = False

class ChangePasswordRequest(BaseModel):
    """Schema for forcing a password change on first login or manual change."""
    current_password: str = Field(..., description="Current plain text password")
    new_password: str = Field(..., description="New plain text password", min_length=6)
    new_username: Optional[str] = Field(None, description="Optional new username to replace temporary username", min_length=3, max_length=50)

class VerifyAadhaarRequest(BaseModel):
    """Schema for validating Aadhaar format via Verhoeff."""
    aadhaar: str = Field(..., description="12 digit Aadhaar number", min_length=12, max_length=14)

class VerifyAadhaarResponse(BaseModel):
    valid: bool

class UserResponse(BaseModel):
    """Pydantic schema to serialize basic user details."""
    id: UUID
    username: str
    phone_number: str
    role: str
    user_status: str
    is_verified: bool

    class Config:
        from_attributes = True  # Enable ORM serialization