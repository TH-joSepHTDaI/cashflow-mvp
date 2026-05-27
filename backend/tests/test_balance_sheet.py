import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.database import engine
from app.models import Asset, Liability, AssetType, LiabilityType

client = TestClient(app)


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


def test_balance_sheet_empty():
    """Test balance sheet with no assets or liabilities."""
    response = client.get("/api/balance-sheet/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["summary"]["total_assets"] == 0.0
    assert data["summary"]["total_liabilities"] == 0.0
    assert data["summary"]["net_worth"] == 0.0
    assert data["assets"]["items"] == []
    assert data["liabilities"]["items"] == []


def test_balance_sheet_with_data():
    """Test balance sheet with assets and liabilities."""
    # Create assets
    client.post("/api/assets/", json={
        "name": "Cash Wallet",
        "asset_type": "cash",
        "value": 1000.00
    })
    client.post("/api/assets/", json={
        "name": "Savings Account",
        "asset_type": "bank_deposit",
        "value": 5000.00
    })
    client.post("/api/assets/", json={
        "name": "Stock Portfolio",
        "asset_type": "fund_etf_stock",
        "value": 10000.00
    })
    
    # Create liabilities
    client.post("/api/liabilities/", json={
        "name": "Credit Card",
        "liability_type": "credit_card",
        "value": 500.00
    })
    client.post("/api/liabilities/", json={
        "name": "Car Loan",
        "liability_type": "car_loan",
        "value": 10000.00
    })
    
    response = client.get("/api/balance-sheet/")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check summary
    assert data["summary"]["total_assets"] == 16000.00
    assert data["summary"]["total_liabilities"] == 10500.00
    assert data["summary"]["net_worth"] == 5500.00
    
    # Check assets breakdown
    assert data["assets"]["total"] == 16000.00
    assert data["assets"]["by_type"]["cash"] == 1000.00
    assert data["assets"]["by_type"]["bank_deposit"] == 5000.00
    assert data["assets"]["by_type"]["fund_etf_stock"] == 10000.00
    assert len(data["assets"]["items"]) == 3
    
    # Check liabilities breakdown
    assert data["liabilities"]["total"] == 10500.00
    assert data["liabilities"]["by_type"]["credit_card"] == 500.00
    assert data["liabilities"]["by_type"]["car_loan"] == 10000.00
    assert len(data["liabilities"]["items"]) == 2


def test_balance_sheet_summary():
    """Test balance sheet summary endpoint."""
    # Create some data
    client.post("/api/assets/", json={
        "name": "Property",
        "asset_type": "property",
        "value": 300000.00
    })
    client.post("/api/liabilities/", json={
        "name": "Mortgage",
        "liability_type": "mortgage",
        "value": 200000.00
    })
    
    response = client.get("/api/balance-sheet/summary")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_assets"] == 300000.00
    assert data["total_liabilities"] == 200000.00
    assert data["net_worth"] == 100000.00
    assert data["asset_count"] == 1
    assert data["liability_count"] == 1
    assert "generated_at" in data


def test_balance_sheet_negative_net_worth():
    """Test balance sheet when liabilities exceed assets."""
    # Create small asset
    client.post("/api/assets/", json={
        "name": "Small Savings",
        "asset_type": "cash",
        "value": 1000.00
    })
    
    # Create large liability
    client.post("/api/liabilities/", json={
        "name": "Big Loan",
        "liability_type": "consumer_loan",
        "value": 5000.00
    })
    
    response = client.get("/api/balance-sheet/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["summary"]["total_assets"] == 1000.00
    assert data["summary"]["total_liabilities"] == 5000.00
    assert data["summary"]["net_worth"] == -4000.00


def test_assets_by_type():
    """Test getting assets by type."""
    # Create multiple cash assets
    client.post("/api/assets/", json={
        "name": "Cash in Wallet",
        "asset_type": "cash",
        "value": 200.00
    })
    client.post("/api/assets/", json={
        "name": "Emergency Cash",
        "asset_type": "cash",
        "value": 500.00
    })
    
    # Create a different type
    client.post("/api/assets/", json={
        "name": "Stocks",
        "asset_type": "fund_etf_stock",
        "value": 10000.00
    })
    
    response = client.get("/api/balance-sheet/assets/by-type/cash")
    assert response.status_code == 200
    
    data = response.json()
    assert data["asset_type"] == "cash"
    assert data["total_value"] == 700.00
    assert data["count"] == 2
    assert len(data["items"]) == 2


def test_assets_by_type_invalid():
    """Test getting assets by invalid type."""
    response = client.get("/api/balance-sheet/assets/by-type/invalid_type")
    assert response.status_code == 400
    assert "Invalid asset type" in response.json()["detail"]


def test_liabilities_by_type():
    """Test getting liabilities by type."""
    # Create multiple credit card liabilities
    client.post("/api/liabilities/", json={
        "name": "Visa Card",
        "liability_type": "credit_card",
        "value": 1000.00
    })
    client.post("/api/liabilities/", json={
        "name": "Mastercard",
        "liability_type": "credit_card",
        "value": 500.00
    })
    
    response = client.get("/api/balance-sheet/liabilities/by-type/credit_card")
    assert response.status_code == 200
    
    data = response.json()
    assert data["liability_type"] == "credit_card"
    assert data["total_value"] == 1500.00
    assert data["count"] == 2
    assert len(data["items"]) == 2


def test_liabilities_by_type_invalid():
    """Test getting liabilities by invalid type."""
    response = client.get("/api/balance-sheet/liabilities/by-type/invalid_type")
    assert response.status_code == 400
    assert "Invalid liability type" in response.json()["detail"]


def test_balance_sheet_decimal_rounding():
    """Test that decimal values are properly rounded."""
    # Create asset with decimal
    client.post("/api/assets/", json={
        "name": "Precise Asset",
        "asset_type": "cash",
        "value": 1000.999
    })
    
    response = client.get("/api/balance-sheet/summary")
    assert response.status_code == 200
    
    data = response.json()
    # Should be rounded to 2 decimal places
    assert data["total_assets"] == 1001.0
