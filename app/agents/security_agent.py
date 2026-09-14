"""
Security Intelligence Agent for FacilityOps.
Monitors electronic badge reader access logs, CCTV AI metadata, perimeter boundaries,
and detects anomalous movements or unauthorized intrusions across zoned security levels.
"""

from typing import Dict, Any, List, Optional
import time
import random
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent
from app.config import (
    ZONE_SECURITY_PUBLIC,
    ZONE_SECURITY_OPERATIONAL,
    ZONE_SECURITY_RESTRICTED,
    ZONE_SECURITY_HIGH,
    FACILITY_ZONES
)

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="agt_security_04",
            name="Security Intelligence Agent",
            role="Autonomous Access Perimeter, CCTV Analytics & Zone Intrusion Detection"
        )
        self.access_events_today = 3840
        self.active_security_events = 1
        self.critical_incidents_count = 0
        self.restricted_zone_events_today = 142
        self.security_health_score = 96.0
        
        # Recent live access logs
        self.recent_access_logs: List[Dict[str, Any]] = self._seed_access_logs()
        
        # CCTV Event stream metadata
        self.cctv_events: List[Dict[str, Any]] = self._seed_cctv_events()

        # Seed initial insight
        self._seed_initial_insights()

    def _seed_access_logs(self) -> List[Dict[str, Any]]:
        now = datetime.now()
        logs = [
            {"id": "ACC-8910", "timestamp": (now - timedelta(minutes=2)).strftime("%H:%M:%S"), "badge_id": "BDG-5520", "user": "Dr. Elena Rostova", "department": "Quantum R&D", "zone_id": "Z-F2-01", "zone_name": "Hardware R&D Lab Alpha", "security_tier": ZONE_SECURITY_RESTRICTED, "status": "Granted", "portal": "Card Reader F2-North"},
            {"id": "ACC-8909", "timestamp": (now - timedelta(minutes=5)).strftime("%H:%M:%S"), "badge_id": "BDG-2041", "user": "Marcus Brody", "department": "Facility Engineering", "zone_id": "Z-F5-03", "zone_name": "Chiller Plant Penthouse", "security_tier": ZONE_SECURITY_RESTRICTED, "status": "Granted", "portal": "Penthouse Turnstile S"},
            {"id": "ACC-8908", "timestamp": (now - timedelta(minutes=8)).strftime("%H:%M:%S"), "badge_id": "BDG-9902", "user": "Contractor - Fire Inspection", "department": "External Services", "zone_id": "Z-F1-01", "zone_name": "Main Atrium", "security_tier": ZONE_SECURITY_PUBLIC, "status": "Granted", "portal": "Speed Gate 3"},
            {"id": "ACC-8907", "timestamp": (now - timedelta(minutes=14)).strftime("%H:%M:%S"), "badge_id": "BDG-7422", "user": "Unknown Guest 09", "department": "Visitor", "zone_id": "Z-F5-01", "zone_name": "Mission Critical Data Center", "security_tier": ZONE_SECURITY_HIGH, "status": "Denied", "portal": "Mantrap Ingress 1", "reason": "Insufficient Security Clearance Level 4"}
        ]
        return logs

    def _seed_cctv_events(self) -> List[Dict[str, Any]]:
        now = datetime.now()
        return [
            {"id": "CCTV-EV-101", "timestamp": (now - timedelta(minutes=14)).strftime("%H:%M:%S"), "camera_id": "CAM-F5-01-PTZ", "location": "Floor 5 Data Center Mantrap", "event_type": "Access Denied Loitering", "severity": "Medium", "confidence": 0.94, "description": "Individual remained at high-security biometric portal for >120s following access denial.", "action_taken": "Audio advisory issued via two-way intercom."},
            {"id": "CCTV-EV-102", "timestamp": (now - timedelta(minutes=32)).strftime("%H:%M:%S"), "camera_id": "CAM-F1-03-DOCK", "location": "Loading Dock Delivery Bay 2", "event_type": "Vehicle Arrival Verified", "severity": "Information", "confidence": 0.98, "description": "Authorized logistics carrier plate verified against manifest.", "action_taken": "Automated bay roller door opened."},
            {"id": "CCTV-EV-103", "timestamp": (now - timedelta(minutes=55)).strftime("%H:%M:%S"), "camera_id": "CAM-F2-03-CLEAN", "location": "Prototype Clean Room Airlock", "event_type": "PPE Compliance Verification", "severity": "Low", "confidence": 0.99, "description": "All personnel entering airlock detected with required ESD suit and hairnet.", "action_taken": "Logged compliance."}
        ]

    def _seed_initial_insights(self):
        self.create_insight(
            title="Biometric Mantrap Loitering Pattern",
            category="Perimeter Security",
            insight="Visitor badge BDG-7422 registered a clearance denial at Mission Data Center mantrap, followed by 140 seconds of unauthorized dwell time detected by AI camera CAM-F5-01-PTZ.",
            why="Guest attempted access outside authorized visitor envelope (Floor 1 & 3 public areas only).",
            risk="Potential physical reconnaissance or social engineering tailgating opportunity into tier-4 data center.",
            recommendation="Dispatch roaming security patrol to Floor 5 corridor to escort visitor back to designated Floor 1 lobby.",
            impact="Eliminates breach vector into mission-critical infrastructure and enforces ISO 27001 physical security compliance.",
            priority="High",
            action_label="Dispatch Security Patrol",
            action_type="security_alert",
            estimated_savings_usd=0.0,
            action_params={"camera_id": "CAM-F5-01-PTZ", "zone_id": "Z-F5-01"}
        )

    def log_badge_event(self, event_data: Dict[str, Any]):
        self.access_events_today += 1
        event_data["id"] = f"ACC-{random.randint(9000, 9999)}"
        event_data["timestamp"] = datetime.now().strftime("%H:%M:%S")
        self.recent_access_logs.insert(0, event_data)
        if len(self.recent_access_logs) > 30:
            self.recent_access_logs = self.recent_access_logs[:30]

    def process_telemetry(self, zone_telemetries: List[Dict[str, Any]]):
        start = time.time()
        self.status = "Analyzing"
        self.telemetry_points_processed += len(zone_telemetries)

        # Evaluate high-security zone motion
        for z in zone_telemetries:
            tier = z.get("security", ZONE_SECURITY_PUBLIC)
            motion = z.get("motion_detected", False)
            occupancy = z.get("current_occupancy", 0)
            
            # If high-security zone has motion/occupancy, verify
            if tier in [ZONE_SECURITY_HIGH, ZONE_SECURITY_RESTRICTED] and occupancy > 0:
                self.restricted_zone_events_today += 1

        self.security_health_score = round(max(70.0, min(99.0, 98.0 - (self.critical_incidents_count * 10.0))), 1)

        self.last_latency_ms = (time.time() - start) * 1000
        self.status = "Active"
        self.last_reasoning_summary = f"Monitoring {len(FACILITY_ZONES)} zones. Access events today: {self.access_events_today}. Security Score: {self.security_health_score}%."

    def get_zone_activity_summary(self) -> Dict[str, Any]:
        return {
            "public_zones": sum(1 for z in FACILITY_ZONES if z["security"] == ZONE_SECURITY_PUBLIC),
            "operational_zones": sum(1 for z in FACILITY_ZONES if z["security"] == ZONE_SECURITY_OPERATIONAL),
            "restricted_zones": sum(1 for z in FACILITY_ZONES if z["security"] == ZONE_SECURITY_RESTRICTED),
            "high_security_zones": sum(1 for z in FACILITY_ZONES if z["security"] == ZONE_SECURITY_HIGH)
        }

    def get_kpis(self) -> Dict[str, Any]:
        return {
            "access_events_today": self.access_events_today,
            "active_security_events": self.active_security_events,
            "critical_incidents_count": self.critical_incidents_count,
            "restricted_zone_events_today": self.restricted_zone_events_today,
            "security_health_score": self.security_health_score,
            "zone_activity": self.get_zone_activity_summary(),
            "recent_access_logs": self.recent_access_logs[:10],
            "cctv_events": self.cctv_events[:10]
        }
