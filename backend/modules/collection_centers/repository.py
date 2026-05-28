from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from backend.repositories.base import BaseRepository
from backend.database.models import CollectionCenter

class CenterRepository(BaseRepository[CollectionCenter]):
    """
    CenterRepository implements database queries for collection center
    dictionary lookups, pincode search filters, and status toggles.
    """
    def __init__(self, db: Session):
        super().__init__(CollectionCenter, db)

    def search_active_centers(
        self,
        pincode: Optional[str] = None,
        district: Optional[str] = None
    ) -> List[CollectionCenter]:
        """
        Query all active collection centers.
        Applies optional filters by pincode or district based on user searches.
        """
        query = self.db.query(self.model).filter(self.model.is_active == True)
        if pincode:
            query = query.filter(self.model.pincode == pincode)
        if district:
            query = query.filter(self.model.district.ilike(f"%{district}%"))
        return query.order_by(self.model.center_name).all()

    def search_active_centers_count(
        self,
        pincode: Optional[str] = None,
        district: Optional[str] = None
    ) -> int:
        """Query the total count of filtered active collection centers."""
        query = self.db.query(self.model).filter(self.model.is_active == True)
        if pincode:
            query = query.filter(self.model.pincode == pincode)
        if district:
            query = query.filter(self.model.district.ilike(f"%{district}%"))
        return query.count()

    def get_all_centers(self, skip: int = 0, limit: int = 20) -> List[CollectionCenter]:
        """Query all collection centers (active and inactive) for administrative lists."""
        return self.db.query(self.model).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def get_all_centers_count(self) -> int:
        """Query the total count of all collection centers globally."""
        return self.db.query(self.model).count()
