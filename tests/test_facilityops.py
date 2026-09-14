"""
Comprehensive Automated Test Suite for FacilityOps AI Platform.
Validates simulation, autonomous agents, cross-agent orchestration,
scenario injections, work order lifecycles, and reporting.
"""

import sys
import unittest

from app.config import FACILITY_ZONES, ASSET_REGISTRY, HEALTH_SCORE_WEIGHTS
from app.engine.simulator import FacilitySimulator
from app.engine.reporter import FacilityReportingEngine
from app.models.telemetry import FacilityOverviewTelemetry
from app.models.reports import FacilityReport

class TestFacilityOpsPlatform(unittest.TestCase):
    def setUp(self):
        self.sim = FacilitySimulator()
        self.reporter = FacilityReportingEngine(self.sim)

    def test_building_topology_and_asset_registry(self):
        """Verify building has 5 floors, 24 zones, and 50+ industrial assets."""
        self.assertEqual(len(FACILITY_ZONES), 24, "Should have exactly 24 facility zones")
        floors = {z["floor"] for z in FACILITY_ZONES}
        self.assertEqual(floors, {1, 2, 3, 4, 5}, "Should span 5 distinct building floors")
        self.assertGreaterEqual(len(ASSET_REGISTRY), 35, "Should register all primary industrial assets")

    def test_simulator_step_and_telemetry(self):
        """Verify simulator advances physics, environmental variables, and telemetry."""
        initial_kwh = self.sim.energy_agent.daily_kwh
        self.sim.step_simulation()
        
        overview = self.sim.get_overview()
        self.assertIsInstance(overview, FacilityOverviewTelemetry)
        self.assertGreater(overview.total_power_kw, 0.0)
        self.assertGreater(overview.daily_energy_kwh, initial_kwh)
        self.assertGreater(overview.facility_health_score, 0.0)
        self.assertLessEqual(overview.facility_health_score, 100.0)

    def test_energy_agent_intelligence(self):
        """Verify energy agent computes distribution, water flow, and carbon emissions."""
        dist = self.sim.energy_agent.get_energy_distribution()
        self.assertIn("HVAC & Cooling", dist)
        self.assertIn("Lighting & Façade", dist)
        self.assertGreater(self.sim.energy_agent.daily_carbon_kg, 0.0)
        self.assertGreater(self.sim.energy_agent.energy_score, 50.0)

    def test_predictive_maintenance_agent(self):
        """Verify condition scores, failure probability, and work order lifecycle."""
        maint = self.sim.maint_agent
        assets = list(self.sim.assets.values())
        dist = maint.get_health_distribution(assets)
        self.assertEqual(dist["healthy"] + dist["good"] + dist["warning"] + dist["critical"], len(assets))

        # Create Work Order
        wo = maint.create_work_order({
            "asset_id": "CH-01",
            "asset_name": "Centrifugal Water Chiller 1",
            "location": "Penthouse",
            "title": "Routine Oil Sampling",
            "priority": "Low",
            "estimated_hours": 2.0,
            "estimated_cost_usd": 300.0,
            "maintenance_action": "Draw oil sample.",
            "ai_trigger_reason": "Preventive maintenance check"
        })
        self.assertEqual(wo.status, "Open")

        # Update lifecycle to Completed
        updated = maint.update_work_order_status(wo.id, "Completed")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.status, "Completed")
        self.assertIsNotNone(updated.completed_date)

    def test_occupancy_agent_intelligence(self):
        """Verify spatial density, space utilization score, and zone distribution."""
        occ = self.sim.occupancy_agent
        zones = list(self.sim.zones.values())
        dist = occ.get_zone_occupancy_distribution(zones)
        self.assertEqual(sum(dist.values()), len(zones))
        self.assertGreater(occ.space_utilization_score, 0.0)
        self.assertLessEqual(occ.space_utilization_score, 100.0)

    def test_security_agent_intelligence(self):
        """Verify access events, security health score, and zone tiers."""
        sec = self.sim.security_agent
        self.assertGreater(sec.access_events_today, 0)
        self.assertGreater(sec.security_health_score, 70.0)
        summary = sec.get_zone_activity_summary()
        self.assertIn("high_security_zones", summary)

    def test_cost_agent_and_tariffs(self):
        """Verify operating cost breakdown and sustainability scoring."""
        cost = self.sim.cost_agent
        dist = cost.get_cost_distribution()
        self.assertIn("Energy & Electricity", dist)
        self.assertIn("Predictive & Planned Maintenance", dist)
        self.assertGreater(cost.total_daily_operating_cost, 0.0)
        self.assertGreater(cost.sustainability_score, 50.0)

    def test_cross_agent_orchestration_and_unified_health_score(self):
        """Verify the cross-agent orchestration engine computes weighted score and correlations."""
        orch = self.sim.orchestrator
        score = orch.compute_facility_health_score()
        self.assertAlmostEqual(score, self.sim.orchestrator.facility_health_score, places=1)
        self.assertGreaterEqual(len(orch.active_correlations), 3)

        # Validate weights sum to 1.0
        self.assertAlmostEqual(sum(HEALTH_SCORE_WEIGHTS.values()), 1.0, places=4)

    def test_chiller_overheat_scenario_injection(self):
        """Verify injecting Chiller 2 incident collapses health and triggers cross-agent correlation."""
        res = self.sim.inject_scenario("scenario_chiller_overheat")
        self.assertEqual(res["status"], "success")
        
        ch2 = self.sim.assets["CH-02"]
        self.assertEqual(ch2["health_status"], "Critical")
        self.assertGreater(ch2["vibration_rms"], 4.0)
        self.assertGreater(ch2["failure_probability_pct"], 75.0)

        # Check cross-agent correlation triggered
        corr_pairs = [c.pair for c in self.sim.orchestrator.active_correlations]
        self.assertIn("ENERGY ↔ MAINTENANCE", corr_pairs)

    def test_restricted_breach_scenario_injection(self):
        """Verify restricted zone breach triggers OCCUPANCY <-> SECURITY correlation."""
        res = self.sim.inject_scenario("scenario_restricted_breach")
        self.assertEqual(res["status"], "success")

        corr_pairs = [c.pair for c in self.sim.orchestrator.active_correlations]
        self.assertIn("OCCUPANCY ↔ SECURITY", corr_pairs)

        # Check critical security alert logged
        alerts = self.sim.orchestrator.get_all_alerts()
        sec_critical = [a for a in alerts if a.category == "Security" and a.severity == "Critical"]
        self.assertGreaterEqual(len(sec_critical), 1)

    def test_reporting_engine(self):
        """Verify full 7-pillar report generation."""
        report = self.reporter.generate_full_report("Last 24 Hours")
        self.assertIsInstance(report, FacilityReport)
        self.assertEqual(report.building_name, "Apex Tower Global HQ")
        self.assertIn("status_headline", report.executive_summary)
        self.assertIn("total_consumption_kwh", report.energy_intelligence)
        self.assertIn("mean_time_between_failures_hrs", report.predictive_maintenance)
        self.assertIn("occupancy_rate_pct", report.occupancy_intelligence)
        self.assertIn("security_compliance_score", report.security_intelligence)
        self.assertIn("daily_operating_cost_usd", report.cost_optimization)
        self.assertIn("scope_2_carbon_kg", report.sustainability)
        self.assertGreater(len(report.key_recommendations), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
