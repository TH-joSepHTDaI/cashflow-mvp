from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models import AssetType, LiabilityType
from app.services import ReportService

router = APIRouter(prefix="/api/v1/balance-sheet", tags=["balance-sheet"])


@router.get("/")
def get_balance_sheet(session: Session = Depends(get_session)):
    """Get the complete balance sheet summary."""
    return ReportService.get_balance_sheet(session)


@router.get("/summary")
def get_balance_sheet_summary(session: Session = Depends(get_session)):
    """Get a brief balance sheet summary (totals only)."""
    return ReportService.get_balance_sheet_summary(session)


@router.get("/assets/by-type/{asset_type}")
def get_assets_by_type(asset_type: str, session: Session = Depends(get_session)):
    """Get assets filtered by type."""
    try:
        asset_type_enum = AssetType(asset_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid asset type. Valid types: {[t.value for t in AssetType]}"
        )
    return ReportService.get_assets_by_type(session, asset_type_enum)


@router.get("/liabilities/by-type/{liability_type}")
def get_liabilities_by_type(liability_type: str, session: Session = Depends(get_session)):
    """Get liabilities filtered by type."""
    try:
        liability_type_enum = LiabilityType(liability_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid liability type. Valid types: {[t.value for t in LiabilityType]}"
        )
    return ReportService.get_liabilities_by_type(session, liability_type_enum)
