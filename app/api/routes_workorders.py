"""
API routes for Predictive Work Order Management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.engine.simulator import simulator_instance
from app.models.work_orders import WorkOrder

router = APIRouter(prefix="/api/workorders", tags=["workorders"])

class WorkOrderCreateRequest(BaseModel):
    asset_id: str
    asset_name: str
    location: str
    title: str
    priority: str
    assigned_to: str
    team: str
    estimated_hours: float
    estimated_cost_usd: float
    maintenance_action: str
    ai_trigger_reason: str

class WorkOrderStatusUpdateRequest(BaseModel):
    status: str

@router.get("", response_model=List[WorkOrder])
def get_work_orders(status: Optional[str] = None):
    wos = simulator_instance.maint_agent.work_orders
    if status and status != "All":
        wos = [w for w in wos if w.status.lower() == status.lower()]
    return wos

@router.post("", response_model=WorkOrder)
def create_work_order(req: WorkOrderCreateRequest):
    new_wo = simulator_instance.maint_agent.create_work_order(req.model_dump())
    return new_wo

@router.post("/{wo_id}/status", response_model=WorkOrder)
def update_status(wo_id: str, req: WorkOrderStatusUpdateRequest):
    wo = simulator_instance.maint_agent.update_work_order_status(wo_id, req.status)
    if not wo:
        raise HTTPException(status_code=404, detail=f"Work Order {wo_id} not found")
    return wo
