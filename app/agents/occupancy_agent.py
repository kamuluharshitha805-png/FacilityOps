"""
Occupancy Intelligence Agent for FacilityOps.
Analyzes zone density, room utilization patterns, visitor movements,
and spatial efficiency to optimize building HVAC, lighting, and workspace allocation.
"""

from typing import Dict, Any, List, Optional
import math
import random
import time
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.config import FACILITY_ZONES

class OccupancyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="agt_occupancy_03",
            name="Occupancy Intelligence Agent",
            role="Autonomous Spatial Density, Space Utilization & Visitor Analytics"
        )
        self.total_building_capacity = sum(z["capacity"] for z in FACILITY_ZONES)
        self.current_occupancy = 582
        self.peak_occupancy = 840
        self.occupancy_rate = round((self.current_occupancy / self.total_building_capacity) * 100, 1)
        self.visitor_count = 48
        self.active_zones_count = 21
        self.space_utilization_score = 84.5
        
        # Room utilization tracking
        self.underutilized_rooms: List[str] = ["Z-F4-03", "Z-F3-04"]
        self.crowded_zones: List[str] = ["Z-F1-02", "Z-F3-01"]
        
        # Hourly profile buffer
        self.hourly_occupancy_profile = self._init_hourly_profile()
        
        # Seed initial insight
        self._seed_initial_insights()

    def _init_hourly_profile(self) -> List[Dict[str, Any]]:
        points = []
        now_hour = 13
        for i in range(24):
            hr = (now_hour - 23 + i) % 24
            if 8 <= hr <= 18:
                # Working hours
                occ = int(250 + 580 * math.sin(max(0, (hr - 8)) / 10 * math.pi) + random.uniform(-20, 20))
                visitors = int(10 + 40 * math.sin(max(0, (hr - 9)) / 8 * math.pi))
            else:
                occ = int(15 + random.uniform(0, 15))
                visitors = 0
            points.append({
                "time": f"{hr:02d}:00",
                "occupancy": max(5, occ),
                "visitors": max(0, visitors),
                "utilization_pct": round(min(100.0, (occ / self.total_building_capacity) * 100), 1)
            })
        return points

    def _seed_initial_insights(self):
        self.create_insight(
            title="Floor 4 Conference & Briefing Room Underutilization",
            category="Space Utilization",
            insight="Global Strategy Briefing Room (Z-F4-03) has averaged only 8.5% weekly occupancy despite 6,000 sq ft dedicated footprint and continuous climate conditioning.",
            why="Calendar bookings show 78% cancellation rate and shift to hybrid remote video meetings.",
            risk="Unneeded lighting and dedicated HVAC continuous runtime costs $1,450/month in wasted operational energy.",
            recommendation="Convert Z-F4-03 to an on-demand occupancy-triggered zone with automated setback mode when unbooked.",
            impact="Reduces dedicated conditioning load by 65%, saving ~$1,450/month and reclaiming space for flexible agile pods.",
            priority="Medium",
            action_label="Implement On-Demand Zone Setback",
            action_type="schedule_adjust",
            estimated_savings_usd=1450.0,
            action_params={"zone_id": "Z-F4-03", "setback_mode": "occupancy_triggered"}
        )

    def process_telemetry(self, zone_telemetries: List[Dict[str, Any]]):
        start = time.time()
        self.status = "Analyzing"
        self.telemetry_points_processed += len(zone_telemetries)

        total_occ = sum(z.get("current_occupancy", 0) for z in zone_telemetries)
        self.current_occupancy = total_occ
        if self.current_occupancy > self.peak_occupancy:
            self.peak_occupancy = self.current_occupancy

        self.occupancy_rate = round((self.current_occupancy / max(1, self.total_building_capacity)) * 100, 1)
        self.active_zones_count = sum(1 for z in zone_telemetries if z.get("current_occupancy", 0) > 0)

        # Categorize zones
        self.crowded_zones = [z["id"] for z in zone_telemetries if z.get("occupancy_rate", 0) > 85.0]
        self.underutilized_rooms = [z["id"] for z in zone_telemetries if z.get("occupancy_rate", 0) < 15.0 and z.get("type") in ["Office", "Conference", "Executive"]]

        # Calculate space utilization score (optimal between 55% and 80%)
        ideal_center = 70.0
        delta = abs(self.occupancy_rate - ideal_center)
        self.space_utilization_score = round(max(50.0, min(98.0, 95.0 - delta * 0.7)), 1)

        self.last_latency_ms = (time.time() - start) * 1000
        self.status = "Active"
        self.last_reasoning_summary = f"Tracking {len(zone_telemetries)} zones. Occupancy: {self.current_occupancy}/{self.total_building_capacity} ({self.occupancy_rate}%). Active Zones: {self.active_zones_count}."

    def get_zone_occupancy_distribution(self, zone_telemetries: List[Dict[str, Any]]) -> Dict[str, int]:
        crowded = sum(1 for z in zone_telemetries if z.get("occupancy_rate", 0) >= 80.0)
        normal = sum(1 for z in zone_telemetries if 35.0 <= z.get("occupancy_rate", 0) < 80.0)
        low = sum(1 for z in zone_telemetries if 5.0 <= z.get("occupancy_rate", 0) < 35.0)
        empty = sum(1 for z in zone_telemetries if z.get("occupancy_rate", 0) < 5.0)
        return {
            "crowded": crowded,
            "normal": normal,
            "low": low,
            "empty": empty
        }

    def get_floor_breakdown(self, zone_telemetries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        floors = {}
        for z in zone_telemetries:
            fl = z.get("floor", 1)
            if fl not in floors:
                floors[fl] = {"floor": fl, "occupancy": 0, "capacity": 0, "active_zones": 0, "total_zones": 0}
            floors[fl]["occupancy"] += z.get("current_occupancy", 0)
            floors[fl]["capacity"] += z.get("capacity", 1)
            floors[fl]["total_zones"] += 1
            if z.get("current_occupancy", 0) > 0:
                floors[fl]["active_zones"] += 1
        
        result = []
        for fl, data in sorted(floors.items()):
            data["rate_pct"] = round((data["occupancy"] / max(1, data["capacity"])) * 100, 1)
            result.append(data)
        return result

    def get_kpis(self, zone_telemetries: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "current_occupancy": self.current_occupancy,
            "total_capacity": self.total_building_capacity,
            "occupancy_rate": self.occupancy_rate,
            "peak_occupancy": self.peak_occupancy,
            "visitor_count": self.visitor_count,
            "active_zones_count": self.active_zones_count,
            "space_utilization_score": self.space_utilization_score,
            "crowded_zones_count": len(self.crowded_zones),
            "underutilized_zones_count": len(self.underutilized_rooms),
            "zone_distribution": self.get_zone_occupancy_distribution(zone_telemetries),
            "floor_breakdown": self.get_floor_breakdown(zone_telemetries),
            "hourly_profile": self.hourly_occupancy_profile
        }
