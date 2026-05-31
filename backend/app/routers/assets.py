from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas import AssetCreate, AssetRead, AssetUpdate
from app.services import AssetService

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])


@router.post("/", response_model=AssetRead, status_code=201)
def create_asset(asset: AssetCreate, session: Session = Depends(get_session)):
    """Create a new asset."""
    return AssetService.create_asset(session, asset)


@router.get("/", response_model=List[AssetRead])
def list_assets(session: Session = Depends(get_session)):
    """List all assets."""
    return AssetService.list_assets(session)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: int, session: Session = Depends(get_session)):
    """Get an asset by ID."""
    asset = AssetService.get_asset(session, asset_id)
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
    asset = AssetService.update_asset(session, asset_id, asset_update)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, session: Session = Depends(get_session)):
    """Delete an asset."""
    deleted = AssetService.delete_asset(session, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return None
