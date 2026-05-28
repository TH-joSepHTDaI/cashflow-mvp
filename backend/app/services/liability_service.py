"""Liability service - business logic for liabilities."""

from typing import List, Optional
from sqlmodel import Session, select

from app.models import Liability, LiabilityType
from app.schemas import LiabilityCreate, LiabilityUpdate


class LiabilityService:
    """Service for liability business logic."""

    @staticmethod
    def create_liability(session: Session, liability_data: LiabilityCreate) -> Liability:
        """Create a new liability."""
        db_liability = Liability.model_validate(liability_data.model_dump())
        session.add(db_liability)
        session.commit()
        session.refresh(db_liability)
        return db_liability

    @staticmethod
    def list_liabilities(session: Session) -> List[Liability]:
        """List all liabilities."""
        return list(session.exec(select(Liability)).all())

    @staticmethod
    def get_liability(session: Session, liability_id: int) -> Optional[Liability]:
        """Get a liability by ID."""
        return session.get(Liability, liability_id)

    @staticmethod
    def update_liability(
        session: Session,
        liability_id: int,
        liability_update: LiabilityUpdate
    ) -> Optional[Liability]:
        """Update a liability. Returns None if not found."""
        db_liability = session.get(Liability, liability_id)
        if not db_liability:
            return None
        
        # Update only provided fields
        update_data = liability_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_liability, key, value)
        
        session.add(db_liability)
        session.commit()
        session.refresh(db_liability)
        return db_liability

    @staticmethod
    def delete_liability(session: Session, liability_id: int) -> bool:
        """Delete a liability. Returns True if deleted, False if not found."""
        liability = session.get(Liability, liability_id)
        if not liability:
            return False
        
        session.delete(liability)
        session.commit()
        return True

    @staticmethod
    def get_liabilities_by_type(session: Session, liability_type: LiabilityType) -> List[Liability]:
        """Get liabilities filtered by type."""
        return list(session.exec(
            select(Liability).where(Liability.liability_type == liability_type)
        ).all())
