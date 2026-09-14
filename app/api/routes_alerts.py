"""
API routes for Central Alert Management.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.engine.simulator import simulator_instance
from app.models.alerts import FacilityAlert

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

class AcknowledgeRequest(BaseModel):
    user: str = "Facility Commander"

@router.get("", response_model=List[FacilityAlert])
def get_alerts(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None
):
    alerts = simulator_instance.orchestrator.get_all_alerts()
    if category and category != "All":
        alerts = [a for a in alerts if a.category.lower() == category.lower()]
    if severity and severity != "All":
        alerts = [a for a in alerts if a.severity.lower() == severity.lower()]
    if status and status != "All":
        alerts = [a for a in alerts if a.status.lower() == status.lower()]
    return alerts

@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, req: AcknowledgeRequest):
    alerts = simulator_instance.orchestrator.get_all_alerts()
    for a in alerts:
        if a.id == alert_id:
            a.status = "In Progress"
            a.acknowledged_by = req.user
            a.acknowledged_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {"status": "success", "alert": a}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

@router.post("/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    alerts = simulator_instance.orchestrator.get_all_alerts()
    for a in alerts:
        if a.id == alert_id:
            a.status = "Resolved"
            a.resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {"status": "success", "alert": a}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
