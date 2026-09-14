"""
Base AI Agent architecture for FacilityOps.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from app.models.agents import AgentStatus, AIInsight
from app.models.alerts import FacilityAlert

class BaseAgent:
    def __init__(self, agent_id: str, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.status = "Active"
        self.health_rating = "Nominal"
        self.last_latency_ms = 1.2
        self.telemetry_points_processed = 0
        self.alerts_generated = 0
        self.recommendations_generated = 0
        self.last_reasoning_summary = "Initialized and awaiting telemetry stream."
        self.active_insights: List[AIInsight] = []
        self.generated_alerts: List[FacilityAlert] = []

    def get_status(self) -> AgentStatus:
        return AgentStatus(
            id=self.agent_id,
            name=self.name,
            role=self.role,
            status=self.status,
            health_rating=self.health_rating,
            latency_ms=round(self.last_latency_ms, 2),
            telemetry_points_processed=self.telemetry_points_processed,
            alerts_generated=self.alerts_generated,
            recommendations_generated=self.recommendations_generated,
            active_insights_count=len(self.active_insights),
            last_reasoning_summary=self.last_reasoning_summary,
            last_updated=datetime.now().strftime("%H:%M:%S")
        )

    def create_insight(
        self,
        title: str,
        category: str,
        insight: str,
        why: str,
        risk: str,
        recommendation: str,
        impact: str,
        priority: str,
        action_label: str,
        action_type: str,
        estimated_savings_usd: float = 0.0,
        action_params: Optional[Dict[str, Any]] = None
    ) -> AIInsight:
        self.recommendations_generated += 1
        item_id = f"INS-{self.agent_id[:3].upper()}-{int(time.time()*1000)%100000}"
        ai_insight = AIInsight(
            id=item_id,
            title=title,
            agent_source=self.name,
            category=category,
            insight=insight,
            why=why,
            risk=risk,
            recommendation=recommendation,
            impact=impact,
            priority=priority,
            estimated_savings_usd=estimated_savings_usd,
            action_label=action_label,
            action_type=action_type,
            action_params=action_params or {},
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_executed=False
        )
        self.active_insights.insert(0, ai_insight)
        if len(self.active_insights) > 20:
            self.active_insights = self.active_insights[:20]
        return ai_insight

    def create_alert(
        self,
        category: str,
        severity: str,
        location: str,
        title: str,
        description: str,
        ai_explanation: str,
        recommended_action: str,
        action_data: Optional[Dict[str, Any]] = None
    ) -> FacilityAlert:
        self.alerts_generated += 1
        alert_id = f"ALT-{category[:3].upper()}-{int(time.time()*1000)%100000}"
        alert = FacilityAlert(
            id=alert_id,
            category=category,
            severity=severity,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            location=location,
            source_agent=self.name,
            title=title,
            description=description,
            ai_explanation=ai_explanation,
            recommended_action=recommended_action,
            status="Active",
            action_data=action_data or {}
        )
        self.generated_alerts.insert(0, alert)
        if len(self.generated_alerts) > 50:
            self.generated_alerts = self.generated_alerts[:50]
        return alert
