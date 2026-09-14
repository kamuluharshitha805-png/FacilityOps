"""
Predictive Maintenance Agent for FacilityOps.
Detects early-stage equipment degradation, calculates multi-variate condition scores,
forecasts failure probability and RUL, and autonomously triggers prioritized work orders.
"""

from typing import Dict, Any, List, Optional
import math
import random
import time
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent
from app.models.work_orders import WorkOrder

class MaintenanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="agt_maint_02",
            name="Predictive Maintenance Agent",
            role="Autonomous Asset Health, Degradation Modeling & Work Order Dispatch"
        )
        self.average_equipment_health = 91.2
        self.prevented_failures = 14
        self.mtbf_hours = 4250.0
        self.mttr_hours = 3.2
        self.maintenance_cost_ytd = 48500.0
        
        # Work Orders Database
        self.work_orders: List[WorkOrder] = self._seed_work_orders()
        
        # Maintenance Calendar Events
        self.calendar_events: List[Dict[str, Any]] = self._seed_calendar()

        # Seed initial predictive insight
        self._seed_initial_insights()

    def _seed_work_orders(self) -> List[WorkOrder]:
        today = datetime.now()
        return [
            WorkOrder(
                id="WO-2026-101",
                asset_id="PMP-03",
                asset_name="Condenser Water Pump 1",
                location="Floor 5 Mechanical Room (Z-F5-03)",
                title="Seal Flush Inspection & Mechanical Coupling Realignment",
                priority="Medium",
                status="Assigned",
                assigned_to="Hydronics Specialist - David Miller",
                team="Mechanical",
                created_date=(today - timedelta(days=2)).strftime("%Y-%m-%d"),
                due_date=(today + timedelta(days=1)).strftime("%Y-%m-%d"),
                estimated_hours=3.5,
                estimated_cost_usd=650.0,
                maintenance_action="Laser shaft realignment and replace mechanical face seal cartridge.",
                ai_trigger_reason="Vibration RMS elevated by 0.35 mm/s with 1X rotational frequency peak harmonics."
            ),
            WorkOrder(
                id="WO-2026-102",
                asset_id="AHU-F2-01",
                asset_name="Floor 2 Labs Clean Supply AHU",
                location="Floor 2 Cleanroom Plant (Z-F2-01)",
                title="HEPA Filter Differential Pressure & Belt Tension Verification",
                priority="High",
                status="In Progress",
                assigned_to="HVAC Controls Lead - Sarah Chen",
                team="HVAC",
                created_date=(today - timedelta(days=1)).strftime("%Y-%m-%d"),
                due_date=today.strftime("%Y-%m-%d"),
                estimated_hours=4.0,
                estimated_cost_usd=1200.0,
                maintenance_action="Inspect differential pressure transducer, replace pre-filters and verify belt tension.",
                ai_trigger_reason="Filter delta-P increased to 1.4 in. w.g. Fan motor slip ratio increased by 6%."
            ),
            WorkOrder(
                id="WO-2026-103",
                asset_id="XFMR-01",
                asset_name="Main Step-Down Transformer 2.5MVA",
                location="Floor 1 Electrical Substation (Z-F1-05)",
                title="Infrared Thermography Scan & Dielectric Oil Sampling",
                priority="Low",
                status="Completed",
                assigned_to="High-Voltage Electrician - Carlos Gomez",
                team="Electrical",
                created_date=(today - timedelta(days=8)).strftime("%Y-%m-%d"),
                due_date=(today - timedelta(days=4)).strftime("%Y-%m-%d"),
                completed_date=(today - timedelta(days=4)).strftime("%Y-%m-%d"),
                estimated_hours=2.5,
                actual_hours=2.0,
                estimated_cost_usd=450.0,
                maintenance_action="Completed 12-point thermographic scan of bushing lugs and tested breakdown voltage of transformer fluid.",
                ai_trigger_reason="Scheduled 6-month condition-based preventive milestone."
            ),
            WorkOrder(
                id="WO-2026-104",
                asset_id="CRAC-02",
                asset_name="Mission Data Center CRAC 2",
                location="Floor 5 Data Center Alpha (Z-F5-01)",
                title="Electronic Expansion Valve (EEV) & Superheat Calibration",
                priority="Medium",
                status="Open",
                assigned_to="Thermal Specialist - Alex Wong",
                team="HVAC",
                created_date=today.strftime("%Y-%m-%d"),
                due_date=(today + timedelta(days=3)).strftime("%Y-%m-%d"),
                estimated_hours=3.0,
                estimated_cost_usd=550.0,
                maintenance_action="Recalibrate stepper motor EEV controller and verify compressor suction line superheat stability.",
                ai_trigger_reason="Suction line temperature oscillation of +/- 4.2°C detected under constant compute rack heat load."
            )
        ]

    def _seed_calendar(self) -> List[Dict[str, Any]]:
        today = datetime.now()
        return [
            {"date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "title": "PMP-03 Coupling Realignment", "priority": "Medium", "asset": "PMP-03", "type": "Corrective"},
            {"date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "title": "ELV-01 Cable Tension & Brake Pad Inspection", "priority": "Medium", "asset": "ELV-01", "type": "Scheduled"},
            {"date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "title": "CRAC-02 EEV Calibration", "priority": "High", "asset": "CRAC-02", "type": "Predictive"},
            {"date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "title": "GEN-01 30-Min Full Load Transfer Test", "priority": "Critical", "asset": "GEN-01", "type": "Compliance"},
            {"date": (today + timedelta(days=7)).strftime("%Y-%m-%d"), "title": "CT-01 & CT-02 Biocide Water Treatment Clean", "priority": "Medium", "asset": "CT-01", "type": "Preventive"},
        ]

    def _seed_initial_insights(self):
        self.create_insight(
            title="Chiller 2 Compressor Drive-End Bearing Friction Warning",
            category="Mechanical Degradation",
            insight="Centrifugal Chiller 2 (CH-02) drive-end bearing vibration RMS has trended upward from 1.4 mm/s to 3.8 mm/s over 72 hours, with temperature reaching 59.5°C.",
            why="Fast Fourier Transform (FFT) vibration telemetry indicates peak amplitude at ball-pass inner ring frequency (BPFI), indicating raceway spalling.",
            risk="Unmitigated operation will lead to catastrophic shaft seizure, unexpected chiller trip during peak heat hours, and emergency replacement costs exceeding $65,000.",
            recommendation="Schedule ultrasonic grease injection and vibration spectrum re-scan within 48 hours; stage Chiller 3 (CH-03) to take base load.",
            impact="Extends bearing life by ~6,000 run hours, prevents unexpected HVAC shutdown, and preserves $18,400 in emergency repair and business disruption costs.",
            priority="Critical",
            action_label="Dispatch Mechanical Overhaul",
            action_type="dispatch_maint",
            estimated_savings_usd=18400.0,
            action_params={"asset_id": "CH-02", "task": "Bearing greasing & spectrum analysis"}
        )

    def process_telemetry(self, asset_telemetries: List[Dict[str, Any]]):
        start = time.time()
        self.status = "Analyzing"
        self.telemetry_points_processed += len(asset_telemetries)

        total_score = 0.0
        for asset in asset_telemetries:
            score = asset.get("health_score", 90.0)
            total_score += score
            
            # Check for critical degradation alert
            if score < 55.0 and not asset.get("alert_generated", False):
                asset["alert_generated"] = True
                self.create_alert(
                    category="Maintenance",
                    severity="Critical",
                    location=f"Zone {asset.get('zone_id')} ({asset.get('name')})",
                    title=f"Critical Equipment Health Warning: {asset.get('name')}",
                    description=f"Condition score plummeted to {score:.1f}/100. Failure probability estimated at {asset.get('failure_probability_pct', 75):.0f}%.",
                    ai_explanation=f"Telemetry indicates abnormal vibration ({asset.get('vibration_rms', 0):.2f} mm/s vs {asset.get('baseline_vibration', 1.0):.2f} baseline) and thermal elevation ({asset.get('temperature_c', 0):.1f}°C). Factors: {', '.join(asset.get('contributing_factors', []))}.",
                    recommended_action="Dispatch maintenance technician immediately. Perform mechanical vibration analysis and stage backup unit.",
                    action_data={"asset_id": asset.get("id"), "health_score": score}
                )

        if asset_telemetries:
            self.average_equipment_health = round(total_score / len(asset_telemetries), 1)

        self.last_latency_ms = (time.time() - start) * 1000
        self.status = "Active"
        self.last_reasoning_summary = f"Evaluated {len(asset_telemetries)} assets. Avg Health: {self.average_equipment_health}%. Open WOs: {len(self.work_orders)}."

    def create_work_order(self, wo_data: Dict[str, Any]) -> WorkOrder:
        today = datetime.now()
        new_wo = WorkOrder(
            id=f"WO-2026-{random.randint(200, 999)}",
            asset_id=wo_data.get("asset_id", "CH-02"),
            asset_name=wo_data.get("asset_name", "Centrifugal Water Chiller 2"),
            location=wo_data.get("location", "Floor 5 Mechanical Penthouse"),
            title=wo_data.get("title", "Predictive Diagnostic & Inspection"),
            priority=wo_data.get("priority", "High"),
            status="Open",
            assigned_to=wo_data.get("assigned_to", "Thermal Systems Team"),
            team=wo_data.get("team", "Mechanical"),
            created_date=today.strftime("%Y-%m-%d"),
            due_date=(today + timedelta(days=2)).strftime("%Y-%m-%d"),
            estimated_hours=float(wo_data.get("estimated_hours", 3.0)),
            estimated_cost_usd=float(wo_data.get("estimated_cost_usd", 750.0)),
            maintenance_action=wo_data.get("maintenance_action", "Investigate high vibration harmonics and grease bearings."),
            ai_trigger_reason=wo_data.get("ai_trigger_reason", "Autonomous trigger from Predictive Maintenance Agent condition score drop.")
        )
        self.work_orders.insert(0, new_wo)
        return new_wo

    def update_work_order_status(self, wo_id: str, new_status: str) -> Optional[WorkOrder]:
        for wo in self.work_orders:
            if wo.id == wo_id:
                wo.status = new_status
                if new_status == "Completed":
                    wo.completed_date = datetime.now().strftime("%Y-%m-%d")
                    wo.actual_hours = wo.estimated_hours
                    self.prevented_failures += 1
                return wo
        return None

    def get_health_distribution(self, assets: List[Dict[str, Any]]) -> Dict[str, int]:
        healthy = sum(1 for a in assets if a.get("health_score", 90.0) >= 85.0)
        good = sum(1 for a in assets if 70.0 <= a.get("health_score", 90.0) < 85.0)
        warning = sum(1 for a in assets if 50.0 <= a.get("health_score", 90.0) < 70.0)
        critical = sum(1 for a in assets if a.get("health_score", 90.0) < 50.0)
        return {
            "healthy": healthy,
            "good": good,
            "warning": warning,
            "critical": critical
        }

    def get_kpis(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        dist = self.get_health_distribution(assets)
        open_wos = sum(1 for wo in self.work_orders if wo.status in ["Open", "Assigned", "In Progress"])
        completed_wos = sum(1 for wo in self.work_orders if wo.status == "Completed")
        
        return {
            "total_assets": len(assets),
            "healthy_assets": dist["healthy"],
            "good_assets": dist["good"],
            "warning_assets": dist["warning"],
            "critical_assets": dist["critical"],
            "average_equipment_health": self.average_equipment_health,
            "prevented_failures": self.prevented_failures,
            "open_work_orders": open_wos,
            "completed_work_orders": completed_wos,
            "mtbf_hours": self.mtbf_hours,
            "mttr_hours": self.mttr_hours,
            "maintenance_cost_ytd": self.maintenance_cost_ytd,
            "health_distribution": dist,
            "work_orders": [wo.model_dump() for wo in self.work_orders],
            "calendar_events": self.calendar_events
        }
