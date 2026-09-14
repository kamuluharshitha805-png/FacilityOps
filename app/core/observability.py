"""
Observability, Structured Metrics & Performance Telemetry for FacilityOps.
Tracks API latencies, error rates, database health, and agent status.
"""

import time
import logging
from typing import Dict, Any, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("facilityops.observability")

class MetricsCollector:
    def __init__(self):
        self.total_requests: int = 0
        self.error_requests: int = 0
        self.latencies_ms: List[float] = []
        self.status_counts: Dict[str, int] = {}
        self.agent_latencies: Dict[str, float] = {}
        self.start_time = time.time()

    def record_request(self, status_code: int, duration_ms: float):
        self.total_requests += 1
        code_str = str(status_code)
        self.status_counts[code_str] = self.status_counts.get(code_str, 0) + 1
        if status_code >= 400:
            self.error_requests += 1
        
        self.latencies_ms.append(duration_ms)
        if len(self.latencies_ms) > 1000:
            self.latencies_ms = self.latencies_ms[-1000:]

    def record_agent_latency(self, agent_id: str, duration_ms: float):
        self.agent_latencies[agent_id] = round(duration_ms, 2)

    def get_summary(self) -> Dict[str, Any]:
        uptime_sec = time.time() - self.start_time
        avg_latency = sum(self.latencies_ms) / max(1, len(self.latencies_ms))
        sorted_latencies = sorted(self.latencies_ms)
        p95_latency = sorted_latencies[int(len(sorted_latencies) * 0.95)] if sorted_latencies else 0.0

        error_rate = (self.error_requests / max(1, self.total_requests)) * 100.0

        return {
            "uptime_seconds": round(uptime_sec, 1),
            "total_requests": self.total_requests,
            "error_requests": self.error_requests,
            "error_rate_pct": round(error_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "status_distribution": self.status_counts,
            "agent_latencies_ms": self.agent_latencies,
            "system_health": "Healthy" if error_rate < 5.0 else "Degraded"
        }

metrics = MetricsCollector()

class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.time()
        try:
            response = await call_next(request)
            duration = (time.time() - start) * 1000
            metrics.record_request(response.status_code, duration)
            response.headers["X-Response-Time-Ms"] = f"{duration:.2f}"
            return response
        except Exception as e:
            duration = (time.time() - start) * 1000
            metrics.record_request(500, duration)
            logger.error(f"Unhandled HTTP error on {request.url.path}: {e}", exc_info=True)
            raise e
