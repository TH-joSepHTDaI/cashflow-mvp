"""Liability Pydantic schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models import LiabilityType


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