from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TeamLevelProgressResponse(BaseModel):
    """Pydantic schema to serialize team progression level details."""
    level_number: int = Field(..., description="The progressive Team Level (1-6)")
    current_progress: int = Field(..., description="Current verified member count of the team")
    requirement_value: int = Field(..., description="Required member count to complete this level")
    completed: bool = Field(..., description="True if the level milestone has been completed")
    completed_at: Optional[datetime] = Field(None, description="Timestamp when milestone was completed")
    reward_amount: float = Field(..., description="Financial reward amount associated with this level")

    class Config:
        from_attributes = True

class PersonalLevelProgressResponse(BaseModel):
    """Pydantic schema to serialize individual citizen progression level details."""
    level_number: int = Field(..., description="The progressive Personal Level (7-11)")
    waste_kg: float = Field(..., description="Approved waste weight (KG) logged for this specific level")
    requirement_value: float = Field(..., description="Required waste weight (KG) to complete this level")
    completed: bool = Field(..., description="True if the level milestone has been completed")
    completed_at: Optional[datetime] = Field(None, description="Timestamp when milestone was completed")
    reward_amount: float = Field(..., description="Financial reward amount associated with this level")

    class Config:
        from_attributes = True
