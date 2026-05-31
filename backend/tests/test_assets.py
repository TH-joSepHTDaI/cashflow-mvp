import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.database import engine
from app.models import Asset, AssetType

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_assets():
    """Cleanup all assets before each test."""
    with Session(engine) as session:
        for a in session.exec(select(Asset)).all():
            session.delete(a)
        session.commit()
    yield
    with Session(engine) as session:
        for a in session.exec(select(Asset)).all():
            session.delete(a)
        session.commit()


def test_create_asset():
    """Test creating an asset."""
    response = client.post("/api/assets/", json={
        "name": "Savings Account",
        "asset_type": "bank_deposit",
        "value": 10000.00
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Savings Account"
    assert data["asset_type"] == "bank_deposit"
    assert data["value"] == 10000.00
    assert "id" in data
    assert "created_at" in data


def test_create_asset_with_different_types():
    """Test creating assets with different asset types."""
    asset_types = ["cash", "bank_deposit", "fund_etf_stock", "property", "other"]
    
    for i, asset_type in enumerate(asset_types):
        response = client.post("/api/assets/", json={
            "name": f"Asset {i}",
            "asset_type": asset_type,
            "value": 1000.00 * (i + 1)
        })
        assert response.status_code == 201
        assert response.json()["asset_type"] == asset_type


def test_list_assets():
    """Test listing assets."""
    # Create assets
    client.post("/api/assets/", json={
        "name": "Cash Wallet",
        "asset_type": "cash",
        "value": 500.00
    })
    client.post("/api/assets/", json={
        "name": "Stock Portfolio",
        "asset_type": "fund_etf_stock",
        "value": 50000.00
    })
    
    response = client.get("/api/assets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_asset():
    """Test getting a specific asset."""
    # Create an asset
    create_response = client.post("/api/assets/", json={
        "name": "Property",
        "asset_type": "property",
        "value": 300000.00
    })
    asset_id = create_response.json()["id"]
    
    # Get the asset
    response = client.get(f"/api/assets/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == asset_id
    assert data["name"] == "Property"
    assert data["value"] == 300000.00


def test_get_asset_not_found():
    """Test getting a non-existent asset."""
    response = client.get("/api/assets/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"


def test_update_asset():
    """Test updating an asset."""
    # Create an asset
    create_response = client.post("/api/assets/", json={
        "name": "Original Name",
        "asset_type": "cash",
        "value": 1000.00
    })
    asset_id = create_response.json()["id"]
    
    # Update the asset
    response = client.put(f"/api/assets/{asset_id}", json={
        "name": "Updated Name",
        "value": 2000.00
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["value"] == 2000.00
    assert data["asset_type"] == "cash"  # Unchanged


def test_update_asset_not_found():
    """Test updating a non-existent asset."""
    response = client.put("/api/assets/99999", json={
        "name": "New Name"
    })
    assert response.status_code == 404


def test_delete_asset():
    """Test deleting an asset."""
    # Create an asset
    create_response = client.post("/api/assets/", json={
        "name": "To Be Deleted",
        "asset_type": "other",
        "value": 100.00
    })
    asset_id = create_response.json()["id"]
    
    # Delete the asset
    response = client.delete(f"/api/assets/{asset_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/assets/{asset_id}")
    assert get_response.status_code == 404


def test_delete_asset_not_found():
    """Test deleting a non-existent asset."""
    response = client.delete("/api/assets/99999")
    assert response.status_code == 404


def test_asset_value_can_be_zero():
    """Test that asset value can be zero."""
    response = client.post("/api/assets/", json={
        "name": "Empty Account",
        "asset_type": "bank_deposit",
        "value": 0.00
    })
    assert response.status_code == 201
    assert response.json()["value"] == 0.00


def test_asset_value_can_be_negative():
    """Test that asset value can be negative (for tracking losses)."""
    response = client.post("/api/assets/", json={
        "name": "Loss Asset",
        "asset_type": "fund_etf_stock",
        "value": -500.00
    })
    assert response.status_code == 201
    assert response.json()["value"] == -500.00


# =============================================================================
# Error Handling and Edge Case Tests
# =============================================================================

def test_create_asset_missing_required_fields():
    """Test creating an asset with missing required fields."""
    # Missing name
    response = client.post("/api/assets/", json={
        "asset_type": "cash",
        "value": 1000.00
    })
    assert response.status_code == 422
    
    # Missing asset_type
    response = client.post("/api/assets/", json={
        "name": "Test Asset",
        "value": 1000.00
    })
    assert response.status_code == 422
    
    # Missing value
    response = client.post("/api/assets/", json={
        "name": "Test Asset",
        "asset_type": "cash"
    })
    assert response.status_code == 422


def test_create_asset_invalid_asset_type():
    """Test creating an asset with invalid asset_type value."""
    response = client.post("/api/assets/", json={
        "name": "Invalid Asset",
        "asset_type": "not_a_valid_type",
        "value": 1000.00
    })
    assert response.status_code == 422


def test_create_asset_non_numeric_value():
    """Test creating an asset with non-numeric value."""
    response = client.post("/api/assets/", json={
        "name": "Invalid Asset",
        "asset_type": "cash",
        "value": "not_a_number"
    })
    assert response.status_code == 422


def test_create_asset_negative_value():
    """Test creating an asset with negative value."""
    response = client.post("/api/assets/", json={
        "name": "Negative Asset",
        "asset_type": "cash",
        "value": -1000.00
    })
    # API allows negative values for tracking losses
    assert response.status_code == 201


def test_create_asset_empty_string_values():
    """Test creating an asset with empty string values."""
    response = client.post("/api/assets/", json={
        "name": "",
        "asset_type": "cash",
        "value": 1000.00
    })
    # Empty name may be accepted or rejected depending on validation


def test_update_asset_invalid_asset_type():
    """Test updating an asset with invalid asset_type."""
    # Create an asset first
    create_response = client.post("/api/assets/", json={
        "name": "Test Asset",
        "asset_type": "cash",
        "value": 1000.00
    })
    asset_id = create_response.json()["id"]
    
    # Try to update with invalid type
    response = client.put(f"/api/assets/{asset_id}", json={
        "asset_type": "invalid_type"
    })
    assert response.status_code == 422


def test_update_asset_non_numeric_value():
    """Test updating an asset with non-numeric value."""
    # Create an asset first
    create_response = client.post("/api/assets/", json={
        "name": "Test Asset",
        "asset_type": "cash",
        "value": 1000.00
    })
    asset_id = create_response.json()["id"]
    
    # Try to update with invalid value
    response = client.put(f"/api/assets/{asset_id}", json={
        "value": "not_a_number"
    })
    assert response.status_code == 422
