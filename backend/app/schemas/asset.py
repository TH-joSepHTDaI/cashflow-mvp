"""Asset Pydantic schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models import AssetType


class AssetBase(BaseModel):
    """Base asset schema."""
    name: str
    asset_type: AssetType
    value: float


class AssetCreate(AssetBase):
    """Schema for creating an asset."""
    pass


class AssetRead(AssetBase):
    """Schema for reading an asset."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetUpdate(BaseModel):
    """Schema for updating an asset (all fields optional)."""
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    value: Optional[float] = None