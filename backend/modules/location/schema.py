from pydantic import BaseModel
from typing import Optional

class PincodeLocationResponse(BaseModel):
    success: bool
    message: str
    post_office: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
