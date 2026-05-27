import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.classifier import classify_transaction, get_classification_reason, CLASSIFICATION_RULES
from app.models import CashflowType, Transaction
from app.main import app
from app.database import engine


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


class TestClassificationRules:
    """Test transaction classification rules."""
    
    def test_salary_classified_as_income(self):
        """Test salary keywords are classified as income."""
        assert classify_transaction("Monthly salary") == CashflowType.INCOME
        assert classify_transaction("Wage payment") == CashflowType.INCOME
        assert classify_transaction("工资收入") == CashflowType.INCOME
        assert classify_transaction("薪水") == CashflowType.INCOME
    
    def test_rent_classified_as_expense(self):
        """Test rent/mortgage keywords are classified as expense."""
        assert classify_transaction("Monthly rent") == CashflowType.EXPENSE
        assert classify_transaction("Mortgage payment") == CashflowType.EXPENSE
        assert classify_transaction("房租") == CashflowType.EXPENSE
        assert classify_transaction("房贷") == CashflowType.EXPENSE
    
    def test_food_classified_as_expense(self):
        """Test food keywords are classified as expense."""
        assert classify_transaction("Restaurant dinner") == CashflowType.EXPENSE
        assert classify_transaction("Coffee shop") == CashflowType.EXPENSE
        assert classify_transaction("Supermarket shopping") == CashflowType.EXPENSE
        assert classify_transaction("餐厅吃饭") == CashflowType.EXPENSE
        assert classify_transaction("买咖啡") == CashflowType.EXPENSE
        assert classify_transaction("超市买菜") == CashflowType.EXPENSE
    
    def test_investment_classified_as_investment(self):
        """Test investment keywords are classified as investment."""
        assert classify_transaction("Stock purchase") == CashflowType.INVESTMENT
        assert classify_transaction("ETF investment") == CashflowType.INVESTMENT
        assert classify_transaction("Fund subscription") == CashflowType.INVESTMENT
        assert classify_transaction("基金定投") == CashflowType.INVESTMENT
        assert classify_transaction("买股票") == CashflowType.INVESTMENT
    
    def test_loan_classified_as_liability_repayment(self):
        """Test loan keywords are classified as liability repayment."""
        assert classify_transaction("Credit card payment") == CashflowType.LIABILITY_REPAYMENT
        assert classify_transaction("Loan repayment") == CashflowType.LIABILITY_REPAYMENT
        assert classify_transaction("信用卡还款") == CashflowType.LIABILITY_REPAYMENT
        assert classify_transaction("还贷款") == CashflowType.LIABILITY_REPAYMENT
    
    def test_unknown_classified_as_other(self):
        """Test unknown keywords are classified as other."""
        assert classify_transaction("Random text") == CashflowType.OTHER
        assert classify_transaction("XYZ123") == CashflowType.OTHER
        assert classify_transaction("") == CashflowType.OTHER
    
    def test_category_used_in_classification(self):
        """Test that category is also used for classification."""
        assert classify_transaction("", "salary") == CashflowType.INCOME
        assert classify_transaction("", "food") == CashflowType.EXPENSE
        assert classify_transaction("", "stock") == CashflowType.INVESTMENT


class TestClassificationReason:
    """Test classification reason function."""
    
    def test_reason_shows_matched_keyword(self):
        """Test that reason shows which keyword matched."""
        reason = get_classification_reason("Monthly salary")
        assert "salary" in reason
        assert "income" in reason
    
    def test_reason_shows_no_match(self):
        """Test that reason shows no match for unknown."""
        reason = get_classification_reason("Random text")
        assert "no match" in reason
        assert "other" in reason


class TestAPIClassificationIntegration:
    """Test classification integrated with API."""
    
    def test_create_transaction_with_auto_classification(self):
        """Test that transactions are auto-classified on creation."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        # Create transaction without specifying cashflow_type
        response = client.post("/api/transactions/", json={
            "amount": 5000.00,
            "date": "2024-01-15",
            "note": "Monthly salary",
            "category": "income"
        })
        
        assert response.status_code == 201
        data = response.json()
        # Should be auto-classified as income
        assert data["cashflow_type"] == "income"
    
    def test_create_transaction_food_auto_classified(self):
        """Test food transactions are auto-classified as expense."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        response = client.post("/api/transactions/", json={
            "amount": 50.00,
            "date": "2024-01-15",
            "note": "Restaurant lunch",
            "category": "food"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["cashflow_type"] == "expense"
    
    def test_create_transaction_investment_auto_classified(self):
        """Test investment transactions are auto-classified."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        response = client.post("/api/transactions/", json={
            "amount": 1000.00,
            "date": "2024-01-15",
            "note": "ETF purchase",
            "category": "investment"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["cashflow_type"] == "investment"
