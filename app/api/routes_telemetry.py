"""
API routes for facility, zone, and asset telemetry.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.engine.simulator import simulator_instance
from app.models.telemetry import FacilityOverviewTelemetry

router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])

@router.get("/overview", response_model=FacilityOverviewTelemetry)
def get_facility_overview():
    return simulator_instance.get_overview()

@router.get("/zones", response_model=List[Dict[str, Any]])
def get_zones():
    return list(simulator_instance.zones.values())

@router.get("/zones/{zone_id}")
def get_zone_detail(zone_id: str):
    zone = simulator_instance.zones.get(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {zone_id} not found")
    
    # Also attach assets located in this zone
    zone_assets = [a for a in simulator_instance.assets.values() if a.get("zone_id") == zone_id]
    return {
        "zone": zone,
        "assets": zone_assets
    }

@router.get("/assets", response_model=List[Dict[str, Any]])
def get_assets():
    return list(simulator_instance.assets.values())

@router.get("/assets/{asset_id}")
def get_asset_detail(asset_id: str):
    asset = simulator_instance.assets.get(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset {asset_id} not found")
    return asset
