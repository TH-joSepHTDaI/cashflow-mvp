from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Dict, List, Optional
from datetime import datetime, date
from collections import defaultdict

from app.database import get_session
from app.models import Transaction, CashflowType

router = APIRouter(prefix="/api/cashflow", tags=["cashflow"])


@router.get("/monthly/range")
def get_cashflow_range(
    start_month: str = Query(..., description="Start month (YYYY-MM)"),
    end_month: str = Query(..., description="End month (YYYY-MM)"),
    session: Session = Depends(get_session)
):
    """
    Get cashflow summaries for a range of months.
    """
    # Validate formats
    try:
        start_dt = datetime.strptime(start_month, "%Y-%m")
        end_dt = datetime.strptime(end_month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        )
    
    if start_dt > end_dt:
        raise HTTPException(
            status_code=400,
            detail="Start month must be before or equal to end month"
        )
    
    # Generate all months in range to ensure we return empty months too
    current_year, current_month = start_dt.year, start_dt.month
    end_year_val, end_month_val = end_dt.year, end_dt.month
    
    all_months = []
    while (current_year, current_month) <= (end_year_val, end_month_val):
        all_months.append(f"{current_year:04d}-{current_month:02d}")
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    # Parse date range for query
    start_year, start_month_num = map(int, start_month.split("-"))
    end_year, end_month_num = map(int, end_month.split("-"))
    
    start_date = date(start_year, start_month_num, 1)
    if end_month_num == 12:
        end_date = date(end_year + 1, 1, 1)
    else:
        end_date = date(end_year, end_month_num + 1, 1)
    
    # Get all transactions in range
    query = select(Transaction).where(
        Transaction.date >= start_date,
        Transaction.date < end_date
    )
    transactions = session.exec(query).all()
    
    # Group by month
    monthly_data: Dict[str, List[Transaction]] = defaultdict(list)
    for t in transactions:
        month = t.date.strftime("%Y-%m")  # Format as YYYY-MM
        monthly_data[month].append(t)
    
    # Calculate cashflow for each month (including empty months)
    results = []
    for month in all_months:
        results.append(_calculate_cashflow(monthly_data.get(month, []), month))
    
    return {
        "start_month": start_month,
        "end_month": end_month,
        "months": results,
        "summary": _calculate_range_summary(results)
    }


@router.get("/monthly/{year_month}")
def get_monthly_cashflow(
    year_month: str,
    session: Session = Depends(get_session)
):
    """
    Get cashflow summary for a specific month.
    Format: YYYY-MM (e.g., 2024-01)
    """
    # Validate format
    try:
        datetime.strptime(year_month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        )
    
    # Parse year_month and filter by date range
    year, month_num = map(int, year_month.split("-"))
    start_date = date(year, month_num, 1)
    if month_num == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month_num + 1, 1)
    
    query = select(Transaction).where(
        Transaction.date >= start_date,
        Transaction.date < end_date
    )
    transactions = session.exec(query).all()
    
    return _calculate_cashflow(transactions, year_month)


@router.get("/summary")
def get_cashflow_summary(
    month: Optional[str] = Query(None, description="Month (YYYY-MM), defaults to current month"),
    session: Session = Depends(get_session)
):
    """
    Get a brief cashflow summary for a month.
    """
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        )
    
    # Parse month and filter by date range
    year, month_num = map(int, month.split("-"))
    start_date = date(year, month_num, 1)
    if month_num == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month_num + 1, 1)
    
    query = select(Transaction).where(
        Transaction.date >= start_date,
        Transaction.date < end_date
    )
    transactions = session.exec(query).all()
    
    cashflow = _calculate_cashflow(transactions, month)
    
    return {
        "month": month,
        "total_income": cashflow["summary"]["total_income"],
        "total_expense": cashflow["summary"]["total_expense"],
        "total_investment": cashflow["summary"]["total_investment"],
        "total_liability_repayment": cashflow["summary"]["total_liability_repayment"],
        "net_cashflow": cashflow["summary"]["net_cashflow"],
        "transaction_count": len(transactions),
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/by-category/{year_month}")
def get_cashflow_by_category(
    year_month: str,
    session: Session = Depends(get_session)
):
    """
    Get cashflow grouped by category for a specific month.
    """
    try:
        datetime.strptime(year_month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        )
    
    # Parse year_month and filter by date range
    year, month_num = map(int, year_month.split("-"))
    start_date = date(year, month_num, 1)
    if month_num == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month_num + 1, 1)
    
    query = select(Transaction).where(
        Transaction.date >= start_date,
        Transaction.date < end_date
    )
    transactions = session.exec(query).all()
    
    # Group by category
    categories: Dict[str, Dict] = defaultdict(lambda: {
        "income": 0.0,
        "expense": 0.0,
        "investment": 0.0,
        "liability_repayment": 0.0,
        "total": 0.0
    })
    
    for t in transactions:
        cat = t.category or "uncategorized"
        cf_type = t.cashflow_type.value
        
        if cf_type == "income":
            categories[cat]["income"] += t.amount
        elif cf_type == "expense":
            categories[cat]["expense"] += t.amount
        elif cf_type == "investment":
            categories[cat]["investment"] += t.amount
        elif cf_type == "liability_repayment":
            categories[cat]["liability_repayment"] += t.amount
        
        categories[cat]["total"] += t.amount
    
    # Convert to list and round
    result_categories = []
    for cat_name, data in sorted(categories.items()):
        result_categories.append({
            "category": cat_name,
            "income": round(data["income"], 2),
            "expense": round(data["expense"], 2),
            "investment": round(data["investment"], 2),
            "liability_repayment": round(data["liability_repayment"], 2),
            "net": round(data["income"] - data["expense"] - data["investment"] - data["liability_repayment"], 2)
        })
    
    return {
        "month": year_month,
        "categories": result_categories,
        "generated_at": datetime.utcnow().isoformat()
    }


def _calculate_cashflow(transactions: List[Transaction], month: str) -> Dict:
    """Calculate cashflow summary from a list of transactions."""
    
    # Initialize totals
    income = 0.0
    expense = 0.0
    investment = 0.0
    liability_repayment = 0.0
    
    # Group by type
    income_items = []
    expense_items = []
    investment_items = []
    liability_items = []
    
    for t in transactions:
        if t.cashflow_type == CashflowType.INCOME:
            income += t.amount
            income_items.append({
                "id": t.id,
                "date": t.date,
                "amount": round(t.amount, 2),
                "category": t.category,
                "note": t.note
            })
        elif t.cashflow_type == CashflowType.EXPENSE:
            expense += t.amount
            expense_items.append({
                "id": t.id,
                "date": t.date,
                "amount": round(t.amount, 2),
                "category": t.category,
                "note": t.note
            })
        elif t.cashflow_type == CashflowType.INVESTMENT:
            investment += t.amount
            investment_items.append({
                "id": t.id,
                "date": t.date,
                "amount": round(t.amount, 2),
                "category": t.category,
                "note": t.note
            })
        elif t.cashflow_type == CashflowType.LIABILITY_REPAYMENT:
            liability_repayment += t.amount
            liability_items.append({
                "id": t.id,
                "date": t.date,
                "amount": round(t.amount, 2),
                "category": t.category,
                "note": t.note
            })
    
    # Calculate net cashflow
    net_cashflow = income - expense - investment - liability_repayment
    
    return {
        "month": month,
        "summary": {
            "total_income": round(income, 2),
            "total_expense": round(expense, 2),
            "total_investment": round(investment, 2),
            "total_liability_repayment": round(liability_repayment, 2),
            "net_cashflow": round(net_cashflow, 2),
            "transaction_count": len(transactions)
        },
        "details": {
            "income": {
                "total": round(income, 2),
                "count": len(income_items),
                "items": income_items
            },
            "expense": {
                "total": round(expense, 2),
                "count": len(expense_items),
                "items": expense_items
            },
            "investment": {
                "total": round(investment, 2),
                "count": len(investment_items),
                "items": investment_items
            },
            "liability_repayment": {
                "total": round(liability_repayment, 2),
                "count": len(liability_items),
                "items": liability_items
            }
        },
        "generated_at": datetime.utcnow().isoformat()
    }


def _calculate_range_summary(monthly_results: List[Dict]) -> Dict:
    """Calculate summary across multiple months."""
    total_income = sum(m["summary"]["total_income"] for m in monthly_results)
    total_expense = sum(m["summary"]["total_expense"] for m in monthly_results)
    total_investment = sum(m["summary"]["total_investment"] for m in monthly_results)
    total_liability = sum(m["summary"]["total_liability_repayment"] for m in monthly_results)
    total_transactions = sum(m["summary"]["transaction_count"] for m in monthly_results)
    
    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "total_investment": round(total_investment, 2),
        "total_liability_repayment": round(total_liability, 2),
        "net_cashflow": round(total_income - total_expense - total_investment - total_liability, 2),
        "average_monthly_income": round(total_income / len(monthly_results), 2) if monthly_results else 0,
        "average_monthly_expense": round(total_expense / len(monthly_results), 2) if monthly_results else 0,
        "total_transactions": total_transactions
    }
