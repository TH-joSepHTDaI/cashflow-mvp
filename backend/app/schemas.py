from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models import CashflowType, AssetType, LiabilityType


# Asset Schemas
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


# Liability Schemas
class LiabilityBase(BaseModel):
    """Base liability schema."""
    name: str
    liability_type: LiabilityType
    value: float


class LiabilityCreate(LiabilityBase):
    """Schema for creating a liability."""
    pass


class LiabilityRead(LiabilityBase):
    """Schema for reading a liability."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LiabilityUpdate(BaseModel):
    """Schema for updating a liability (all fields optional)."""
    name: Optional[str] = None
    liability_type: Optional[LiabilityType] = None
    value: Optional[float] = None


# Transaction Schemas
class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: float
    date: str
    note: Optional[str] = None
    category: str
    cashflow_type: CashflowType = CashflowType.OTHER


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionRead(TransactionBase):
    """Schema for reading a transaction."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction (all fields optional)."""
    amount: Optional[float] = None
    date: Optional[str] = None
    note: Optional[str] = None
    category: Optional[str] = None
    cashflow_type: Optional[CashflowType] = None
