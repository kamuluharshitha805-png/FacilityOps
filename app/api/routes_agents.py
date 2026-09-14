"""
API routes for autonomous AI agents, insights, and cross-agent orchestrations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.engine.simulator import simulator_instance
from app.models.agents import AgentStatus, AIInsight, CrossAgentCorrelation

router = APIRouter(prefix="/api/agents", tags=["agents"])

class RecommendationActionRequest(BaseModel):
    insight_id: str

@router.get("/status", response_model=List[AgentStatus])
def get_agents_status():
    return [
        simulator_instance.energy_agent.get_status(),
        simulator_instance.maint_agent.get_status(),
        simulator_instance.occupancy_agent.get_status(),
        simulator_instance.security_agent.get_status(),
        simulator_instance.cost_agent.get_status()
    ]

@router.get("/insights", response_model=List[AIInsight])
def get_all_insights():
    return simulator_instance.orchestrator.get_all_insights()

@router.get("/correlations", response_model=List[CrossAgentCorrelation])
def get_cross_agent_correlations():
    return simulator_instance.orchestrator.active_correlations

@router.post("/execute-recommendation")
def execute_recommendation(req: RecommendationActionRequest):
    res = simulator_instance.execute_recommendation(req.insight_id)
    if res.get("status") == "error":
        raise HTTPException(status_code=400, detail=res.get("message"))
    return res

@router.get("/energy")
def get_energy_agent_details():
    ea = simulator_instance.energy_agent
    return {
        "kpis": ea.get_kpis(),
        "hourly_history": ea.hourly_history,
        "daily_history": ea.daily_history,
        "insights": ea.active_insights
    }

@router.get("/maintenance")
def get_maintenance_agent_details():
    ma = simulator_instance.maint_agent
    return {
        "kpis": ma.get_kpis(list(simulator_instance.assets.values())),
        "insights": ma.active_insights
    }

@router.get("/occupancy")
def get_occupancy_agent_details():
    oa = simulator_instance.occupancy_agent
    return {
        "kpis": oa.get_kpis(list(simulator_instance.zones.values())),
        "insights": oa.active_insights
    }

@router.get("/security")
def get_security_agent_details():
    sa = simulator_instance.security_agent
    return {
        "kpis": sa.get_kpis(),
        "insights": sa.active_insights
    }

@router.get("/cost")
def get_cost_agent_details():
    ca = simulator_instance.cost_agent
    return {
        "kpis": ca.get_kpis(),
        "insights": ca.active_insights
    }

@router.get("/executive-overview")
def get_executive_overview():
    return simulator_instance.orchestrator.get_executive_overview()
