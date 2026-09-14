"""
API routes for facility intelligence reports.
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.engine.reporter import reporting_engine
from app.models.reports import FacilityReport

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/generate", response_model=FacilityReport)
def generate_report(period: str = Query("Last 24 Hours", description="Reporting period")):
    return reporting_engine.generate_full_report(period=period)
