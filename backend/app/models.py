from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class CashflowType(str, Enum):
    """Cashflow transaction types."""
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"
    LIABILITY_REPAYMENT = "liability_repayment"
    OTHER = "other"


class Transaction(SQLModel, table=True):
    """Transaction model for income, expenses, investments, etc."""
    __tablename__ = "transactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(..., description="Transaction amount")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    note: Optional[str] = Field(default=None, description="Transaction note/description")
    category: str = Field(..., description="Transaction category")
    cashflow_type: CashflowType = Field(default=CashflowType.OTHER, description="Type of cashflow")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AssetType(str, Enum):
    """Asset types."""
    CASH = "cash"
    BANK_DEPOSIT = "bank_deposit"
    FUND_ETF_STOCK = "fund_etf_stock"
    PROPERTY = "property"
    OTHER = "other"


class Asset(SQLModel, table=True):
    """Asset model for tracking personal assets."""
    __tablename__ = "assets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Asset name")
    asset_type: AssetType = Field(..., description="Type of asset")
    value: float = Field(..., description="Current value")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LiabilityType(str, Enum):
    """Liability types."""
    CREDIT_CARD = "credit_card"
    MORTGAGE = "mortgage"
    CAR_LOAN = "car_loan"
    CONSUMER_LOAN = "consumer_loan"
    OTHER = "other"


class Liability(SQLModel, table=True):
    """Liability model for tracking personal debts."""
    __tablename__ = "liabilities"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Liability name")
    liability_type: LiabilityType = Field(..., description="Type of liability")
    value: float = Field(..., description="Current value (positive number)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
