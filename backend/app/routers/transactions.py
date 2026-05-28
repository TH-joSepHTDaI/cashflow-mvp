from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date

from app.database import get_session
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionRead, TransactionUpdate
from app.classifier import classify_transaction

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead, status_code=201)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)):
    """Create a new transaction with automatic classification."""
    # Auto-classify if cashflow_type is not provided or is OTHER
    transaction_data = transaction.model_dump()
    if transaction_data.get("cashflow_type") == "other" or not transaction_data.get("cashflow_type"):
        transaction_data["cashflow_type"] = classify_transaction(
            transaction_data.get("note", ""),
            transaction_data.get("category", "")
        )
    
    db_transaction = Transaction.model_validate(transaction_data)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    month: Optional[str] = Query(None, description="Filter by month (YYYY-MM)"),
    session: Session = Depends(get_session)
):
    """List all transactions, optionally filtered by month."""
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
            raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM")
    
    transactions = session.exec(query).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Get a transaction by ID."""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    session: Session = Depends(get_session)
):
    """Update a transaction."""
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Update only provided fields
    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Delete a transaction."""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    session.delete(transaction)
    session.commit()
    return None
