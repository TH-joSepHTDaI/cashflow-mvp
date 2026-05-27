import pytest
from sqlmodel import SQLModel
from pathlib import Path

from app.database import engine, create_db_and_tables, DATABASE_PATH
from app.models import Transaction, Asset, Liability


def test_database_file_created():
    """Test that database file is created."""
    # Ensure data directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Create tables
    create_db_and_tables()
    
    # Check database file exists
    assert DATABASE_PATH.exists(), f"Database file not found at {DATABASE_PATH}"


def test_tables_created():
    """Test that all required tables are created."""
    create_db_and_tables()
    
    # Get all table names from metadata
    tables = SQLModel.metadata.tables
    
    # Check required tables exist
    assert "transactions" in tables, "transactions table not found"
    assert "assets" in tables, "assets table not found"
    assert "liabilities" in tables, "liabilities table not found"


def test_transaction_model():
    """Test Transaction model can be instantiated."""
    from app.models import Transaction, CashflowType
    
    transaction = Transaction(
        amount=100.50,
        date="2024-01-15",
        note="Test transaction",
        category="food",
        cashflow_type=CashflowType.EXPENSE
    )
    
    assert transaction.amount == 100.50
    assert transaction.date == "2024-01-15"
    assert transaction.cashflow_type == CashflowType.EXPENSE


def test_asset_model():
    """Test Asset model can be instantiated."""
    from app.models import Asset, AssetType
    
    asset = Asset(
        name="Savings Account",
        asset_type=AssetType.BANK_DEPOSIT,
        value=5000.00
    )
    
    assert asset.name == "Savings Account"
    assert asset.asset_type == AssetType.BANK_DEPOSIT
    assert asset.value == 5000.00


def test_liability_model():
    """Test Liability model can be instantiated."""
    from app.models import Liability, LiabilityType
    
    liability = Liability(
        name="Credit Card",
        liability_type=LiabilityType.CREDIT_CARD,
        value=1500.00
    )
    
    assert liability.name == "Credit Card"
    assert liability.liability_type == LiabilityType.CREDIT_CARD
    assert liability.value == 1500.00
