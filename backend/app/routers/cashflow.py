from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional

from app.database import get_session
from app.services import ReportService

router = APIRouter(prefix="/api/cashflow", tags=["cashflow"])


@router.get("/monthly/range")
def get_cashflow_range(
    start_month: str = Query(..., description="Start month (YYYY-MM)"),
    end_month: str = Query(..., description="End month (YYYY-MM)"),
    session: Session = Depends(get_session)
):
    """Get cashflow summaries for a range of months."""
    result, error = ReportService.get_cashflow_range(session, start_month, end_month)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


@router.get("/monthly/{year_month}")
def get_monthly_cashflow(
    year_month: str,
    session: Session = Depends(get_session)
):
    """Get cashflow summary for a specific month. Format: YYYY-MM (e.g., 2024-01)"""
    result, error = ReportService.get_monthly_cashflow(session, year_month)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


@router.get("/summary")
def get_cashflow_summary(
    month: Optional[str] = Query(None, description="Month (YYYY-MM), defaults to current month"),
    session: Session = Depends(get_session)
):
    """Get a brief cashflow summary for a month."""
    result, error = ReportService.get_cashflow_summary(session, month)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


@router.get("/by-category/{year_month}")
def get_cashflow_by_category(
    year_month: str,
    session: Session = Depends(get_session)
):
    """Get cashflow grouped by category for a specific month."""
    result, error = ReportService.get_cashflow_by_category(session, year_month)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result
