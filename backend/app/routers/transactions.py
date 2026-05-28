from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional

from app.database import get_session
from app.schemas import TransactionCreate, TransactionRead, TransactionUpdate
from app.services import TransactionService

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead, status_code=201)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)):
    """Create a new transaction with automatic classification."""
    return TransactionService.create_transaction(session, transaction)


@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    month: Optional[str] = Query(None, description="Filter by month (YYYY-MM)"),
    session: Session = Depends(get_session)
):
    """List all transactions, optionally filtered by month."""
    transactions, error = TransactionService.list_transactions(session, month)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return transactions


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Get a transaction by ID."""
    transaction = TransactionService.get_transaction(session, transaction_id)
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
    transaction = TransactionService.update_transaction(
        session, transaction_id, transaction_update
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Delete a transaction."""
    deleted = TransactionService.delete_transaction(session, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None
