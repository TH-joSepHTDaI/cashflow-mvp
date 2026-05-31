"""
Transaction classification rules for automatic categorization.

Rules:
- salary, wage, income, 工资, 收入 → income
- rent, mortgage, 房租, 房贷 → fixed_expense
- food, restaurant, coffee, supermarket, 饭, 餐厅, 咖啡, 超市 → daily_expense
- fund, ETF, stock, 基金, 股票, 定投 → investment
- credit card, loan repayment, 信用卡, 还款, 贷款 → liability_repayment
- unknown → other
"""

from app.models import CashflowType
from app.config import CLASSIFICATION_RULES


def classify_transaction(note: str, category: str = "") -> CashflowType:
    """
    Classify a transaction based on note and category.
    
    Args:
        note: Transaction note/description
        category: Transaction category (optional)
    
    Returns:
        CashflowType: The classified cashflow type
    """
    # Combine note and category for classification
    text = f"{note} {category}".lower()
    
    # Check each rule
    for cashflow_type, keywords in CLASSIFICATION_RULES.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return cashflow_type
    
    # Default to other if no match
    return CashflowType.OTHER


def get_classification_reason(note: str, category: str = "") -> str:
    """
    Get the reason for classification (which keyword matched).
    
    Args:
        note: Transaction note/description
        category: Transaction category (optional)
    
    Returns:
        str: The matched keyword or "no match"
    """
    text = f"{note} {category}".lower()
    
    for cashflow_type, keywords in CLASSIFICATION_RULES.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return f"Matched '{keyword}' → {cashflow_type.value}"
    
    return "no match → other"
