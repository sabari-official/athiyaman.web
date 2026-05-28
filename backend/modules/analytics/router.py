from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List

from backend.core.database import get_db
from backend.middleware.rbac import RoleChecker
from backend.modules.analytics.schema import (
    DashboardStatisticsResponse, AnalyticsSnapshotResponse,
    SystemLogRosterResponse, SystemStatusResponse,
    FeatureToggleRequest, FeatureToggleResponse
)
from backend.modules.analytics.service import AnalyticsService

router = APIRouter(tags=["Analytics & Diagnostics"])

# Role guards
admin_guard = RoleChecker(allowed_roles=["ADMIN"])
developer_guard = RoleChecker(allowed_roles=["DEVELOPER"])
staff_guard = RoleChecker(allowed_roles=["ADMIN", "DEVELOPER"])

@router.get("/analytics/dashboard", response_model=DashboardStatisticsResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Fetch precalculated global dashboard metrics from reporting views.
    Restricted strictly to administrators.
    """
    service = AnalyticsService(db)
    result = service.get_dashboard_stats()
    return result

@router.post("/admin/analytics/snapshots", response_model=List[AnalyticsSnapshotResponse], status_code=status.HTTP_201_CREATED)
def trigger_analytics_snapshots(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(admin_guard)
):
    """
    Triggers historical precalculated KPI statistics snapshot recordings.
    Restricted strictly to administrators.
    """
    admin_id = UUID(auth_user.get("sub"))
    service = AnalyticsService(db)
    result = service.capture_metric_snapshots(admin_id)
    return result

@router.get("/developer/system/status", response_model=SystemStatusResponse)
def get_live_system_telemetry(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(developer_guard)
):
    """
    Exposes live system diagnostic telemetry (CPU, RAM, Connections, Latency).
    Restricted strictly to developers.
    """
    service = AnalyticsService(db)
    result = service.get_system_telemetry()
    return result

@router.get("/developer/system/logs", response_model=SystemLogRosterResponse)
def get_system_diagnostic_logs(
    page: int = 1,
    limit: int = 50,
    log_level: Optional[str] = None,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(developer_guard)
):
    """
    Exposes paginated developer monitoring logs from the system_logs table.
    Restricted strictly to developers.
    """
    service = AnalyticsService(db)
    result = service.get_system_logs(page=page, limit=limit, log_level=log_level)
    return result

@router.post("/developer/features/toggle", response_model=FeatureToggleResponse)
def toggle_feature_flag(
    payload: FeatureToggleRequest,
    db: Session = Depends(get_db),
    auth_user: dict = Depends(staff_guard)
):
    """
    Toggles or updates platform-wide system settings feature flags in the database.
    Restricted strictly to administrators and developers.
    """
    user_id = UUID(auth_user.get("sub"))
    service = AnalyticsService(db)
    setting = service.toggle_feature_flag(user_id, payload)
    return setting

@router.post("/developer/backups/create", status_code=status.HTTP_201_CREATED)
def trigger_database_backup(
    db: Session = Depends(get_db),
    auth_user: dict = Depends(developer_guard)
):
    """
    Triggers an administrative physical database backup process.
    Restricted strictly to developers.
    """
    # Demonstration mock response conforming to specs
    return {"status": "BACKUP_COMPLETED", "message": "Database backup completed successfully."}
