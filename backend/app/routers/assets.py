from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models import Asset
from app.schemas import AssetCreate, AssetRead, AssetUpdate

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.post("/", response_model=AssetRead, status_code=201)
def create_asset(asset: AssetCreate, session: Session = Depends(get_session)):
    """Create a new asset."""
    db_asset = Asset.model_validate(asset.model_dump())
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


@router.get("/", response_model=List[AssetRead])
def list_assets(session: Session = Depends(get_session)):
    """List all assets."""
    assets = session.exec(select(Asset)).all()
    return assets


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: int, session: Session = Depends(get_session)):
    """Get an asset by ID."""
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetRead)
def update_asset(
    asset_id: int,
    asset_update: AssetUpdate,
    session: Session = Depends(get_session)
):
    """Update an asset."""
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Update only provided fields
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
    
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, session: Session = Depends(get_session)):
    """Delete an asset."""
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    session.delete(asset)
    session.commit()
    return None
