"""Asset service - business logic for assets."""

from typing import List, Optional
from sqlmodel import Session, select

from app.models import Asset, AssetType
from app.schemas import AssetCreate, AssetUpdate


class AssetService:
    """Service for asset business logic."""

    @staticmethod
    def create_asset(session: Session, asset_data: AssetCreate) -> Asset:
        """Create a new asset."""
        db_asset = Asset.model_validate(asset_data.model_dump())
        session.add(db_asset)
        session.commit()
        session.refresh(db_asset)
        return db_asset

    @staticmethod
    def list_assets(session: Session) -> List[Asset]:
        """List all assets."""
        return list(session.exec(select(Asset)).all())

    @staticmethod
    def get_asset(session: Session, asset_id: int) -> Optional[Asset]:
        """Get an asset by ID."""
        return session.get(Asset, asset_id)

    @staticmethod
    def update_asset(
        session: Session,
        asset_id: int,
        asset_update: AssetUpdate
    ) -> Optional[Asset]:
        """Update an asset. Returns None if not found."""
        db_asset = session.get(Asset, asset_id)
        if not db_asset:
            return None
        
        # Update only provided fields
        update_data = asset_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_asset, key, value)
        
        session.add(db_asset)
        session.commit()
        session.refresh(db_asset)
        return db_asset

    @staticmethod
    def delete_asset(session: Session, asset_id: int) -> bool:
        """Delete an asset. Returns True if deleted, False if not found."""
        asset = session.get(Asset, asset_id)
        if not asset:
            return False
        
        session.delete(asset)
        session.commit()
        return True

    @staticmethod
    def get_assets_by_type(session: Session, asset_type: AssetType) -> List[Asset]:
        """Get assets filtered by type."""
        return list(session.exec(
            select(Asset).where(Asset.asset_type == asset_type)
        ).all())
