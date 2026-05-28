"""Transaction service - business logic for transactions."""

from datetime import date, datetime
from typing import List, Optional, Tuple
from sqlmodel import Session, select

from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate
from app.classifier import classify_transaction


class TransactionService:
    """Service for transaction business logic."""

    @staticmethod
    def create_transaction(
        session: Session,
        transaction_data: TransactionCreate
    ) -> Transaction:
        """Create a new transaction with automatic classification."""
        data = transaction_data.model_dump()
        
        # Auto-classify if cashflow_type is not provided or is OTHER
        if data.get("cashflow_type") == "other" or not data.get("cashflow_type"):
            data["cashflow_type"] = classify_transaction(
                data.get("note", ""),
                data.get("category", "")
            )
        
        db_transaction = Transaction.model_validate(data)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def list_transactions(
        session: Session,
        month: Optional[str] = None
    ) -> Tuple[List[Transaction], Optional[str]]:
        """
        List all transactions, optionally filtered by month.
        Returns (transactions, error_message).
        """
        query = select(Transaction)
        
        if month:
            # Parse month string (YYYY-MM) and filter by date range
            try:
                year, month_num = map(int, month.split("-"))
                start_date = date(year, month_num, 1)
                # Calculate end of month
                if month_num == 12:
                    end_date = date(year + 1, 1, 1)
                else:
                    end_date = date(year, month_num + 1, 1)
                query = query.where(Transaction.date >= start_date, Transaction.date < end_date)
            except ValueError:
                return [], "Invalid month format. Use YYYY-MM"
        
        transactions = session.exec(query).all()
        return list(transactions), None

    @staticmethod
    def get_transaction(session: Session, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by ID."""
        return session.get(Transaction, transaction_id)

    @staticmethod
    def update_transaction(
        session: Session,
        transaction_id: int,
        transaction_update: TransactionUpdate
    ) -> Optional[Transaction]:
        """Update a transaction. Returns None if not found."""
        db_transaction = session.get(Transaction, transaction_id)
        if not db_transaction:
            return None
        
        # Update only provided fields
        update_data = transaction_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        
        # Update the updated_at timestamp
        db_transaction.updated_at = datetime.utcnow()
        
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def delete_transaction(session: Session, transaction_id: int) -> bool:
        """Delete a transaction. Returns True if deleted, False if not found."""
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            return False
        
        session.delete(transaction)
        session.commit()
        return True
