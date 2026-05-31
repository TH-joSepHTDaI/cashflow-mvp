"""Tests for service layer business logic."""

import pytest
from sqlmodel import Session, select

from app.database import engine
from app.models import Asset, AssetType, Liability, LiabilityType
from app.services.asset_service import AssetService
from app.services.liability_service import LiabilityService
from app.schemas import AssetCreate, LiabilityCreate


@pytest.fixture(autouse=True)
def cleanup_database():
    """Cleanup all assets and liabilities before each test."""
    with Session(engine) as session:
        for a in session.exec(select(Asset)).all():
            session.delete(a)
        for l in session.exec(select(Liability)).all():
            session.delete(l)
        session.commit()
    yield
    with Session(engine) as session:
        for a in session.exec(select(Asset)).all():
            session.delete(a)
        for l in session.exec(select(Liability)).all():
            session.delete(l)
        session.commit()


# =============================================================================
# Asset Service Tests
# =============================================================================

class TestAssetService:
    """Tests for AssetService."""

    def test_get_assets_by_type_cash(self):
        """Test filtering assets by type: cash."""
        with Session(engine) as session:
            # Create assets of different types
            AssetService.create_asset(session, AssetCreate(
                name="Cash Wallet",
                asset_type=AssetType.CASH,
                value=500.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Bank Account",
                asset_type=AssetType.BANK_DEPOSIT,
                value=5000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Piggy Bank",
                asset_type=AssetType.CASH,
                value=100.00
            ))

            # Filter by cash type
            cash_assets = AssetService.get_assets_by_type(session, AssetType.CASH)
            assert len(cash_assets) == 2
            assert all(a.asset_type == AssetType.CASH for a in cash_assets)

    def test_get_assets_by_type_bank_deposit(self):
        """Test filtering assets by type: bank_deposit."""
        with Session(engine) as session:
            # Create assets of different types
            AssetService.create_asset(session, AssetCreate(
                name="Savings Account",
                asset_type=AssetType.BANK_DEPOSIT,
                value=10000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Checking Account",
                asset_type=AssetType.BANK_DEPOSIT,
                value=2500.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Stock ETF",
                asset_type=AssetType.FUND_ETF_STOCK,
                value=50000.00
            ))

            # Filter by bank_deposit type
            deposit_assets = AssetService.get_assets_by_type(session, AssetType.BANK_DEPOSIT)
            assert len(deposit_assets) == 2
            assert all(a.asset_type == AssetType.BANK_DEPOSIT for a in deposit_assets)

    def test_get_assets_by_type_fund_etf_stock(self):
        """Test filtering assets by type: fund_etf_stock."""
        with Session(engine) as session:
            # Create assets of different types
            AssetService.create_asset(session, AssetCreate(
                name="Stock Portfolio",
                asset_type=AssetType.FUND_ETF_STOCK,
                value=75000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Crypto",
                asset_type=AssetType.FUND_ETF_STOCK,
                value=5000.00
            ))

            # Filter by fund_etf_stock type
            stock_assets = AssetService.get_assets_by_type(session, AssetType.FUND_ETF_STOCK)
            assert len(stock_assets) == 2
            assert all(a.asset_type == AssetType.FUND_ETF_STOCK for a in stock_assets)

    def test_get_assets_by_type_property(self):
        """Test filtering assets by type: property."""
        with Session(engine) as session:
            # Create assets of different types
            AssetService.create_asset(session, AssetCreate(
                name="Home",
                asset_type=AssetType.PROPERTY,
                value=500000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Rental Property",
                asset_type=AssetType.PROPERTY,
                value=300000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Cash",
                asset_type=AssetType.CASH,
                value=1000.00
            ))

            # Filter by property type
            property_assets = AssetService.get_assets_by_type(session, AssetType.PROPERTY)
            assert len(property_assets) == 2
            assert all(a.asset_type == AssetType.PROPERTY for a in property_assets)

    def test_get_assets_by_type_other(self):
        """Test filtering assets by type: other."""
        with Session(engine) as session:
            # Create assets of different types
            AssetService.create_asset(session, AssetCreate(
                name="Collectibles",
                asset_type=AssetType.OTHER,
                value=5000.00
            ))
            AssetService.create_asset(session, AssetCreate(
                name="Art",
                asset_type=AssetType.OTHER,
                value=10000.00
            ))

            # Filter by other type
            other_assets = AssetService.get_assets_by_type(session, AssetType.OTHER)
            assert len(other_assets) == 2
            assert all(a.asset_type == AssetType.OTHER for a in other_assets)

    def test_get_assets_by_type_empty_result(self):
        """Test filtering assets by type when no assets of that type exist."""
        with Session(engine) as session:
            # Create only cash assets
            AssetService.create_asset(session, AssetCreate(
                name="Cash Wallet",
                asset_type=AssetType.CASH,
                value=500.00
            ))

            # Filter by property type (none exist)
            property_assets = AssetService.get_assets_by_type(session, AssetType.PROPERTY)
            assert len(property_assets) == 0
            assert isinstance(property_assets, list)


# =============================================================================
# Liability Service Tests
# =============================================================================

class TestLiabilityService:
    """Tests for LiabilityService."""

    def test_get_liabilities_by_type_credit_card(self):
        """Test filtering liabilities by type: credit_card."""
        with Session(engine) as session:
            # Create liabilities of different types
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Visa Card",
                liability_type=LiabilityType.CREDIT_CARD,
                value=2500.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Mastercard",
                liability_type=LiabilityType.CREDIT_CARD,
                value=1500.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Home Loan",
                liability_type=LiabilityType.MORTGAGE,
                value=300000.00
            ))

            # Filter by credit_card type
            cc_liabilities = LiabilityService.get_liabilities_by_type(session, LiabilityType.CREDIT_CARD)
            assert len(cc_liabilities) == 2
            assert all(l.liability_type == LiabilityType.CREDIT_CARD for l in cc_liabilities)

    def test_get_liabilities_by_type_mortgage(self):
        """Test filtering liabilities by type: mortgage."""
        with Session(engine) as session:
            # Create liabilities of different types
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Primary Residence",
                liability_type=LiabilityType.MORTGAGE,
                value=400000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Vacation Home",
                liability_type=LiabilityType.MORTGAGE,
                value=200000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Car Loan",
                liability_type=LiabilityType.CAR_LOAN,
                value=25000.00
            ))

            # Filter by mortgage type
            mortgage_liabilities = LiabilityService.get_liabilities_by_type(session, LiabilityType.MORTGAGE)
            assert len(mortgage_liabilities) == 2
            assert all(l.liability_type == LiabilityType.MORTGAGE for l in mortgage_liabilities)

    def test_get_liabilities_by_type_car_loan(self):
        """Test filtering liabilities by type: car_loan."""
        with Session(engine) as session:
            # Create liabilities of different types
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Toyota Loan",
                liability_type=LiabilityType.CAR_LOAN,
                value=20000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Honda Loan",
                liability_type=LiabilityType.CAR_LOAN,
                value=15000.00
            ))

            # Filter by car_loan type
            car_loans = LiabilityService.get_liabilities_by_type(session, LiabilityType.CAR_LOAN)
            assert len(car_loans) == 2
            assert all(l.liability_type == LiabilityType.CAR_LOAN for l in car_loans)

    def test_get_liabilities_by_type_consumer_loan(self):
        """Test filtering liabilities by type: consumer_loan."""
        with Session(engine) as session:
            # Create liabilities of different types
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Personal Loan",
                liability_type=LiabilityType.CONSUMER_LOAN,
                value=10000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Student Loan",
                liability_type=LiabilityType.CONSUMER_LOAN,
                value=50000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Credit Card",
                liability_type=LiabilityType.CREDIT_CARD,
                value=3000.00
            ))

            # Filter by consumer_loan type
            consumer_loans = LiabilityService.get_liabilities_by_type(session, LiabilityType.CONSUMER_LOAN)
            assert len(consumer_loans) == 2
            assert all(l.liability_type == LiabilityType.CONSUMER_LOAN for l in consumer_loans)

    def test_get_liabilities_by_type_other(self):
        """Test filtering liabilities by type: other."""
        with Session(engine) as session:
            # Create liabilities of different types
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Medical Debt",
                liability_type=LiabilityType.OTHER,
                value=5000.00
            ))
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Family Loan",
                liability_type=LiabilityType.OTHER,
                value=2000.00
            ))

            # Filter by other type
            other_liabilities = LiabilityService.get_liabilities_by_type(session, LiabilityType.OTHER)
            assert len(other_liabilities) == 2
            assert all(l.liability_type == LiabilityType.OTHER for l in other_liabilities)

    def test_get_liabilities_by_type_empty_result(self):
        """Test filtering liabilities by type when no liabilities of that type exist."""
        with Session(engine) as session:
            # Create only credit card liabilities
            LiabilityService.create_liability(session, LiabilityCreate(
                name="Credit Card",
                liability_type=LiabilityType.CREDIT_CARD,
                value=2500.00
            ))

            # Filter by mortgage type (none exist)
            mortgage_liabilities = LiabilityService.get_liabilities_by_type(session, LiabilityType.MORTGAGE)
            assert len(mortgage_liabilities) == 0
            assert isinstance(mortgage_liabilities, list)
