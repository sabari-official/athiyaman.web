from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List

from backend.database.models import CollectionCenter
from backend.modules.collection_centers.repository import CenterRepository
from backend.modules.collection_centers.schema import CenterCreateRequest, CenterUpdateRequest

class CenterService:
    """
    CenterService manages all operations regarding authorized physical centers:
    handling searches based on pincodes, administrative center registers,
    and visibility switches.
    """
    def __init__(self, db: Session):
        self.db = db
        self.center_repo = CenterRepository(db)

    def search_centers(self, pincode: Optional[str] = None, district: Optional[str] = None) -> dict:
        """
        Retrieves active collection centers matching optional pincode or district queries.
        This provides map geocoordinates to navigate physical sites.
        """
        items = self.center_repo.search_active_centers(pincode=pincode, district=district)
        total = self.center_repo.search_active_centers_count(pincode=pincode, district=district)
        return {
            "items": items,
            "total": total
        }

    def get_all_centers(self, skip: int = 0, limit: int = 20) -> dict:
        """Retrieves paginated, comprehensive centers roster for administrative queues."""
        items = self.center_repo.get_all_centers(skip=skip, limit=limit)
        total = self.center_repo.get_all_centers_count()
        return {
            "items": items,
            "total": total
        }

    def create_center(self, admin_id: UUID, payload: CenterCreateRequest) -> CollectionCenter:
        """
        Registers a new Collection Center in the system.
        Only called by authenticated Administrators.
        """
        # Enforce unique center name constraints
        existing = self.db.query(CollectionCenter).filter(
            CollectionCenter.center_name == payload.center_name
        ).first()
        if existing:
            raise ValueError("CENTER_NAME_DUPLICATE")

        center = CollectionCenter(
            center_name=payload.center_name,
            state=payload.state,
            district=payload.district,
            pincode=payload.pincode,
            door_no=payload.door_no,
            street_name=payload.street_name,
            landmark=payload.landmark,
            post_office=payload.post_office,
            city=payload.city,
            latitude=payload.latitude,
            longitude=payload.longitude,
            phone=payload.phone,
            is_active=True
        )
        self.db.add(center)
        self.db.commit()
        self.db.refresh(center)
        return center

    def update_center(self, admin_id: UUID, center_id: UUID, payload: CenterUpdateRequest) -> CollectionCenter:
        """
        Updates details for an existing collection center.
        Only called by authenticated Administrators.
        """
        center = self.center_repo.get_by_id(center_id)
        if not center:
            raise ValueError("CENTER_NOT_FOUND")

        update_dict = payload.model_dump(exclude_unset=True)

        if "center_name" in update_dict and update_dict["center_name"]:
            existing = self.db.query(CollectionCenter).filter(
                CollectionCenter.center_name == update_dict["center_name"],
                CollectionCenter.id != center_id
            ).first()
            if existing:
                raise ValueError("CENTER_NAME_DUPLICATE")

        for field, value in update_dict.items():
            if hasattr(center, field):
                setattr(center, field, value)

        self.db.commit()
        self.db.refresh(center)
        return center

    def toggle_center(self, admin_id: UUID, center_id: UUID) -> CollectionCenter:
        """
        Toggles the active status of a collection center.
        Disabling a center hides it from public search and prevents new waste logs.
        """
        center = self.center_repo.get_by_id(center_id)
        if not center:
            raise ValueError("CENTER_NOT_FOUND")

        center.is_active = not center.is_active
        self.db.commit()
        self.db.refresh(center)
        return center
