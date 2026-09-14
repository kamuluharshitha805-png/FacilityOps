"""
Facility intelligence reporting schema.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class FacilityReport(BaseModel):
    report_id: str
    title: str
    generated_at: str
    period: str
    building_name: str
    facility_health_score: float
    
    executive_summary: Dict[str, Any]
    energy_intelligence: Dict[str, Any]
    predictive_maintenance: Dict[str, Any]
    occupancy_intelligence: Dict[str, Any]
    security_intelligence: Dict[str, Any]
    cost_optimization: Dict[str, Any]
    sustainability: Dict[str, Any]
    
    key_recommendations: List[Dict[str, Any]]
