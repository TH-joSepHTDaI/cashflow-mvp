from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Dict, List
from datetime import datetime

from app.database import get_session
from app.models import Asset, Liability, AssetType, LiabilityType

router = APIRouter(prefix="/api/balance-sheet", tags=["balance-sheet"])


@router.get("/")
def get_balance_sheet(session: Session = Depends(get_session)):
    """
    Get the complete balance sheet summary.
    Returns total assets, total liabilities, and net worth.
    """
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
            "items": [
                {
                    "id": liability.id,
                    "name": liability.name,
                    "type": liability.liability_type.value,
                    "value": round(liability.value, 2)
                }
                for liability in liabilities
            ]
        },
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/summary")
def get_balance_sheet_summary(session: Session = Depends(get_session)):
    """
    Get a brief balance sheet summary (totals only).
    """
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


@router.get("/assets/by-type/{asset_type}")
def get_assets_by_type(asset_type: str, session: Session = Depends(get_session)):
    """
    Get assets filtered by type.
    """
    try:
        asset_type_enum = AssetType(asset_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid asset type. Valid types: {[t.value for t in AssetType]}"
        )
    
    assets = session.exec(
        select(Asset).where(Asset.asset_type == asset_type_enum)
    ).all()
    
    total_value = sum(asset.value for asset in assets)
    
    return {
        "asset_type": asset_type,
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


@router.get("/liabilities/by-type/{liability_type}")
def get_liabilities_by_type(liability_type: str, session: Session = Depends(get_session)):
    """
    Get liabilities filtered by type.
    """
    try:
        liability_type_enum = LiabilityType(liability_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid liability type. Valid types: {[t.value for t in LiabilityType]}"
        )
    
    liabilities = session.exec(
        select(Liability).where(Liability.liability_type == liability_type_enum)
    ).all()
    
    total_value = sum(liability.value for liability in liabilities)
    
    return {
        "liability_type": liability_type,
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
