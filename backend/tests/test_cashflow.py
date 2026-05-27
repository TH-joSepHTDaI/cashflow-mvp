import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.database import engine
from app.models import Transaction, CashflowType

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_transactions():
    """Cleanup all transactions before each test."""
    with Session(engine) as session:
        for t in session.exec(select(Transaction)).all():
            session.delete(t)
        session.commit()
    yield
    with Session(engine) as session:
        for t in session.exec(select(Transaction)).all():
            session.delete(t)
        session.commit()


def test_monthly_cashflow_empty():
    """Test monthly cashflow with no transactions."""
    response = client.get("/api/cashflow/monthly/2024-01")
    assert response.status_code == 200
    
    data = response.json()
    assert data["month"] == "2024-01"
    assert data["summary"]["total_income"] == 0.0
    assert data["summary"]["total_expense"] == 0.0
    assert data["summary"]["net_cashflow"] == 0.0
    assert data["summary"]["transaction_count"] == 0


def test_monthly_cashflow_with_data():
    """Test monthly cashflow with various transaction types."""
    # Create income transaction
    client.post("/api/transactions/", json={
        "amount": 5000.00,
        "date": "2024-01-15",
        "note": "Monthly salary",
        "category": "salary",
        "cashflow_type": "income"
    })
    
    # Create expense transactions
    client.post("/api/transactions/", json={
        "amount": 1000.00,
        "date": "2024-01-10",
        "note": "Rent payment",
        "category": "housing",
        "cashflow_type": "expense"
    })
    client.post("/api/transactions/", json={
        "amount": 300.00,
        "date": "2024-01-20",
        "note": "Groceries",
        "category": "food",
        "cashflow_type": "expense"
    })
    
    # Create investment transaction
    client.post("/api/transactions/", json={
        "amount": 1000.00,
        "date": "2024-01-05",
        "note": "Stock purchase",
        "category": "investment",
        "cashflow_type": "investment"
    })
    
    response = client.get("/api/cashflow/monthly/2024-01")
    assert response.status_code == 200
    
    data = response.json()
    assert data["month"] == "2024-01"
    assert data["summary"]["total_income"] == 5000.00
    assert data["summary"]["total_expense"] == 1300.00
    assert data["summary"]["total_investment"] == 1000.00
    assert data["summary"]["net_cashflow"] == 2700.00
    assert data["summary"]["transaction_count"] == 4
    
    # Check details
    assert data["details"]["income"]["count"] == 1
    assert data["details"]["expense"]["count"] == 2
    assert data["details"]["investment"]["count"] == 1


def test_monthly_cashflow_invalid_format():
    """Test monthly cashflow with invalid date format."""
    response = client.get("/api/cashflow/monthly/invalid")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]


def test_cashflow_range():
    """Test cashflow range endpoint."""
    # Create transactions for multiple months
    client.post("/api/transactions/", json={
        "amount": 5000.00,
        "date": "2024-01-15",
        "note": "January salary",
        "category": "salary",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 2000.00,
        "date": "2024-01-20",
        "note": "January rent",
        "category": "housing",
        "cashflow_type": "expense"
    })
    client.post("/api/transactions/", json={
        "amount": 5500.00,
        "date": "2024-02-15",
        "note": "February salary",
        "category": "salary",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 2000.00,
        "date": "2024-02-20",
        "note": "February rent",
        "category": "housing",
        "cashflow_type": "expense"
    })
    
    response = client.get("/api/cashflow/monthly/range?start_month=2024-01&end_month=2024-02")
    assert response.status_code == 200
    
    data = response.json()
    assert data["start_month"] == "2024-01"
    assert data["end_month"] == "2024-02"
    assert len(data["months"]) == 2
    
    # Check summary
    assert data["summary"]["total_income"] == 10500.00
    assert data["summary"]["total_expense"] == 4000.00
    assert data["summary"]["net_cashflow"] == 6500.00
    assert data["summary"]["average_monthly_income"] == 5250.00
    assert data["summary"]["average_monthly_expense"] == 2000.00


def test_cashflow_range_invalid_order():
    """Test cashflow range with invalid month order."""
    response = client.get("/api/cashflow/monthly/range?start_month=2024-03&end_month=2024-01")
    assert response.status_code == 400
    assert "Start month must be before" in response.json()["detail"]


def test_cashflow_summary():
    """Test cashflow summary endpoint."""
    # Create transactions
    client.post("/api/transactions/", json={
        "amount": 6000.00,
        "date": "2024-03-15",
        "note": "Salary",
        "category": "salary",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 500.00,
        "date": "2024-03-10",
        "note": "Credit card payment",
        "category": "debt",
        "cashflow_type": "liability_repayment"
    })
    
    response = client.get("/api/cashflow/summary?month=2024-03")
    assert response.status_code == 200
    
    data = response.json()
    assert data["month"] == "2024-03"
    assert data["total_income"] == 6000.00
    assert data["total_liability_repayment"] == 500.00
    assert data["net_cashflow"] == 5500.00
    assert data["transaction_count"] == 2


def test_cashflow_by_category():
    """Test cashflow grouped by category."""
    # Create transactions in different categories
    client.post("/api/transactions/", json={
        "amount": 5000.00,
        "date": "2024-04-15",
        "note": "Salary",
        "category": "salary",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 2000.00,
        "date": "2024-04-01",
        "note": "Rent",
        "category": "housing",
        "cashflow_type": "expense"
    })
    client.post("/api/transactions/", json={
        "amount": 150.00,
        "date": "2024-04-10",
        "note": "Dinner",
        "category": "food",
        "cashflow_type": "expense"
    })
    client.post("/api/transactions/", json={
        "amount": 80.00,
        "date": "2024-04-12",
        "note": "Lunch",
        "category": "food",
        "cashflow_type": "expense"
    })
    
    response = client.get("/api/cashflow/by-category/2024-04")
    assert response.status_code == 200
    
    data = response.json()
    assert data["month"] == "2024-04"
    assert len(data["categories"]) == 3  # salary, housing, food
    
    # Find categories
    categories = {c["category"]: c for c in data["categories"]}
    assert categories["salary"]["income"] == 5000.00
    assert categories["housing"]["expense"] == 2000.00
    assert categories["food"]["expense"] == 230.00


def test_cashflow_filters_by_month():
    """Test that cashflow only includes transactions from specified month."""
    # Create transactions in different months
    client.post("/api/transactions/", json={
        "amount": 1000.00,
        "date": "2024-05-15",
        "note": "May transaction",
        "category": "test",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 2000.00,
        "date": "2024-06-15",
        "note": "June transaction",
        "category": "test",
        "cashflow_type": "income"
    })
    
    # Query May
    response = client.get("/api/cashflow/monthly/2024-05")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["total_income"] == 1000.00
    assert data["summary"]["transaction_count"] == 1
    
    # Query June
    response = client.get("/api/cashflow/monthly/2024-06")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["total_income"] == 2000.00
    assert data["summary"]["transaction_count"] == 1


def test_cashflow_negative_net():
    """Test cashflow when expenses exceed income."""
    client.post("/api/transactions/", json={
        "amount": 2000.00,
        "date": "2024-07-15",
        "note": "Small income",
        "category": "salary",
        "cashflow_type": "income"
    })
    client.post("/api/transactions/", json={
        "amount": 3000.00,
        "date": "2024-07-10",
        "note": "Big expense",
        "category": "housing",
        "cashflow_type": "expense"
    })
    
    response = client.get("/api/cashflow/monthly/2024-07")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["net_cashflow"] == -1000.00
