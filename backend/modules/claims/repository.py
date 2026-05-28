from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import RewardClaim

class ClaimRepository(BaseRepository[RewardClaim]):
    """
    ClaimRepository implements SQLAlchemy database access patterns
    for reward milestone claims.
    """
    def __init__(self, db: Session):
        super().__init__(RewardClaim, db)

    def get_user_claims(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[RewardClaim]:
        """Queries paginated reward claims submitted by a specific user."""
        return self.db.query(self.model).filter(
            self.model.user_id == user_id
        ).order_by(self.model.requested_at.desc()).offset(skip).limit(limit).all()

    def get_user_claims_count(self, user_id: UUID) -> int:
        """Queries the total count of reward claims submitted by a specific user."""
        return self.db.query(self.model).filter(self.model.user_id == user_id).count()

    def get_all_claims(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        claim_type: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> List[RewardClaim]:
        """
        Queries paginated, filtered reward claims globally.
        Used primarily for administrative audit queues.
        """
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.status == status)
        if claim_type:
            query = query.filter(self.model.claim_type == claim_type)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.requested_at.desc()).offset(skip).limit(limit).all()

    def get_all_claims_count(
        self,
        status: Optional[str] = None,
        claim_type: Optional[str] = None,
        user_id: Optional[UUID] = None
    ) -> int:
        """Queries the total count of filtered reward claims globally."""
        query = self.db.query(self.model)
        if status:
            query = query.filter(self.model.status == status)
        if claim_type:
            query = query.filter(self.model.claim_type == claim_type)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        return query.count()
