"""
Predictive work order tracking and maintenance calendar models.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class WorkOrder(BaseModel):
    id: str
    asset_id: str
    asset_name: str
    location: str
    title: str
    priority: str          # Critical, High, Medium, Low
    status: str            # Open, Assigned, In Progress, Completed, Overdue
    assigned_to: str       # e.g., "Thermal Systems Team - Mark Vance", "Controls Specialist - Sarah Chen"
    team: str              # Mechanical, Electrical, HVAC, Security, Controls
    created_date: str
    due_date: str
    completed_date: Optional[str] = None
    estimated_hours: float
    actual_hours: Optional[float] = None
    estimated_cost_usd: float
    maintenance_action: str
    ai_trigger_reason: str
    source_alert_id: Optional[str] = None
