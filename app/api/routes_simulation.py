"""
API routes for scenario injection and simulator control.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.engine.simulator import simulator_instance
from app.engine.scenarios import AVAILABLE_SCENARIOS

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

class ScenarioInjectRequest(BaseModel):
    scenario_id: str

@router.get("/scenarios")
def get_available_scenarios():
    return {
        "active_scenario": simulator_instance.active_scenario,
        "scenarios": AVAILABLE_SCENARIOS
    }

@router.post("/inject")
def inject_scenario(req: ScenarioInjectRequest):
    return simulator_instance.inject_scenario(req.scenario_id)

@router.post("/step")
def step_simulation():
    simulator_instance.step_simulation()
    return simulator_instance.get_overview()
