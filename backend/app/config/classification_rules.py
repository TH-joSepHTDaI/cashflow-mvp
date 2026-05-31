"""
Classification rules for automatic transaction categorization.

This module contains keyword-based rules for classifying transactions
into cashflow types. Rules can be extended for AI-based classification.
"""

from app.models import CashflowType


# Classification keywords mapped to cashflow types
CLASSIFICATION_RULES = {
    CashflowType.INCOME: [
        "salary", "wage", "income", "工资", "收入", "薪水", "薪资"
    ],
    CashflowType.EXPENSE: [
        # Fixed expenses
        "rent", "mortgage", "房租", "房贷", "租金",
        # Daily expenses
        "food", "restaurant", "coffee", "supermarket",
        "饭", "餐厅", "咖啡", "超市", "食物", "餐饮", "买菜"
    ],
    CashflowType.INVESTMENT: [
        "fund", "etf", "stock", "基金", "股票", "定投", "投资"
    ],
    CashflowType.LIABILITY_REPAYMENT: [
        "credit card", "loan repayment", "信用卡", "还款", "贷款", "还贷"
    ]
}


# Sub-categories for granular classification (future use with AI classification)
# Maps cashflow types to potential sub-categories
SUB_CATEGORIES = {
    CashflowType.INCOME: [
        "salary",           # Regular employment income
        "bonus",            # Performance/annual bonus
        "freelance",        # Contract/freelance work
        "investment_income", # Dividends, interest
        "gift",             # Received gifts
        "refund",           # Refunds/reimbursements
        "other_income"      # Miscellaneous income
    ],
    CashflowType.EXPENSE: [
        # Fixed expenses
        "housing",          # Rent, mortgage, property fees
        "utilities",        # Electricity, water, gas, internet
        "insurance",        # Health, life, property insurance
        "subscription",     # Recurring subscriptions
        
        # Variable/Daily expenses
        "food",             # Groceries, restaurants
        "transportation",   # Public transit, fuel, parking
        "shopping",         # Clothing, electronics, general
        "entertainment",    # Movies, games, hobbies
        "healthcare",       # Medical, dental, pharmacy
        "education",        # Courses, books, training
        "personal_care",    # Hair, beauty, gym
        "other_expense"     # Miscellaneous expenses
    ],
    CashflowType.INVESTMENT: [
        "stocks",           # Individual stocks
        "bonds",            # Government/corporate bonds
        "mutual_funds",     # Mutual funds
        "etf",              # Exchange-traded funds
        "crypto",           # Cryptocurrency
        "real_estate",      # Property investments
        "retirement",       # 401k, IRA, pension
        "other_investment"  # Other investment vehicles
    ],
    CashflowType.LIABILITY_REPAYMENT: [
        "credit_card",      # Credit card payments
        "mortgage_payment", # Home loan repayment
        "student_loan",     # Education loan repayment
        "personal_loan",    # Personal loan repayment
        "car_loan",         # Auto loan repayment
        "other_liability"   # Other debt repayment
    ],
    CashflowType.OTHER: [
        "transfer",         # Internal transfers
        "adjustment",       # Account adjustments
        "unknown",          # Uncategorized
        "other"             # Other/miscellaneous
    ]
}
