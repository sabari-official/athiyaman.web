from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CenterCreateRequest(BaseModel):
    """Pydantic schema to validate new collection center creation requests from Admin."""
    center_name: str = Field(..., min_length=3, max_length=255, description="The authorized unique physical name of the collection center")
    state: str = Field(..., description="State where the collection center is physically located")
    district: str = Field(..., description="District region where the collection center is physically located")
    pincode: str = Field(..., min_length=6, max_length=6, description="6-digit unique postal pincode matching center location")
    door_no: str = Field(..., description="Door number of the center")
    street_name: str = Field(..., description="Street name of the center")
    landmark: Optional[str] = Field(None, description="Landmark near the center")
    post_office: str = Field(..., description="Post office region")
    city: str = Field(..., description="City or town of the center")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Optional geocoded map coordinates - Latitude")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Optional geocoded map coordinates - Longitude")
    phone: Optional[str] = Field(None, description="Active public contact helpline phone number of the center")

class CenterUpdateRequest(BaseModel):
    """Pydantic schema to validate updates on center details."""
    center_name: Optional[str] = Field(None, min_length=3, max_length=255)
    state: Optional[str] = Field(None)
    district: Optional[str] = Field(None)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)
    door_no: Optional[str] = Field(None)
    street_name: Optional[str] = Field(None)
    landmark: Optional[str] = Field(None)
    post_office: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    phone: Optional[str] = Field(None)

class CenterResponse(BaseModel):
    """Pydantic schema to serialize collection center details."""
    id: UUID
    center_name: str
    state: str
    district: str
    pincode: str
    door_no: str
    street_name: str
    landmark: Optional[str] = None
    post_office: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CenterRosterResponse(BaseModel):
    """Pydantic schema to serialize list of queried collection centers."""
    items: List[CenterResponse]
    total: int
