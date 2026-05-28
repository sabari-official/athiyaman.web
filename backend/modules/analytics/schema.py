from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class DashboardStatisticsResponse(BaseModel):
    """Pydantic schema to serialize precalculated global platform statistics."""
    total_users: int
    total_teams: int
    total_members: int
    total_waste: float
    total_claims: int
    total_payments: float

class AnalyticsSnapshotResponse(BaseModel):
    """Pydantic schema to serialize historical analytics snapshots."""
    id: UUID
    metric_name: str
    metric_value: float
    snapshot_date: date
    snapshot_type: str

    class Config:
        from_attributes = True

class SystemLogResponse(BaseModel):
    """Pydantic schema to serialize developer monitoring logs."""
    id: UUID
    log_level: str
    source: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class SystemLogRosterResponse(BaseModel):
    """Pydantic schema to serialize paginated Lists of system traces."""
    items: List[SystemLogResponse]
    total: int
    page: int
    limit: int

class SystemStatusResponse(BaseModel):
    """Pydantic schema to serialize developer live hardware telemetry."""
    cpu_usage: float
    memory_usage: float
    active_db_connections: int
    api_latency_ms: int

class FeatureToggleRequest(BaseModel):
    """Pydantic schema to validate feature flag settings toggles."""
    setting_key: str = Field(..., min_length=1, description="Unique platform feature setting identifier")
    setting_value: str = Field(..., min_length=1, description="Dynamic string representation of the setting flag state")

class FeatureToggleResponse(BaseModel):
    """Pydantic schema to serialize feature flag updates."""
    setting_key: str
    setting_value: str
    updated_at: datetime

    class Config:
        from_attributes = True
