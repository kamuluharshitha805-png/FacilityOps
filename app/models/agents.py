"""
Agent state, AI insights, recommendations, and cross-agent correlation models.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class AgentStatus(BaseModel):
    id: str
    name: str
    role: str
    status: str  # Active, Ingesting, Analyzing, Correlating, Optimizing
    health_rating: str  # Nominal, Degraded, Busy
    latency_ms: float
    telemetry_points_processed: int
    alerts_generated: int
    recommendations_generated: int
    active_insights_count: int
    last_reasoning_summary: str
    last_updated: str

class AIInsight(BaseModel):
    id: str
    title: str
    agent_source: str  # Energy, Maintenance, Occupancy, Security, Cost, Cross-Agent Orchestration
    category: str
    
    # 5-Pillar Explainable AI Architecture
    insight: str         # What happened?
    why: str             # Why did it happen?
    risk: str            # What happens if no action is taken?
    recommendation: str  # What should be done?
    impact: str          # What is the expected benefit?
    
    priority: str        # Critical, High, Medium, Low
    estimated_savings_usd: Optional[float] = 0.0
    action_label: str    # e.g., "Adjust Setpoint", "Dispatch Technician", "Trigger Lockdown"
    action_type: str     # hvac_setpoint, dispatch_maint, security_alert, schedule_adjust, peak_shave
    action_params: Optional[Dict[str, Any]] = None
    timestamp: str
    is_executed: bool = False
    executed_at: Optional[str] = None

class CrossAgentCorrelation(BaseModel):
    id: str
    pair: str  # e.g. "ENERGY ↔ MAINTENANCE", "OCCUPANCY ↔ SECURITY", etc.
    agent_a: str
    agent_b: str
    event_a: str
    event_b: str
    correlation_rule: str
    ai_reasoning: str
    confidence_pct: float
    recommended_unified_action: str
    financial_or_risk_impact: str
    timestamp: str
    active: bool = True
