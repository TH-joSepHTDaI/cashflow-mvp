from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models import Liability
from app.schemas import LiabilityCreate, LiabilityRead, LiabilityUpdate

router = APIRouter(prefix="/api/liabilities", tags=["liabilities"])


@router.post("/", response_model=LiabilityRead, status_code=201)
def create_liability(liability: LiabilityCreate, session: Session = Depends(get_session)):
    """Create a new liability."""
    db_liability = Liability.model_validate(liability.model_dump())
    session.add(db_liability)
    session.commit()
    session.refresh(db_liability)
    return db_liability


@router.get("/", response_model=List[LiabilityRead])
def list_liabilities(session: Session = Depends(get_session)):
    """List all liabilities."""
    liabilities = session.exec(select(Liability)).all()
    return liabilities


@router.get("/{liability_id}", response_model=LiabilityRead)
def get_liability(liability_id: int, session: Session = Depends(get_session)):
    """Get a liability by ID."""
    liability = session.get(Liability, liability_id)
    if not liability:
        raise HTTPException(status_code=404, detail="Liability not found")
    return liability


@router.put("/{liability_id}", response_model=LiabilityRead)
def update_liability(
    liability_id: int,
    liability_update: LiabilityUpdate,
    session: Session = Depends(get_session)
):
    """Update a liability."""
    db_liability = session.get(Liability, liability_id)
    if not db_liability:
        raise HTTPException(status_code=404, detail="Liability not found")
    
    # Update only provided fields
    update_data = liability_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_liability, key, value)
    
    session.add(db_liability)
    session.commit()
    session.refresh(db_liability)
    return db_liability


@router.delete("/{liability_id}", status_code=204)
def delete_liability(liability_id: int, session: Session = Depends(get_session)):
    """Delete a liability."""
    liability = session.get(Liability, liability_id)
    if not liability:
        raise HTTPException(status_code=404, detail="Liability not found")
    
    session.delete(liability)
    session.commit()
    return None
