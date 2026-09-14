"""
FastAPI REST & WebSocket Endpoints Integration Test Suite.
"""

import unittest
from starlette.testclient import TestClient
from app.main import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_serve_index_html(self):
        """Verify root endpoint serves index.html."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("FacilityOps AI Platform", res.text)
        self.assertIn("main-content-view", res.text)

    def test_telemetry_overview(self):
        """Verify /api/telemetry/overview returns valid schema."""
        res = self.client.get("/api/telemetry/overview")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("facility_health_score", data)
        self.assertIn("total_power_kw", data)
        self.assertIn("energy_distribution", data)
        self.assertIn("cost_distribution", data)

    def test_telemetry_zones_and_assets(self):
        """Verify zone and asset listing and drill-down."""
        res = self.client.get("/api/telemetry/zones")
        self.assertEqual(res.status_code, 200)
        zones = res.json()
        self.assertEqual(len(zones), 24)

        # Drill-down
        zone_id = zones[0]["id"]
        res_detail = self.client.get(f"/api/telemetry/zones/{zone_id}")
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn("zone", res_detail.json())
        self.assertIn("assets", res_detail.json())

        # Assets
        res_assets = self.client.get("/api/telemetry/assets")
        self.assertEqual(res_assets.status_code, 200)
        assets = res_assets.json()
        self.assertGreater(len(assets), 30)

    def test_agents_status_and_correlations(self):
        """Verify agents status and cross-agent correlations."""
        res_agents = self.client.get("/api/agents/status")
        self.assertEqual(res_agents.status_code, 200)
        agents = res_agents.json()
        self.assertEqual(len(agents), 5)

        res_corr = self.client.get("/api/agents/correlations")
        self.assertEqual(res_corr.status_code, 200)
        corrs = res_corr.json()
        self.assertGreater(len(corrs), 0)

    def test_alerts_and_workorders(self):
        """Verify alerts and work orders CRUD endpoints."""
        res_alerts = self.client.get("/api/alerts")
        self.assertEqual(res_alerts.status_code, 200)
        alerts = res_alerts.json()
        self.assertIsInstance(alerts, list)

        res_wos = self.client.get("/api/workorders")
        self.assertEqual(res_wos.status_code, 200)
        wos = res_wos.json()
        self.assertGreater(len(wos), 0)

    def test_reporting_engine_endpoint(self):
        """Verify report generation endpoint."""
        res = self.client.get("/api/reports/generate?period=Last%2024%20Hours")
        self.assertEqual(res.status_code, 200)
        rep = res.json()
        self.assertIn("executive_summary", rep)
        self.assertIn("energy_intelligence", rep)
        self.assertIn("predictive_maintenance", rep)
        self.assertIn("occupancy_intelligence", rep)
        self.assertIn("security_intelligence", rep)
        self.assertIn("cost_optimization", rep)
        self.assertIn("sustainability", rep)

    def test_simulation_injection_endpoint(self):
        """Verify incident injection via API."""
        res = self.client.post("/api/simulation/inject", json={"scenario_id": "scenario_chiller_overheat"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")

    def test_websocket_streaming(self):
        """Verify WebSocket stream connects and emits initial state."""
        with self.client.websocket_connect("/ws/live") as ws:
            msg = ws.receive_json()
            self.assertEqual(msg["type"], "initial_state")
            self.assertIn("overview", msg)
            
            # Send ping
            ws.send_json({"action": "ping"})
            resp = ws.receive_json()
            self.assertEqual(resp["type"], "pong")

if __name__ == "__main__":
    unittest.main(verbosity=2)
