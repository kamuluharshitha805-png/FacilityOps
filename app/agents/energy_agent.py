"""
Energy Intelligence Agent for FacilityOps.
Monitors electrical, water, HVAC, and utility telemetry to optimize energy,
detect anomalies, track carbon footprint, and generate actionable savings recommendations.
"""

from typing import Dict, Any, List, Optional
import math
import random
import time
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.config import TARIFF_CONFIG, FACILITY_ZONES

class EnergyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="agt_energy_01",
            name="Energy Intelligence Agent",
            role="Autonomous Utility, HVAC & Carbon Optimization"
        )
        self.current_kw = 1240.0
        self.peak_demand_kw = 1480.0
        self.daily_kwh = 16840.0
        self.water_flow_gpm = 34.5
        self.daily_water_gal = 18450.0
        self.daily_carbon_kg = 6483.4
        self.hvac_total_kw = 680.0
        self.lighting_total_kw = 230.0
        self.equipment_total_kw = 330.0
        self.energy_score = 88.5
        self.potential_savings_usd = 4250.0
        self.realized_savings_usd = 1820.0
        
        # History buffers for charts
        self.hourly_history: List[Dict[str, Any]] = self._init_hourly_history()
        self.daily_history: List[Dict[str, Any]] = self._init_daily_history()
        
        # Water leak detection states
        self.water_leak_detected = False
        self.water_leak_zone = None

        # Seed initial insights
        self._seed_initial_insights()

    def _init_hourly_history(self) -> List[Dict[str, Any]]:
        points = []
        now_hour = 13  # 1 PM
        for i in range(24):
            hr = (now_hour - 23 + i) % 24
            base_kw = 600 + 700 * math.sin(max(0, (hr - 6)) / 12 * math.pi) if 6 <= hr <= 20 else 550 + random.uniform(-30, 30)
            cooling_kw = base_kw * 0.52
            lighting_kw = base_kw * 0.22
            plug_kw = base_kw * 0.26
            water_gpm = 15 + 30 * math.sin(max(0, (hr - 7)) / 10 * math.pi) if 7 <= hr <= 19 else 6 + random.uniform(-1, 2)
            points.append({
                "time": f"{hr:02d}:00",
                "total_kw": round(base_kw, 1),
                "hvac_kw": round(cooling_kw, 1),
                "lighting_kw": round(lighting_kw, 1),
                "equipment_kw": round(plug_kw, 1),
                "water_gpm": round(water_gpm, 1),
                "carbon_kg": round(base_kw * TARIFF_CONFIG["carbon_kg_per_kwh"], 1)
            })
        return points

    def _init_daily_history(self) -> List[Dict[str, Any]]:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        history = []
        for d in days:
            is_weekend = d in ["Sat", "Sun"]
            kwh = 24500.0 if not is_weekend else 11200.0
            history.append({
                "day": d,
                "kwh": kwh,
                "cost_usd": round(kwh * 0.165, 2),
                "carbon_kg": round(kwh * TARIFF_CONFIG["carbon_kg_per_kwh"], 1),
                "water_gal": 22000.0 if not is_weekend else 7500.0
            })
        return history

    def _seed_initial_insights(self):
        self.create_insight(
            title="HVAC Static Pressure Setback Optimization",
            category="HVAC Optimization",
            insight="AHU-F3-01 and AHU-F3-02 supply duct static pressure is operating at 1.8 in. w.g. despite variable-air volume boxes averaging only 42% open.",
            why="Static pressure reset schedule in BMS has a fixed minimum floor rather than dynamic trim-and-respond logic.",
            risk="Excess fan motor kilowatt draw increases thermal heat gain in ductwork, wasting 28 kWh/day and generating $860/mo unnecessary utility cost.",
            recommendation="Enable Trim-and-Respond dynamic static pressure setback logic to lower duct setpoint from 1.8 to 1.3 in. w.g.",
            impact="Reduces fan energy consumption by 24%, saving ~$860/month with zero disruption to thermal comfort.",
            priority="Medium",
            action_label="Apply Dynamic Pressure Reset",
            action_type="hvac_setpoint",
            estimated_savings_usd=860.0,
            action_params={"ahu_ids": ["AHU-F3-01", "AHU-F3-02"], "target_pressure": 1.3}
        )

        self.create_insight(
            title="Off-Peak Pre-Cooling & Chiller Staging Opportunity",
            category="Demand Shaving",
            insight="Upcoming weather and occupancy models predict afternoon temperature reaching 31°C with 88% building occupancy between 13:00 - 16:00.",
            why="Grid tariff jumps to peak demand pricing ($0.245/kWh + $18/kW demand charge) from 12:00 to 18:00.",
            risk="Unmanaged chiller ramp will trigger a new monthly peak demand penalty of ~1,680 kW, incurring $5,400 in demand charges.",
            recommendation="Pre-cool thermal mass of Floors 2-4 by 1.2°C between 06:30 - 08:30 during low-cost tariff ($0.098/kWh), then ramp down Chiller 2 during peak hours.",
            impact="Avoids 140 kW of peak demand spike and trims $3,200 in monthly electric utility charges.",
            priority="High",
            action_label="Activate Pre-Cooling Strategy",
            action_type="peak_shave",
            estimated_savings_usd=3200.0,
            action_params={"pre_cool_delta": 1.2, "peak_limit_kw": 1450.0}
        )

    def process_telemetry(self, zone_telemetries: List[Dict[str, Any]], asset_telemetries: List[Dict[str, Any]]):
        start = time.time()
        self.status = "Analyzing"
        self.telemetry_points_processed += len(zone_telemetries) + len(asset_telemetries)

        # Aggregate loads
        total_zone_kw = sum(z.get("power_draw_kw", 0.0) for z in zone_telemetries)
        hvac_assets_kw = sum(a.get("current_kw", 0.0) for a in asset_telemetries if a.get("type") in ["Chiller", "Boiler", "CoolingTower", "Pump", "AHU", "CRAC"])
        lighting_kw = sum(z.get("power_draw_kw", 0.0) * (z.get("lighting_pct", 50.0) / 100.0) * 0.35 for z in zone_telemetries)
        equipment_kw = max(100.0, total_zone_kw - lighting_kw)

        self.hvac_total_kw = round(hvac_assets_kw, 1)
        self.lighting_total_kw = round(lighting_kw, 1)
        self.equipment_total_kw = round(equipment_kw, 1)
        self.current_kw = round(self.hvac_total_kw + self.lighting_total_kw + self.equipment_total_kw, 1)

        if self.current_kw > self.peak_demand_kw:
            self.peak_demand_kw = self.current_kw

        # Update running daily counters
        self.daily_kwh += (self.current_kw / 3600.0) * 2.0  # scaled simulation increment
        self.daily_carbon_kg = round(self.daily_kwh * TARIFF_CONFIG["carbon_kg_per_kwh"], 1)

        # Calculate efficiency score based on baseline
        cop_readings = [a.get("current_cop", 4.5) for a in asset_telemetries if a.get("type") in ["Chiller", "AHU", "CRAC"]]
        avg_cop = sum(cop_readings) / max(1, len(cop_readings))
        cop_efficiency_ratio = min(1.0, avg_cop / 5.2)

        # Base energy score
        self.energy_score = round(max(50.0, min(99.0, 70.0 + cop_efficiency_ratio * 25.0 - (self.current_kw / self.peak_demand_kw) * 5.0)), 1)

        # Anomaly detection: Water flow
        if self.water_flow_gpm > 65.0:
            if not self.water_leak_detected:
                self.water_leak_detected = True
                self.create_alert(
                    category="Energy",
                    severity="High",
                    location="Zone Z-F5-04 Cooling Tower Make-Up Ingress",
                    title="Abnormal Water Flow & Potential Hydraulic Leakage",
                    description=f"Water consumption spiked to {self.water_flow_gpm:.1f} GPM (+165% above expected diurnal baseline).",
                    ai_explanation="Flow sensor MTR-WATER-ROOF shows non-pulsed continuous draw exceeding make-up water replenishment rates.",
                    recommended_action="Inspect cooling tower basin float valve and secondary bypass loops for mechanical overflow or rupture.",
                    action_data={"flow_gpm": self.water_flow_gpm, "valve_tag": "CT-VLV-04"}
                )
        else:
            self.water_leak_detected = False

        self.last_latency_ms = (time.time() - start) * 1000
        self.status = "Active"
        self.last_reasoning_summary = f"Monitoring {len(zone_telemetries)} zones & {len(asset_telemetries)} assets. Power: {self.current_kw} kW. Score: {self.energy_score}."

    def get_energy_distribution(self) -> Dict[str, float]:
        return {
            "HVAC & Cooling": round(self.hvac_total_kw, 1),
            "Lighting & Façade": round(self.lighting_total_kw, 1),
            "Data Center & IT Loads": round(self.equipment_total_kw * 0.65, 1),
            "Pumps & Hydronic Auxiliaries": round(self.equipment_total_kw * 0.20, 1),
            "Plug Loads & Other Utilities": round(self.equipment_total_kw * 0.15, 1)
        }

    def get_kpis(self) -> Dict[str, Any]:
        return {
            "total_power_kw": self.current_kw,
            "peak_demand_kw": self.peak_demand_kw,
            "daily_energy_kwh": round(self.daily_kwh, 1),
            "daily_carbon_kg": round(self.daily_carbon_kg, 1),
            "water_flow_gpm": round(self.water_flow_gpm, 1),
            "daily_water_gal": round(self.daily_water_gal, 1),
            "energy_efficiency_score": self.energy_score,
            "hvac_energy_kw": self.hvac_total_kw,
            "potential_savings_usd": self.potential_savings_usd,
            "realized_savings_usd": self.realized_savings_usd,
            "energy_distribution": self.get_energy_distribution()
        }
