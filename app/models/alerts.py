"""
Central alert models and severity classifications for FacilityOps.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class FacilityAlert(BaseModel):
    id: str
    category: str        # Energy, Maintenance, Occupancy, Security, Cost, Facility Critical
    severity: str        # Information, Low, Medium, High, Critical
    timestamp: str
    location: str        # Floor / Zone / Asset
    source_agent: str    # Energy Agent, Predictive Maintenance Agent, Occupancy Agent, Security Agent, Cost Agent, Orchestrator
    title: str
    description: str
    ai_explanation: str
    recommended_action: str
    status: str          # Active, In Progress, Resolved
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[str] = None
    resolved_at: Optional[str] = None
    action_data: Optional[Dict[str, Any]] = None
