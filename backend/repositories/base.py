from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Decoupled Generic Base Repository class implementing clean SQLAlchemy database operations.
    Shields Service layers from raw query sessions handling.
    """
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: UUID) -> Optional[T]:
        """Queries single model entity matching the time-ordered UUID identifier."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Queries all instances of the entity with mandatory pagination bounds."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: T) -> T:
        """Saves a new declarative model record inside the active transaction session."""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, db_obj: T, update_data: dict) -> T:
        """Updates attributes on a persistent model entity inside the active transaction session."""
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: T) -> bool:
        """Physical deletion helper (restricted strictly to transient/dependency tables)."""
        try:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
