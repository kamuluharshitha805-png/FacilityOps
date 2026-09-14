import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..db import models
from ..core.observability import log_event, record_metric

class OccupancyService:
    """Service for occupancy analytics and aggregation."""
    def __init__(self, db: Session):
        self.db = db

    def aggregate_occupancy(self, building_id: str, start: datetime.datetime, end: datetime.datetime) -> List[Dict[str, Any]]:
        """Aggregate occupancy events per zone per hour (stub implementation)."""
        rows = (
            self.db.query(
                models.OccupancyEvent.zone_id,
                models.OccupancyEvent.timestamp,
                models.OccupancyEvent.occupancy_count,
            )
            .join(models.Zone)
            .filter(
                models.Zone.building.has(models.Building.facility_id == building_id),
                models.OccupancyEvent.timestamp >= start,
                models.OccupancyEvent.timestamp <= end,
            )
            .all()
        )
        agg = {}
        for r in rows:
            hour = r.timestamp.replace(minute=0, second=0, microsecond=0)
            key = (r.zone_id, hour)
            if key not in agg:
                agg[key] = {"occupancy_sum": 0, "count": 0}
            agg[key]["occupancy_sum"] += float(r.occupancy_count or 0)
            agg[key]["count"] += 1
        result = []
        for (zone_id, hour), data in agg.items():
            cnt = data.pop("count")
            result.append({
                "zone_id": zone_id,
                "timestamp": hour.isoformat(),
                "average_occupancy": data["occupancy_sum"] / cnt,
            })
        log_event("occupancy_aggregate", building_id=building_id, start=start.isoformat(), end=end.isoformat(), count=len(result))
        record_metric("occupancy.aggregate.records", len(result), labels={"building_id": building_id})
        return result
