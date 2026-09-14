"""
Real-time IoT Building Simulator for FacilityOps.
Simulates diurnal occupancy cycles, environmental thermodynamics, asset telemetry,
and drives continuous AI Agent execution with WebSocket streaming.
"""

import asyncio
import copy
import math
import random
import time
from datetime import datetime
from typing import Dict, Any, List, Set

from app.config import FACILITY_ZONES, ASSET_REGISTRY, TARIFF_CONFIG
from app.agents.energy_agent import EnergyAgent
from app.agents.maintenance_agent import MaintenanceAgent
from app.agents.occupancy_agent import OccupancyAgent
from app.agents.security_agent import SecurityAgent
from app.agents.cost_agent import CostAgent
from app.agents.orchestration import FacilityOrchestrator
from app.models.telemetry import ZoneTelemetry, AssetTelemetry, FacilityOverviewTelemetry, SubScores

class FacilitySimulator:
    def __init__(self):
        self.zones: Dict[str, Dict[str, Any]] = {}
        self.assets: Dict[str, Dict[str, Any]] = {}
        self.active_scenario: str = "scenario_reset_nominal"
        self.simulation_speed: float = 1.0
        self.is_running: bool = True
        self.listeners: Set[Any] = set()

        # Instantiate Autonomous Agents
        self.energy_agent = EnergyAgent()
        self.maint_agent = MaintenanceAgent()
        self.occupancy_agent = OccupancyAgent()
        self.security_agent = SecurityAgent()
        self.cost_agent = CostAgent()

        # Instantiate Central Orchestrator
        self.orchestrator = FacilityOrchestrator(
            energy_agent=self.energy_agent,
            maint_agent=self.maint_agent,
            occupancy_agent=self.occupancy_agent,
            security_agent=self.security_agent,
            cost_agent=self.cost_agent
        )

        self._init_data()

    def _init_data(self):
        # Initialize Zones
        for z in FACILITY_ZONES:
            zone_id = z["id"]
            fl = z["floor"]
            # Diurnal baseline occupancy
            base_occ = int(z["capacity"] * random.uniform(0.40, 0.75)) if z["type"] in ["Office", "Dining", "Lobby"] else int(z["capacity"] * 0.25)
            self.zones[zone_id] = {
                "id": zone_id,
                "floor": fl,
                "name": z["name"],
                "type": z["type"],
                "security": z["security"],
                "area_sqft": z["area_sqft"],
                "capacity": z["capacity"],
                "current_occupancy": max(0, base_occ),
                "occupancy_rate": round((base_occ / max(1, z["capacity"])) * 100, 1),
                "temperature_c": round(z["hvac_setpoint"] + random.uniform(-0.4, 0.4), 1),
                "target_temperature_c": z["hvac_setpoint"],
                "humidity_pct": round(random.uniform(46.0, 52.0), 1),
                "co2_ppm": round(450.0 + base_occ * 2.5, 0),
                "power_draw_kw": round((z["area_sqft"] / 1000.0) * random.uniform(1.8, 3.2), 1),
                "hvac_status": "Normal",
                "lighting_pct": 75.0 if base_occ > 0 else 20.0,
                "motion_detected": base_occ > 0,
                "is_anomaly": False,
                "anomaly_reason": None
            }

        # Initialize Assets
        for a in ASSET_REGISTRY:
            asset_id = a["id"]
            install_yr = a["install_year"]
            age_years = 2026 - install_yr
            base_hours = age_years * 4200.0 + random.uniform(500, 2000)
            
            # Initial condition calculation
            base_score = round(max(85.0, 98.0 - (age_years * 1.5) - random.uniform(0, 3)), 1)
            
            self.assets[asset_id] = {
                "id": asset_id,
                "name": a["name"],
                "type": a["type"],
                "zone_id": a["zone_id"],
                "criticality": a["criticality"],
                "rated_kw": a["rated_kw"],
                "current_kw": round(a["rated_kw"] * random.uniform(0.55, 0.80), 1) if a["rated_kw"] > 0 else 0.0,
                "rated_cop": a["rated_cop"],
                "current_cop": round(a["rated_cop"] * random.uniform(0.92, 0.98), 2),
                "vibration_rms": round(a["baseline_vibration"] + random.uniform(0.01, 0.05), 2),
                "baseline_vibration": a["baseline_vibration"],
                "temperature_c": round(a["baseline_temp"] + random.uniform(-1.0, 1.5), 1),
                "baseline_temperature": a["baseline_temp"],
                "pressure_psi": round(random.uniform(42.0, 58.0), 1) if a["type"] in ["Chiller", "Pump", "Boiler"] else None,
                "running_hours": round(base_hours, 1),
                "health_score": base_score,
                "health_status": "Healthy" if base_score >= 85 else "Good",
                "failure_probability_pct": round(max(2.0, 100.0 - base_score - 5.0), 1),
                "failure_window_days": None,
                "rul_hours": round(25000.0 - (base_hours % 10000), 0),
                "mtbf_hours": 4200.0,
                "mttr_hours": 3.2,
                "contributing_factors": ["Normal operational wear within ISO vibration standards"],
                "is_anomalous": False,
                "alert_generated": False
            }

    def inject_scenario(self, scenario_id: str) -> Dict[str, Any]:
        self.active_scenario = scenario_id

        if scenario_id == "scenario_chiller_overheat":
            # Degrade CH-02
            ch2 = self.assets.get("CH-02")
            if ch2:
                ch2["is_anomalous"] = True
                ch2["vibration_rms"] = 4.85
                ch2["temperature_c"] = 68.5
                ch2["current_kw"] = 432.0  # +120 kW over standard load
                ch2["current_cop"] = 3.6   # COP collapses
                ch2["health_score"] = 41.5 # Critical status
                ch2["health_status"] = "Critical"
                ch2["failure_probability_pct"] = 84.0
                ch2["failure_window_days"] = 4
                ch2["contributing_factors"] = [
                    "Drive-end bearing inner race spalling (BPFI peak harmonics)",
                    "Thermal rise of +18.5°C over calibrated baseline",
                    "Elevated compressor motor current draw (+28%)"
                ]
                ch2["alert_generated"] = False  # Allows trigger

        elif scenario_id == "scenario_restricted_breach":
            # Trigger breach in Data Center Alpha
            dc_zone = self.zones.get("Z-F5-01")
            if dc_zone:
                dc_zone["is_anomaly"] = True
                dc_zone["motion_detected"] = True
                dc_zone["current_occupancy"] = 2
                dc_zone["anomaly_reason"] = "Unregistered motion inside Tier-4 Data Center corridor."

        elif scenario_id == "scenario_water_leak":
            self.energy_agent.water_flow_gpm = 78.4
            roof_zone = self.zones.get("Z-F5-04")
            if roof_zone:
                roof_zone["is_anomaly"] = True
                roof_zone["anomaly_reason"] = "Cooling tower basin float sensor stuck open."

        elif scenario_id == "scenario_peak_demand_spike":
            self.energy_agent.current_kw = 1685.0
            self.energy_agent.peak_demand_kw = 1685.0

        elif scenario_id == "scenario_reset_nominal":
            # Restore all to pristine
            self._init_data()
            self.energy_agent.water_flow_gpm = 34.5

        # Immediately trigger agent evaluation
        self.step_simulation()

        return {
            "status": "success",
            "active_scenario": scenario_id,
            "facility_health_score": self.orchestrator.facility_health_score,
            "correlations_count": len(self.orchestrator.active_correlations),
            "alerts_count": len(self.orchestrator.get_all_alerts())
        }

    def execute_recommendation(self, insight_id: str) -> Dict[str, Any]:
        """User clicked action button on an AI insight card."""
        insights = self.orchestrator.get_all_insights()
        for ins in insights:
            if ins.id == insight_id:
                ins.is_executed = True
                ins.executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Apply action consequences
                if ins.action_type == "hvac_setpoint":
                    for z in self.zones.values():
                        if "pressure" in ins.action_label.lower():
                            z["power_draw_kw"] = round(z["power_draw_kw"] * 0.82, 1)
                        z["hvac_status"] = "Eco"

                elif ins.action_type == "dispatch_maint":
                    asset_id = ins.action_params.get("asset_id", "CH-02")
                    # Create automated work order
                    self.maint_agent.create_work_order({
                        "asset_id": asset_id,
                        "asset_name": self.assets.get(asset_id, {}).get("name", "Industrial Asset"),
                        "title": f"Predictive Overhaul: {ins.title}",
                        "priority": ins.priority,
                        "maintenance_action": ins.recommendation,
                        "ai_trigger_reason": ins.why
                    })
                    # Mitigate asset status
                    target = self.assets.get(asset_id)
                    if target:
                        target["health_score"] = 82.0
                        target["health_status"] = "Good"
                        target["vibration_rms"] = target["baseline_vibration"] * 1.1
                        target["temperature_c"] = target["baseline_temperature"] + 1.0

                elif ins.action_type == "security_alert":
                    zone_id = ins.action_params.get("zone_id", "Z-F5-01")
                    if zone_id in self.zones:
                        self.zones[zone_id]["motion_detected"] = False
                        self.zones[zone_id]["current_occupancy"] = 0
                        self.zones[zone_id]["is_anomaly"] = False

                elif ins.action_type == "peak_shave":
                    self.energy_agent.current_kw = round(self.energy_agent.current_kw * 0.88, 1)
                    self.energy_agent.realized_savings_usd += ins.estimated_savings_usd or 500.0

                self.step_simulation()
                return {"status": "executed", "insight": ins.model_dump()}

        return {"status": "error", "message": f"Insight {insight_id} not found"}

    def step_simulation(self):
        """Execute one simulation cycle."""
        # 1. Update zone physics (minor natural jitter)
        for z in self.zones.values():
            if not z.get("is_anomaly"):
                z["temperature_c"] = round(z["target_temperature_c"] + random.uniform(-0.2, 0.2), 1)
                z["humidity_pct"] = round(max(40.0, min(60.0, z["humidity_pct"] + random.uniform(-0.1, 0.1))), 1)

        # 2. Update asset telemetry
        for a in self.assets.values():
            if not a.get("is_anomalous"):
                a["vibration_rms"] = round(max(0.1, a["baseline_vibration"] + random.uniform(-0.02, 0.03)), 2)
                a["temperature_c"] = round(a["baseline_temperature"] + random.uniform(-0.4, 0.5), 1)
                a["running_hours"] += round(0.02 * self.simulation_speed, 2)

        # 3. Process telemetry across agents
        zone_list = list(self.zones.values())
        asset_list = list(self.assets.values())

        self.energy_agent.process_telemetry(zone_list, asset_list)
        self.maint_agent.process_telemetry(asset_list)
        self.occupancy_agent.process_telemetry(zone_list)
        self.security_agent.process_telemetry(zone_list)

        open_wos = sum(1 for wo in self.maint_agent.work_orders if wo.status in ["Open", "Assigned", "In Progress"])
        self.cost_agent.process_telemetry(
            daily_kwh=self.energy_agent.daily_kwh,
            daily_water_gal=self.energy_agent.daily_water_gal,
            open_wos=open_wos,
            prevented_failures=self.maint_agent.prevented_failures
        )

        # 4. Cross-Agent Orchestration
        self.orchestrator.evaluate_cross_agent_rules(zone_list, asset_list)
        self.orchestrator.compute_facility_health_score()

    def get_overview(self) -> FacilityOverviewTelemetry:
        health_dist = self.maint_agent.get_health_distribution(list(self.assets.values()))
        open_wos = sum(1 for wo in self.maint_agent.work_orders if wo.status in ["Open", "Assigned", "In Progress"])
        active_alerts = [a for a in self.orchestrator.get_all_alerts() if a.status == "Active"]
        
        return FacilityOverviewTelemetry(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            simulation_time=datetime.now().strftime("%H:%M:%S"),
            building_name="Apex Tower Global HQ",
            facility_health_score=self.orchestrator.facility_health_score,
            sub_scores=SubScores(
                energy=self.energy_agent.energy_score,
                maintenance=self.maint_agent.average_equipment_health,
                occupancy=self.occupancy_agent.space_utilization_score,
                security=self.security_agent.security_health_score,
                cost=self.cost_agent.cost_efficiency_score,
                sustainability=self.cost_agent.sustainability_score
            ),
            total_power_kw=self.energy_agent.current_kw,
            peak_demand_kw=self.energy_agent.peak_demand_kw,
            daily_energy_kwh=round(self.energy_agent.daily_kwh, 1),
            total_water_gpm=self.energy_agent.water_flow_gpm,
            daily_water_gal=round(self.energy_agent.daily_water_gal, 1),
            daily_carbon_kg=self.energy_agent.daily_carbon_kg,
            daily_operating_cost=self.cost_agent.total_daily_operating_cost,
            current_occupancy=self.occupancy_agent.current_occupancy,
            occupancy_rate=self.occupancy_agent.occupancy_rate,
            total_assets=len(self.assets),
            healthy_assets=health_dist["healthy"],
            good_assets=health_dist["good"],
            warning_assets=health_dist["warning"],
            critical_assets=health_dist["critical"],
            active_alerts_count=len(active_alerts),
            active_security_events_count=self.security_agent.active_security_events,
            open_work_orders_count=open_wos,
            prevented_failures_count=self.maint_agent.prevented_failures,
            estimated_monthly_savings_usd=sum(ins.estimated_savings_usd or 0 for ins in self.orchestrator.get_all_insights()),
            energy_distribution=self.energy_agent.get_energy_distribution(),
            cost_distribution=self.cost_agent.get_cost_distribution()
        )

# Global simulator instance singleton
simulator_instance = FacilitySimulator()
