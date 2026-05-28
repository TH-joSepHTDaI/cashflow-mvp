import pytest
from app.database import create_db_and_tables


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables before running tests."""
    create_db_and_tables()
    yield
