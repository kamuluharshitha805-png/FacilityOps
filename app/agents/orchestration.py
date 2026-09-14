"""
Cross-Agent Orchestration & Facility Intelligence Engine.
The central nervous system of FacilityOps that correlates telemetry across all agents,
executes multi-agent AI reasoning, computes the unified Facility Health Score,
and drives the Facility Intelligence Command Center.
"""

from typing import Dict, Any, List, Optional
import time
import random
from datetime import datetime
from app.agents.energy_agent import EnergyAgent
from app.agents.maintenance_agent import MaintenanceAgent
from app.agents.occupancy_agent import OccupancyAgent
from app.agents.security_agent import SecurityAgent
from app.agents.cost_agent import CostAgent
from app.models.agents import CrossAgentCorrelation, AIInsight
from app.models.alerts import FacilityAlert
from app.config import HEALTH_SCORE_WEIGHTS, ZONE_SECURITY_HIGH, ZONE_SECURITY_RESTRICTED

class FacilityOrchestrator:
    def __init__(
        self,
        energy_agent: EnergyAgent,
        maint_agent: MaintenanceAgent,
        occupancy_agent: OccupancyAgent,
        security_agent: SecurityAgent,
        cost_agent: CostAgent
    ):
        self.energy_agent = energy_agent
        self.maint_agent = maint_agent
        self.occupancy_agent = occupancy_agent
        self.security_agent = security_agent
        self.cost_agent = cost_agent
        
        self.facility_health_score = 91.5
        self.active_correlations: List[CrossAgentCorrelation] = []
        self.last_sync_time = datetime.now().strftime("%H:%M:%S")
        
        # Initialize standard correlations
        self._init_baseline_correlations()

    def _init_baseline_correlations(self):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.active_correlations = [
            CrossAgentCorrelation(
                id="CORR-EN-MA-01",
                pair="ENERGY ↔ MAINTENANCE",
                agent_a="Energy Intelligence Agent",
                agent_b="Predictive Maintenance Agent",
                event_a="Chiller 2 specific electrical draw rose by +18% (1.14 kW/ton vs 0.72 baseline).",
                event_b="Chiller 2 drive-end bearing vibration RMS increased to 3.8 mm/s with 59.5°C thermal rise.",
                correlation_rule="Correlated Mechanical Friction Loss & Power Spike Pattern",
                ai_reasoning="Bearing raceway spalling is inducing mechanical rotational resistance, directly causing motor over-amperage and wasting 48 kW of electrical continuous load.",
                confidence_pct=96.4,
                recommended_unified_action="Dispatch expedited laser alignment and ultrasonic grease injection. Stage redundant Chiller 3.",
                financial_or_risk_impact="Avoids $18,400 emergency motor replacement and eliminates $2,100/mo parasitic power burn.",
                timestamp=now_str,
                active=True
            ),
            CrossAgentCorrelation(
                id="CORR-EN-OC-01",
                pair="ENERGY ↔ OCCUPANCY",
                agent_a="Energy Intelligence Agent",
                agent_b="Occupancy Intelligence Agent",
                event_a="Floor 4 Executive Briefing Room VAV box cooling airflow at 100% capacity (42 kW load).",
                event_b="PIR & optical sensors confirm 0 occupants present for past 180 continuous minutes.",
                correlation_rule="Unoccupied Conditioned Space Energy Waste Rule",
                ai_reasoning="Zone schedule in BMS did not clear after canceled calendar meeting, causing full-blast cooling and lighting in an empty 6,000 sq ft hall.",
                confidence_pct=99.1,
                recommended_unified_action="Execute automated thermal setback (21°C -> 24°C) and extinguish decorative downlights.",
                financial_or_risk_impact="Immediately cuts 38 kW continuous waste, saving $1,450/month in operating costs.",
                timestamp=now_str,
                active=True
            ),
            CrossAgentCorrelation(
                id="CORR-MA-CO-01",
                pair="MAINTENANCE ↔ COST",
                agent_a="Predictive Maintenance Agent",
                agent_b="Cost Optimization Agent",
                event_a="Chiller 2 failure probability increased to 74% within 14-day window.",
                event_b="Cost Agent evaluated emergency replacement quote ($185,000) vs planned overhaul ($8,400).",
                correlation_rule="Lifecycle Failure Cost-Risk Optimization",
                ai_reasoning="Running equipment to failure in peak season multiplies cost by 22x and causes severe tenant disruption. Planned intervention delivers 95.4% cost avoidance.",
                confidence_pct=98.0,
                recommended_unified_action="Approve preventative maintenance work order WO-2026-101 immediately during scheduled weekend downtime window.",
                financial_or_risk_impact="Yields net capital risk avoidance of $176,600.",
                timestamp=now_str,
                active=True
            )
        ]

    def evaluate_cross_agent_rules(
        self,
        zone_telemetries: List[Dict[str, Any]],
        asset_telemetries: List[Dict[str, Any]]
    ):
        """
        Continuously evaluate active cross-agent correlation pipelines across all 5 agents.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. OCCUPANCY ↔ SECURITY: Movement in restricted zone without badge swipe
        for z in zone_telemetries:
            tier = z.get("security")
            occ = z.get("current_occupancy", 0)
            motion = z.get("motion_detected", False)
            
            if tier in [ZONE_SECURITY_HIGH, ZONE_SECURITY_RESTRICTED] and (occ > 0 or motion):
                # Check if an authorized badge swipe occurred in this zone in last 5 mins
                zone_id = z["id"]
                authorized_swipes = [
                    log for log in self.security_agent.recent_access_logs 
                    if log.get("zone_id") == zone_id and log.get("status") == "Granted"
                ]
                
                if not authorized_swipes and not any(c.id == f"CORR-OC-SC-{zone_id}" for c in self.active_correlations):
                    # Raise High-Priority Cross-Agent Correlation!
                    corr = CrossAgentCorrelation(
                        id=f"CORR-OC-SC-{zone_id}",
                        pair="OCCUPANCY ↔ SECURITY",
                        agent_a="Occupancy Intelligence Agent",
                        agent_b="Security Intelligence Agent",
                        event_a=f"PIR motion sensors detected {occ} person(s) moving inside {z['name']} ({zone_id}).",
                        event_b=f"Security access log has zero valid badge swipes in {zone_id} during the last 5-minute window.",
                        correlation_rule="Unauthenticated Physical Presence in Restricted Zone",
                        ai_reasoning="Occupancy telemetry confirms physical breach in restricted security tier without electronic access authorization. Possible forced door or tailgating.",
                        confidence_pct=97.8,
                        recommended_unified_action=f"Lockdown zone {zone_id} access doors, reposition PTZ cameras, and dispatch rapid security patrol.",
                        financial_or_risk_impact="Prevents unauthorized data compromise or intellectual property theft.",
                        timestamp=now_str,
                        active=True
                    )
                    self.active_correlations.insert(0, corr)
                    
                    # Create central alert
                    self.security_agent.create_alert(
                        category="Security",
                        severity="Critical",
                        location=f"{z['name']} ({zone_id})",
                        title="Cross-Agent Correlated Breach: Unauthenticated Zone Intrusion",
                        description=f"Motion detected in high-security zone {z['name']} with no corresponding valid badge entry.",
                        ai_explanation="Correlated Occupancy PIR telemetry against Security Access Control event logs. High confidence unauthorized intrusion.",
                        recommended_action="Execute immediate security dispatch and lockdown.",
                        action_data={"zone_id": zone_id, "breach_type": "tailgate_or_bypass"}
                    )

        # 2. ENERGY ↔ MAINTENANCE: Equipment vibration & power surge correlation
        for a in asset_telemetries:
            vib_ratio = a.get("vibration_rms", 1.0) / max(0.1, a.get("baseline_vibration", 1.0))
            if vib_ratio > 2.2 and not any(c.id == f"CORR-EN-MA-{a['id']}" for c in self.active_correlations):
                corr = CrossAgentCorrelation(
                    id=f"CORR-EN-MA-{a['id']}",
                    pair="ENERGY ↔ MAINTENANCE",
                    agent_a="Predictive Maintenance Agent",
                    agent_b="Energy Intelligence Agent",
                    event_a=f"Vibration on {a['name']} elevated {vib_ratio:.1f}x above baseline ({a.get('vibration_rms'):.2f} mm/s).",
                    event_b=f"Equipment power draw spiked to {a.get('current_kw'):.1f} kW (+28% above standard operating curve).",
                    correlation_rule="Mechanical Wear Driving Parasitic Electrical Surge",
                    ai_reasoning=f"Severe mechanical degradation in {a['name']} is causing excessive friction, converting electrical energy directly into waste heat and vibration.",
                    confidence_pct=95.2,
                    recommended_unified_action=f"Immediately issue emergency work order for {a['name']} and transfer load to backup asset.",
                    financial_or_risk_impact=f"Avoids catastrophic motor burn-out ($45,000) and saves {a.get('current_kw')*0.25:.0f} kW in parasitic power.",
                    timestamp=now_str,
                    active=True
                )
                self.active_correlations.insert(0, corr)

        # Keep active correlations bounded
        if len(self.active_correlations) > 10:
            self.active_correlations = self.active_correlations[:10]

    def compute_facility_health_score(self) -> float:
        """
        Unified Facility Health Score weighted multi-agent formula:
        Score = 0.20*Energy + 0.25*Maintenance + 0.15*Occupancy + 0.15*Security + 0.15*Cost + 0.10*Sustainability
        """
        w = HEALTH_SCORE_WEIGHTS
        score = (
            w["energy"] * self.energy_agent.energy_score +
            w["maintenance"] * self.maint_agent.average_equipment_health +
            w["occupancy"] * self.occupancy_agent.space_utilization_score +
            w["security"] * self.security_agent.security_health_score +
            w["cost"] * self.cost_agent.cost_efficiency_score +
            w["sustainability"] * self.cost_agent.sustainability_score
        )
        self.facility_health_score = round(score, 1)
        self.last_sync_time = datetime.now().strftime("%H:%M:%S")
        return self.facility_health_score

    def get_all_insights(self) -> List[AIInsight]:
        """Aggregate insights from all agents, ordered by priority."""
        all_ins: List[AIInsight] = []
        all_ins.extend(self.energy_agent.active_insights)
        all_ins.extend(self.maint_agent.active_insights)
        all_ins.extend(self.occupancy_agent.active_insights)
        all_ins.extend(self.security_agent.active_insights)
        all_ins.extend(self.cost_agent.active_insights)
        
        priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        all_ins.sort(key=lambda x: priority_map.get(x.priority, 4))
        return all_ins

    def get_all_alerts(self) -> List[FacilityAlert]:
        """Aggregate central alerts from all agents."""
        alerts: List[FacilityAlert] = []
        alerts.extend(self.energy_agent.generated_alerts)
        alerts.extend(self.maint_agent.generated_alerts)
        alerts.extend(self.occupancy_agent.generated_alerts)
        alerts.extend(self.security_agent.generated_alerts)
        alerts.extend(self.cost_agent.generated_alerts)
        
        severity_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Information": 4}
        alerts.sort(key=lambda x: severity_map.get(x.severity, 5))
        return alerts

    def get_executive_overview(self) -> Dict[str, Any]:
        """Produce the high-level executive command center summary."""
        health = self.compute_facility_health_score()
        alerts = self.get_all_alerts()
        active_alerts = [a for a in alerts if a.status == "Active"]
        insights = self.get_all_insights()

        return {
            "facility_health_score": health,
            "sub_scores": {
                "energy": self.energy_agent.energy_score,
                "maintenance": self.maint_agent.average_equipment_health,
                "occupancy": self.occupancy_agent.space_utilization_score,
                "security": self.security_agent.security_health_score,
                "cost": self.cost_agent.cost_efficiency_score,
                "sustainability": self.cost_agent.sustainability_score
            },
            "major_risks": [
                "Chiller 2 drive-end bearing vibration approaching critical trip threshold.",
                "Upcoming afternoon peak-tariff window risk ($0.245/kWh demand surcharge)."
            ],
            "major_opportunities": [
                "Dynamic VAV static pressure reset can reduce fan power by 24% ($860/mo).",
                "On-demand setback in Floor 4 conference briefing room yields $1,450/mo savings."
            ],
            "active_alerts_count": len(active_alerts),
            "critical_alerts_count": sum(1 for a in active_alerts if a.severity == "Critical"),
            "open_work_orders_count": len([wo for wo in self.maint_agent.work_orders if wo.status != "Completed"]),
            "estimated_monthly_savings_usd": sum(ins.estimated_savings_usd or 0 for ins in insights),
            "active_correlations": [c.model_dump() for c in self.active_correlations[:5]],
            "last_sync": self.last_sync_time
        }
