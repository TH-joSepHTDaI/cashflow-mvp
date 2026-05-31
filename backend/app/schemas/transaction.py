"""Transaction Pydantic schemas."""

from pydantic import BaseModel
from datetime import datetime
from datetime import date as Date
from typing import Optional

from app.models import CashflowType


class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: float
    date: Date
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
    date: Optional[Date] = None
    note: Optional[str] = None
    category: Optional[str] = None
    cashflow_type: Optional[CashflowType] = None