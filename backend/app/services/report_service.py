"""Report service - business logic for cashflow and balance sheet reports."""

from datetime import date, datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from sqlmodel import Session, select

from app.models import Transaction, Asset, Liability, CashflowType, AssetType, LiabilityType


class ReportService:
    """Service for report generation business logic."""

    # ==================== Cashflow Reports ====================

    @staticmethod
    def get_monthly_cashflow(
        session: Session,
        year_month: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get cashflow summary for a specific month.
        Returns (cashflow_data, error_message).
        """
        # Validate format
        try:
            datetime.strptime(year_month, "%Y-%m")
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        
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
        
        return ReportService._calculate_cashflow(list(transactions), year_month), None

    @staticmethod
    def get_cashflow_range(
        session: Session,
        start_month: str,
        end_month: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get cashflow summaries for a range of months.
        Returns (cashflow_data, error_message).
        """
        # Validate formats
        try:
            start_dt = datetime.strptime(start_month, "%Y-%m")
            end_dt = datetime.strptime(end_month, "%Y-%m")
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        
        if start_dt > end_dt:
            return None, "Start month must be before or equal to end month"
        
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
            month = t.date.strftime("%Y-%m")
            monthly_data[month].append(t)
        
        # Calculate cashflow for each month (including empty months)
        results = []
        for month in all_months:
            results.append(ReportService._calculate_cashflow(monthly_data.get(month, []), month))
        
        return {
            "start_month": start_month,
            "end_month": end_month,
            "months": results,
            "summary": ReportService._calculate_range_summary(results)
        }, None

    @staticmethod
    def get_cashflow_summary(
        session: Session,
        month: Optional[str] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get a brief cashflow summary for a month.
        Returns (summary_data, error_message).
        """
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        
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
        
        cashflow = ReportService._calculate_cashflow(list(transactions), month)
        
        return {
            "month": month,
            "total_income": cashflow["summary"]["total_income"],
            "total_expense": cashflow["summary"]["total_expense"],
            "total_investment": cashflow["summary"]["total_investment"],
            "total_liability_repayment": cashflow["summary"]["total_liability_repayment"],
            "net_cashflow": cashflow["summary"]["net_cashflow"],
            "transaction_count": len(transactions),
            "generated_at": datetime.utcnow().isoformat()
        }, None

    @staticmethod
    def get_cashflow_by_category(
        session: Session,
        year_month: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get cashflow grouped by category for a specific month.
        Returns (category_data, error_message).
        """
        try:
            datetime.strptime(year_month, "%Y-%m")
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM (e.g., 2024-01)"
        
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
        }, None

    # ==================== Balance Sheet Reports ====================

    @staticmethod
    def get_balance_sheet(session: Session) -> Dict:
        """Get the complete balance sheet summary."""
        # Get all assets
        assets = session.exec(select(Asset)).all()
        
        # Get all liabilities
        liabilities = session.exec(select(Liability)).all()
        
        # Calculate totals
        total_assets = sum(asset.value for asset in assets)
        total_liabilities = sum(liability.value for liability in liabilities)
        net_worth = total_assets - total_liabilities
        
        # Group assets by type
        assets_by_type: Dict[str, float] = {}
        for asset in assets:
            asset_type = asset.asset_type.value
            assets_by_type[asset_type] = assets_by_type.get(asset_type, 0) + asset.value
        
        # Group liabilities by type
        liabilities_by_type: Dict[str, float] = {}
        for liability in liabilities:
            liability_type = liability.liability_type.value
            liabilities_by_type[liability_type] = liabilities_by_type.get(liability_type, 0) + liability.value
        
        # Build liability items list
        liability_items = []
        for liability in liabilities:
            liability_items.append({
                "id": liability.id,
                "name": liability.name,
                "type": liability.liability_type.value,
                "value": round(liability.value, 2)
            })
        
        return {
            "summary": {
                "total_assets": round(total_assets, 2),
                "total_liabilities": round(total_liabilities, 2),
                "net_worth": round(net_worth, 2)
            },
            "assets": {
                "total": round(total_assets, 2),
                "by_type": {k: round(v, 2) for k, v in assets_by_type.items()},
                "items": [
                    {
                        "id": asset.id,
                        "name": asset.name,
                        "type": asset.asset_type.value,
                        "value": round(asset.value, 2)
                    }
                    for asset in assets
                ]
            },
            "liabilities": {
                "total": round(total_liabilities, 2),
                "by_type": {k: round(v, 2) for k, v in liabilities_by_type.items()},
                "items": liability_items
            },
            "generated_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_balance_sheet_summary(session: Session) -> Dict:
        """Get a brief balance sheet summary (totals only)."""
        # Get all assets
        assets = session.exec(select(Asset)).all()
        
        # Get all liabilities
        liabilities = session.exec(select(Liability)).all()
        
        # Calculate totals
        total_assets = sum(asset.value for asset in assets)
        total_liabilities = sum(liability.value for liability in liabilities)
        net_worth = total_assets - total_liabilities
        
        return {
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "net_worth": round(net_worth, 2),
            "asset_count": len(assets),
            "liability_count": len(liabilities),
            "generated_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_assets_by_type(session: Session, asset_type: AssetType) -> Dict:
        """Get assets filtered by type."""
        assets = session.exec(
            select(Asset).where(Asset.asset_type == asset_type)
        ).all()
        
        total_value = sum(asset.value for asset in assets)
        
        return {
            "asset_type": asset_type.value,
            "total_value": round(total_value, 2),
            "count": len(assets),
            "items": [
                {
                    "id": asset.id,
                    "name": asset.name,
                    "value": round(asset.value, 2)
                }
                for asset in assets
            ]
        }

    @staticmethod
    def get_liabilities_by_type(session: Session, liability_type: LiabilityType) -> Dict:
        """Get liabilities filtered by type."""
        liabilities = session.exec(
            select(Liability).where(Liability.liability_type == liability_type)
        ).all()
        
        total_value = sum(liability.value for liability in liabilities)
        
        return {
            "liability_type": liability_type.value,
            "total_value": round(total_value, 2),
            "count": len(liabilities),
            "items": [
                {
                    "id": liability.id,
                    "name": liability.name,
                    "value": round(liability.value, 2)
                }
                for liability in liabilities
            ]
        }

    # ==================== Helper Methods ====================

    @staticmethod
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

    @staticmethod
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
