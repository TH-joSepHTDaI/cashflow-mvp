import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.database import engine
from app.models import Transaction

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_transactions():
    """Cleanup all transactions before each test."""
    with Session(engine) as session:
        # Delete all transactions before test
        for t in session.exec(select(Transaction)).all():
            session.delete(t)
        session.commit()
    yield
    # Cleanup after test as well
    with Session(engine) as session:
        for t in session.exec(select(Transaction)).all():
            session.delete(t)
        session.commit()


def test_create_transaction():
    """Test creating a transaction."""
    response = client.post("/api/transactions/", json={
        "amount": 100.50,
        "date": "2024-01-15",
        "note": "Grocery shopping",
        "category": "food",
        "cashflow_type": "expense"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.50
    assert data["date"] == "2024-01-15"
    assert data["category"] == "food"
    assert data["cashflow_type"] == "expense"
    assert "id" in data
    assert "created_at" in data


def test_list_transactions():
    """Test listing transactions."""
    # Create a transaction first
    client.post("/api/transactions/", json={
        "amount": 50.00,
        "date": "2024-01-20",
        "note": "Coffee",
        "category": "food",
        "cashflow_type": "expense"
    })
    
    response = client.get("/api/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_transactions_by_month():
    """Test filtering transactions by month."""
    # Create transactions for different months
    client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "January expense",
        "category": "food",
        "cashflow_type": "expense"
    })
    client.post("/api/transactions/", json={
        "amount": 200.00,
        "date": "2024-02-10",
        "note": "February expense",
        "category": "food",
        "cashflow_type": "expense"
    })
    
    # Filter by January
    response = client.get("/api/transactions/?month=2024-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"].startswith("2024-01")


def test_get_transaction():
    """Test getting a specific transaction."""
    # Create a transaction
    create_response = client.post("/api/transactions/", json={
        "amount": 75.00,
        "date": "2024-01-25",
        "note": "Restaurant",
        "category": "food",
        "cashflow_type": "expense"
    })
    transaction_id = create_response.json()["id"]
    
    # Get the transaction
    response = client.get(f"/api/transactions/{transaction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["amount"] == 75.00


def test_get_transaction_not_found():
    """Test getting a non-existent transaction."""
    response = client.get("/api/transactions/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"


def test_update_transaction():
    """Test updating a transaction."""
    # Create a transaction
    create_response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "Original note",
        "category": "food",
        "cashflow_type": "expense"
    })
    transaction_id = create_response.json()["id"]
    
    # Update the transaction
    response = client.put(f"/api/transactions/{transaction_id}", json={
        "amount": 150.00,
        "note": "Updated note"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 150.00
    assert data["note"] == "Updated note"
    assert data["category"] == "food"  # Unchanged


def test_update_transaction_not_found():
    """Test updating a non-existent transaction."""
    response = client.put("/api/transactions/99999", json={
        "amount": 100.00
    })
    assert response.status_code == 404


def test_delete_transaction():
    """Test deleting a transaction."""
    # Create a transaction
    create_response = client.post("/api/transactions/", json={
        "amount": 50.00,
        "date": "2024-01-30",
        "note": "To be deleted",
        "category": "other",
        "cashflow_type": "expense"
    })
    transaction_id = create_response.json()["id"]
    
    # Delete the transaction
    response = client.delete(f"/api/transactions/{transaction_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/transactions/{transaction_id}")
    assert get_response.status_code == 404


def test_delete_transaction_not_found():
    """Test deleting a non-existent transaction."""
    response = client.delete("/api/transactions/99999")
    assert response.status_code == 404
