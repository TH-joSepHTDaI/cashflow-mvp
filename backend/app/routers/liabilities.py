from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas import LiabilityCreate, LiabilityRead, LiabilityUpdate
from app.services import LiabilityService

router = APIRouter(prefix="/api/liabilities", tags=["liabilities"])


@router.post("/", response_model=LiabilityRead, status_code=201)
def create_liability(liability: LiabilityCreate, session: Session = Depends(get_session)):
    """Create a new liability."""
    return LiabilityService.create_liability(session, liability)


@router.get("/", response_model=List[LiabilityRead])
def list_liabilities(session: Session = Depends(get_session)):
    """List all liabilities."""
    return LiabilityService.list_liabilities(session)


@router.get("/{liability_id}", response_model=LiabilityRead)
def get_liability(liability_id: int, session: Session = Depends(get_session)):
    """Get a liability by ID."""
    liability = LiabilityService.get_liability(session, liability_id)
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
    liability = LiabilityService.update_liability(session, liability_id, liability_update)
    if not liability:
        raise HTTPException(status_code=404, detail="Liability not found")
    return liability


@router.delete("/{liability_id}", status_code=204)
def delete_liability(liability_id: int, session: Session = Depends(get_session)):
    """Delete a liability."""
    deleted = LiabilityService.delete_liability(session, liability_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Liability not found")
    return None
