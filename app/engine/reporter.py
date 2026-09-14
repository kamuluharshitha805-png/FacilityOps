"""
Automated Facility Intelligence Reporting Engine.
Generates comprehensive audit and intelligence reports covering all 7 pillars.
"""

from typing import Dict, Any, List
import time
from datetime import datetime
from app.models.reports import FacilityReport
from app.engine.simulator import simulator_instance

class FacilityReportingEngine:
    def __init__(self, simulator=simulator_instance):
        self.sim = simulator

    def generate_full_report(self, period: str = "Last 24 Hours") -> FacilityReport:
        overview = self.sim.get_overview()
        orch = self.sim.orchestrator
        en = self.sim.energy_agent
        ma = self.sim.maint_agent
        oc = self.sim.occupancy_agent
        sc = self.sim.security_agent
        co = self.sim.cost_agent

        all_alerts = orch.get_all_alerts()
        all_insights = orch.get_all_insights()
        health_dist = ma.get_health_distribution(list(self.sim.assets.values()))

        report = FacilityReport(
            report_id=f"REP-FAC-{datetime.now().strftime('%Y%m%d-%H%M')}",
            title=f"Facility Intelligence Executive Audit & Performance Report ({period})",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            period=period,
            building_name=overview.building_name,
            facility_health_score=overview.facility_health_score,
            
            executive_summary={
                "overall_health_score": overview.facility_health_score,
                "status_headline": "Facility operating in stable operational state with targeted mechanical and thermal optimization opportunities active.",
                "major_issues_count": overview.active_alerts_count,
                "critical_risks_count": sum(1 for a in all_alerts if a.severity == "Critical" and a.status == "Active"),
                "prevented_catastrophic_failures": ma.prevented_failures,
                "realized_monthly_savings_usd": co.monthly_realized_savings,
                "potential_monthly_savings_usd": sum(ins.estimated_savings_usd or 0 for ins in all_insights),
                "sub_score_ratings": {
                    "Energy": f"{en.energy_score}/100",
                    "Maintenance": f"{ma.average_equipment_health}/100",
                    "Occupancy": f"{oc.space_utilization_score}/100",
                    "Security": f"{sc.security_health_score}/100",
                    "Cost": f"{co.cost_efficiency_score}/100",
                    "Sustainability": f"{co.sustainability_score}/100"
                }
            },
            
            energy_intelligence={
                "total_consumption_kwh": overview.daily_energy_kwh,
                "current_demand_kw": overview.total_power_kw,
                "peak_demand_kw": overview.peak_demand_kw,
                "water_consumption_gal": overview.daily_water_gal,
                "carbon_emissions_kg": overview.daily_carbon_kg,
                "hvac_power_share_pct": round((overview.energy_distribution.get("HVAC & Cooling", 0) / max(1, overview.total_power_kw)) * 100, 1),
                "energy_distribution": overview.energy_distribution,
                "key_opportunity": "Dynamic VAV static pressure reset can reduce fan power by 24% ($860/mo)."
            },
            
            predictive_maintenance={
                "total_assets_monitored": overview.total_assets,
                "healthy_assets": health_dist["healthy"],
                "good_assets": health_dist["good"],
                "warning_assets": health_dist["warning"],
                "critical_assets": health_dist["critical"],
                "mean_time_between_failures_hrs": ma.mtbf_hours,
                "mean_time_to_repair_hrs": ma.mttr_hours,
                "open_work_orders_count": overview.open_work_orders_count,
                "critical_asset_focus": "Centrifugal Chiller 2 (CH-02) bearing vibration FFT analysis indicates inner race raceway spalling."
            },
            
            occupancy_intelligence={
                "current_headcount": overview.current_occupancy,
                "occupancy_rate_pct": overview.occupancy_rate,
                "peak_occupancy_headcount": oc.peak_occupancy,
                "visitor_count": oc.visitor_count,
                "active_zones": oc.active_zones_count,
                "space_utilization_score": oc.space_utilization_score,
                "underutilized_zones": oc.underutilized_rooms,
                "crowded_zones": oc.crowded_zones
            },
            
            security_intelligence={
                "access_events_logged": sc.access_events_today,
                "restricted_zone_swipes": sc.restricted_zone_events_today,
                "active_security_alarms": sc.active_security_events,
                "critical_incidents": sc.critical_incidents_count,
                "security_compliance_score": sc.security_health_score,
                "perimeter_status": "Secure. Dual-biometric and PTZ automated surveillance tracking active."
            },
            
            cost_optimization={
                "daily_operating_cost_usd": overview.daily_operating_cost,
                "monthly_projected_spend_usd": round(overview.daily_operating_cost * 30.5, 2),
                "energy_cost_share": co.daily_energy_cost,
                "maintenance_cost_share": co.daily_maintenance_cost,
                "water_utility_cost_share": co.daily_water_cost,
                "cost_distribution": overview.cost_distribution,
                "financial_roi_summary": "Implementing top 3 AI recommendations yields $5,510/mo in verifiable operational savings."
            },
            
            sustainability={
                "scope_2_carbon_kg": overview.daily_carbon_kg,
                "monthly_carbon_tons": round((overview.daily_carbon_kg * 30.5) / 1000.0, 2),
                "water_utilization_efficiency": "Good (1.2 gpm/1,000 sqft)",
                "sustainability_index_score": co.sustainability_score,
                "esg_alignment": "Aligns with LEED Platinum and ISO 50001 Energy Management standard."
            },
            
            key_recommendations=[
                {
                    "title": ins.title,
                    "agent": ins.agent_source,
                    "priority": ins.priority,
                    "estimated_savings_usd": ins.estimated_savings_usd,
                    "action": ins.recommendation,
                    "impact": ins.impact
                }
                for ins in all_insights[:5]
            ]
        )
        return report

reporting_engine = FacilityReportingEngine()
