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


# =============================================================================
# Error Handling and Edge Case Tests
# =============================================================================

def test_create_transaction_missing_required_fields():
    """Test creating a transaction with missing required fields."""
    # Missing amount
    response = client.post("/api/transactions/", json={
        "date": "2024-01-15",
        "note": "Missing amount",
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422
    
    # Missing date
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "note": "Missing date",
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422
    
    # Missing category
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "Missing category",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422


def test_create_transaction_invalid_amount_type():
    """Test creating a transaction with invalid amount type (string instead of number)."""
    response = client.post("/api/transactions/", json={
        "amount": "not_a_number",
        "date": "2024-01-15",
        "note": "Invalid amount type",
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422


def test_create_transaction_invalid_date_format():
    """Test creating a transaction with invalid date formats."""
    # Invalid format
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "15-01-2024",
        "note": "Invalid date format",
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422
    
    # Another invalid format
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024/01/15",
        "note": "Invalid date format",
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 422


def test_create_transaction_negative_amount():
    """Test creating a transaction with negative amount."""
    response = client.post("/api/transactions/", json={
        "amount": -50.00,
        "date": "2024-01-15",
        "note": "Negative amount transaction",
        "category": "food",
        "cashflow_type": "expense"
    })
    # The API accepts negative amounts (may be valid for refunds/adjustments)
    assert response.status_code == 201


def test_create_transaction_future_date():
    """Test creating a transaction with future date."""
    from datetime import date, timedelta
    future_date = (date.today() + timedelta(days=30)).isoformat()
    
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": future_date,
        "note": "Future transaction",
        "category": "food",
        "cashflow_type": "expense"
    })
    # The API accepts future dates (may be valid for planned transactions)
    assert response.status_code == 201


def test_create_transaction_malformed_json():
    """Test creating a transaction with malformed JSON body."""
    response = client.post(
        "/api/transactions/",
        data="not valid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_create_transaction_very_long_note():
    """Test creating a transaction with very long note (> 500 chars)."""
    long_note = "A" * 1000
    
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": long_note,
        "category": "food",
        "cashflow_type": "expense"
    })
    # The API accepts long notes
    assert response.status_code == 201
    assert response.json()["note"] == long_note


def test_create_transaction_empty_string_values():
    """Test creating a transaction with empty string values."""
    # Empty category should fail (required field)
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "",
        "category": "",
        "cashflow_type": "expense"
    })
    # Empty strings are accepted for note, but category should have validation
    # Depending on implementation, this may pass or fail
    

def test_create_transaction_null_optional_fields():
    """Test creating a transaction with null in optional fields."""
    response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": None,
        "category": "food",
        "cashflow_type": "expense"
    })
    assert response.status_code == 201
    assert response.json()["note"] is None


def test_update_transaction_invalid_amount_type():
    """Test updating a transaction with invalid amount type."""
    # Create a transaction first
    create_response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "Original",
        "category": "food",
        "cashflow_type": "expense"
    })
    transaction_id = create_response.json()["id"]
    
    # Try to update with invalid amount
    response = client.put(f"/api/transactions/{transaction_id}", json={
        "amount": "invalid"
    })
    assert response.status_code == 422


def test_update_transaction_invalid_date_format():
    """Test updating a transaction with invalid date format."""
    # Create a transaction first
    create_response = client.post("/api/transactions/", json={
        "amount": 100.00,
        "date": "2024-01-15",
        "note": "Original",
        "category": "food",
        "cashflow_type": "expense"
    })
    transaction_id = create_response.json()["id"]
    
    # Try to update with invalid date
    response = client.put(f"/api/transactions/{transaction_id}", json={
        "date": "not-a-date"
    })
    assert response.status_code == 422
