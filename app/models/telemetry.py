"""
Telemetry data models for sensors, equipment, zones, and building facilities.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ZoneTelemetry(BaseModel):
    id: str
    floor: int
    name: str
    type: str
    security: str
    area_sqft: int
    capacity: int
    current_occupancy: int
    occupancy_rate: float
    temperature_c: float
    target_temperature_c: float
    humidity_pct: float
    co2_ppm: float
    power_draw_kw: float
    hvac_status: str  # Normal, Eco, Boost, Standby, Offline
    lighting_pct: float
    motion_detected: bool
    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None

class AssetTelemetry(BaseModel):
    id: str
    name: str
    type: str
    zone_id: str
    criticality: str
    rated_kw: float
    current_kw: float
    rated_cop: float
    current_cop: float
    vibration_rms: float  # mm/s
    baseline_vibration: float
    temperature_c: float
    baseline_temperature: float
    pressure_psi: Optional[float] = None
    running_hours: float
    health_score: float  # 0 to 100
    health_status: str  # Healthy, Good, Warning, Critical
    failure_probability_pct: float  # 0 to 100%
    failure_window_days: Optional[int] = None
    rul_hours: float  # Remaining useful life
    mtbf_hours: float
    mttr_hours: float
    contributing_factors: List[str] = []
    is_anomalous: bool = False

class SubScores(BaseModel):
    energy: float
    maintenance: float
    occupancy: float
    security: float
    cost: float
    sustainability: float

class FacilityOverviewTelemetry(BaseModel):
    timestamp: str
    simulation_time: str
    building_name: str
    facility_health_score: float
    sub_scores: SubScores
    
    # Real-Time Operational Overview
    total_power_kw: float
    peak_demand_kw: float
    daily_energy_kwh: float
    total_water_gpm: float
    daily_water_gal: float
    daily_carbon_kg: float
    daily_operating_cost: float
    current_occupancy: int
    occupancy_rate: float
    
    # Assets status counts
    total_assets: int
    healthy_assets: int
    good_assets: int
    warning_assets: int
    critical_assets: int
    
    # Live counts
    active_alerts_count: int
    active_security_events_count: int
    open_work_orders_count: int
    prevented_failures_count: int
    estimated_monthly_savings_usd: float

    # Energy Distribution Breakdown (kW)
    energy_distribution: Dict[str, float]
    # Cost Distribution Breakdown ($)
    cost_distribution: Dict[str, float]
