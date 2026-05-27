import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.database import engine
from app.models import Liability, LiabilityType

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_liabilities():
    """Cleanup all liabilities before each test."""
    with Session(engine) as session:
        for l in session.exec(select(Liability)).all():
            session.delete(l)
        session.commit()
    yield
    with Session(engine) as session:
        for l in session.exec(select(Liability)).all():
            session.delete(l)
        session.commit()


def test_create_liability():
    """Test creating a liability."""
    response = client.post("/api/liabilities/", json={
        "name": "Credit Card Debt",
        "liability_type": "credit_card",
        "value": 5000.00
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Credit Card Debt"
    assert data["liability_type"] == "credit_card"
    assert data["value"] == 5000.00
    assert "id" in data
    assert "created_at" in data


def test_create_liability_with_different_types():
    """Test creating liabilities with different liability types."""
    liability_types = ["credit_card", "mortgage", "car_loan", "consumer_loan", "other"]
    
    for i, liability_type in enumerate(liability_types):
        response = client.post("/api/liabilities/", json={
            "name": f"Liability {i}",
            "liability_type": liability_type,
            "value": 1000.00 * (i + 1)
        })
        assert response.status_code == 201
        assert response.json()["liability_type"] == liability_type


def test_list_liabilities():
    """Test listing liabilities."""
    # Create liabilities
    client.post("/api/liabilities/", json={
        "name": "Credit Card",
        "liability_type": "credit_card",
        "value": 2000.00
    })
    client.post("/api/liabilities/", json={
        "name": "Home Mortgage",
        "liability_type": "mortgage",
        "value": 300000.00
    })
    
    response = client.get("/api/liabilities/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_liability():
    """Test getting a specific liability."""
    # Create a liability
    create_response = client.post("/api/liabilities/", json={
        "name": "Car Loan",
        "liability_type": "car_loan",
        "value": 25000.00
    })
    liability_id = create_response.json()["id"]
    
    # Get the liability
    response = client.get(f"/api/liabilities/{liability_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == liability_id
    assert data["name"] == "Car Loan"
    assert data["value"] == 25000.00


def test_get_liability_not_found():
    """Test getting a non-existent liability."""
    response = client.get("/api/liabilities/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Liability not found"


def test_update_liability():
    """Test updating a liability."""
    # Create a liability
    create_response = client.post("/api/liabilities/", json={
        "name": "Original Liability",
        "liability_type": "consumer_loan",
        "value": 10000.00
    })
    liability_id = create_response.json()["id"]
    
    # Update the liability
    response = client.put(f"/api/liabilities/{liability_id}", json={
        "name": "Updated Liability",
        "value": 8000.00
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Liability"
    assert data["value"] == 8000.00
    assert data["liability_type"] == "consumer_loan"  # Unchanged


def test_update_liability_not_found():
    """Test updating a non-existent liability."""
    response = client.put("/api/liabilities/99999", json={
        "name": "New Name"
    })
    assert response.status_code == 404


def test_delete_liability():
    """Test deleting a liability."""
    # Create a liability
    create_response = client.post("/api/liabilities/", json={
        "name": "To Be Deleted",
        "liability_type": "other",
        "value": 500.00
    })
    liability_id = create_response.json()["id"]
    
    # Delete the liability
    response = client.delete(f"/api/liabilities/{liability_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/liabilities/{liability_id}")
    assert get_response.status_code == 404


def test_delete_liability_not_found():
    """Test deleting a non-existent liability."""
    response = client.delete("/api/liabilities/99999")
    assert response.status_code == 404


def test_liability_value_can_be_zero():
    """Test that liability value can be zero (paid off)."""
    response = client.post("/api/liabilities/", json={
        "name": "Paid Off Loan",
        "liability_type": "consumer_loan",
        "value": 0.00
    })
    assert response.status_code == 201
    assert response.json()["value"] == 0.00
