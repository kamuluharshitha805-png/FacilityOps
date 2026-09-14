"""
Cost Optimization Agent for FacilityOps.
Translates operational and telemetry data into executive financial intelligence,
tracks utility and maintenance expenditures, models ROI, and prioritizes savings actions.
"""

from typing import Dict, Any, List, Optional
import math
import random
import time
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.config import TARIFF_CONFIG

class CostAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="agt_cost_05",
            name="Cost Optimization Agent",
            role="Autonomous Financial Analytics, Tariff Optimization & ROI Modeling"
        )
        self.daily_energy_cost = 2780.0
        self.daily_maintenance_cost = 620.0
        self.daily_water_cost = 101.5
        self.daily_operations_cost = 1450.0
        self.daily_equipment_depreciation = 940.0
        self.daily_other_cost = 320.0
        
        self.total_daily_operating_cost = round(
            self.daily_energy_cost + self.daily_maintenance_cost + self.daily_water_cost + 
            self.daily_operations_cost + self.daily_equipment_depreciation + self.daily_other_cost, 2
        )
        self.monthly_realized_savings = 14850.0
        self.monthly_potential_savings = 28400.0
        self.cost_efficiency_score = 86.4
        self.sustainability_score = 91.0
        self.resource_utilization_pct = 78.5

        # Seed initial financial insight
        self._seed_initial_insights()

    def _seed_initial_insights(self):
        self.create_insight(
            title="Transformer Redundancy Load-Balancing & Losses",
            category="Energy Cost",
            insight="Main Step-Down Transformer XFMR-01 is operating at 82% rated capacity while redundant unit XFMR-02 operates at only 12% no-load standby.",
            why="Unbalanced loading increases I²R copper core winding losses exponentially on XFMR-01 ($410/mo wasted heat dissipation).",
            risk="Accelerates insulation thermal degradation, reducing transformer remaining life by an estimated 4.5 years.",
            recommendation="Auto-transfer 35% of secondary feeder breakers to XFMR-02 to balance loads at 47% each, running at peak transformer efficiency curve.",
            impact="Reduces parasitic electrical heat loss by 18,500 kWh/year, yielding $3,050/yr direct electricity cost savings.",
            priority="Low",
            action_label="Balance Transformer Feeder Load",
            action_type="dispatch_maint",
            estimated_savings_usd=3050.0,
            action_params={"source_xfmr": "XFMR-01", "target_xfmr": "XFMR-02", "transfer_pct": 35}
        )

    def process_telemetry(self, daily_kwh: float, daily_water_gal: float, open_wos: int, prevented_failures: int):
        start = time.time()
        self.status = "Analyzing"
        self.telemetry_points_processed += 1

        # Dynamic tariff calculation
        current_hour = datetime.now().hour
        if 12 <= current_hour <= 18:
            rate = TARIFF_CONFIG["peak_kwh_rate"]
        elif 8 <= current_hour < 12 or 18 < current_hour <= 22:
            rate = TARIFF_CONFIG["standard_kwh_rate"]
        else:
            rate = TARIFF_CONFIG["offpeak_kwh_rate"]

        self.daily_energy_cost = round(daily_kwh * rate, 2)
        self.daily_water_cost = round(daily_water_gal * TARIFF_CONFIG["water_rate_per_gal"], 2)
        self.daily_maintenance_cost = round(450.0 + (open_wos * 85.0), 2)
        
        self.total_daily_operating_cost = round(
            self.daily_energy_cost + self.daily_maintenance_cost + self.daily_water_cost + 
            self.daily_operations_cost + self.daily_equipment_depreciation + self.daily_other_cost, 2
        )

        # Efficiency calculation
        baseline_expected = 7200.0
        ratio = self.total_daily_operating_cost / baseline_expected
        self.cost_efficiency_score = round(max(55.0, min(99.0, 100.0 - (ratio - 0.75) * 40.0)), 1)
        
        # Sustainability score calculation based on carbon and water
        carbon_factor = daily_kwh * TARIFF_CONFIG["carbon_kg_per_kwh"]
        self.sustainability_score = round(max(60.0, min(99.0, 95.0 - (carbon_factor / 15000.0) * 10.0)), 1)

        self.last_latency_ms = (time.time() - start) * 1000
        self.status = "Active"
        self.last_reasoning_summary = f"Daily Run Cost: ${self.total_daily_operating_cost:,.2f}. Cost Efficiency: {self.cost_efficiency_score}%. Sustainability: {self.sustainability_score}%."

    def get_cost_distribution(self) -> Dict[str, float]:
        return {
            "Energy & Electricity": self.daily_energy_cost,
            "Predictive & Planned Maintenance": self.daily_maintenance_cost,
            "Municipal Water & Utilities": self.daily_water_cost,
            "Facility Operations & Staffing": self.daily_operations_cost,
            "Capital Asset Depreciation": self.daily_equipment_depreciation,
            "Consumables & Other": self.daily_other_cost
        }

    def get_kpis(self) -> Dict[str, Any]:
        return {
            "total_operating_cost": self.total_daily_operating_cost,
            "daily_energy_cost": self.daily_energy_cost,
            "daily_maintenance_cost": self.daily_maintenance_cost,
            "daily_water_cost": self.daily_water_cost,
            "monthly_realized_savings": self.monthly_realized_savings,
            "monthly_potential_savings": self.monthly_potential_savings,
            "cost_efficiency_score": self.cost_efficiency_score,
            "sustainability_score": self.sustainability_score,
            "resource_utilization_pct": self.resource_utilization_pct,
            "cost_distribution": self.get_cost_distribution(),
            "carbon_emissions_kg": round(self.daily_energy_cost / 0.165 * TARIFF_CONFIG["carbon_kg_per_kwh"], 1)
        }
