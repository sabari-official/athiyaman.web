from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import SystemLog, AnalyticsSnapshot

class AnalyticsRepository(BaseRepository[AnalyticsSnapshot]):
    """
    AnalyticsRepository implements database abstraction queries for dashboard views,
    historical snapshots, and diagnostic developer traces.
    """
    def __init__(self, db: Session):
        super().__init__(AnalyticsSnapshot, db)

    def get_precalculated_dashboard_stats(self) -> dict:
        """Queries the vw_dashboard_statistics precalculated view directly."""
        stmt = text("SELECT * FROM vw_dashboard_statistics")
        row = self.db.execute(stmt).first()
        if not row:
            # Fallback in case the view returns no rows
            return {
                "total_users": 0,
                "total_teams": 0,
                "total_members": 0,
                "total_waste": 0.0,
                "total_claims": 0,
                "total_payments": 0.0
            }
        
        # Mapped keys returned from DDL:
        # total_users, total_teams, total_members, total_waste, total_claims, total_payments
        return {
            "total_users": getattr(row, "total_users", 0),
            "total_teams": getattr(row, "total_teams", 0),
            "total_members": getattr(row, "total_members", 0),
            "total_waste": float(getattr(row, "total_waste", 0.0) or 0.0),
            "total_claims": getattr(row, "total_claims", 0),
            "total_payments": float(getattr(row, "total_payments", 0.0) or 0.0)
        }

    def search_system_logs(self, skip: int = 0, limit: int = 50, log_level: Optional[str] = None) -> List[SystemLog]:
        """Queries paginated traces logged in the system_logs explorer table."""
        query = self.db.query(SystemLog)
        if log_level:
            query = query.filter(SystemLog.log_level == log_level.upper())
        return query.order_by(SystemLog.created_at.desc(), SystemLog.id.desc()).offset(skip).limit(limit).all()

    def search_system_logs_count(self, log_level: Optional[str] = None) -> int:
        """Queries the total count of filtered system traces."""
        query = self.db.query(SystemLog)
        if log_level:
            query = query.filter(SystemLog.log_level == log_level.upper())
        return query.count()
