import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..db import models
from ..core.observability import log_event, record_metric

class EnergyService:
    """Service class for energy analytics operations."""

    def __init__(self, db: Session):
        self.db = db

    def aggregate_hourly(self, facility_id: str, start: datetime.datetime, end: datetime.datetime) -> List[Dict[str, Any]]:
        """Aggregate energy readings per zone per hour.
        Returns a list of dictionaries with averaged metrics.
        """
        rows = (
            self.db.query(
                models.EnergyReading.zone_id,
                models.EnergyReading.timestamp,
                models.EnergyReading.electricity_kw,
                models.EnergyReading.water_gpm,
                models.EnergyReading.hvac_kw,
                models.EnergyReading.demand_kw,
            )
            .join(models.Zone)
            .filter(
                models.Zone.building.has(models.Building.facility_id == facility_id),
                models.EnergyReading.timestamp >= start,
                models.EnergyReading.timestamp <= end,
            )
            .all()
        )
        # Simple aggregation by zone and hour
        agg: Dict[tuple, Dict[str, Any]] = {}
        for r in rows:
            hour = r.timestamp.replace(minute=0, second=0, microsecond=0)
            key = (r.zone_id, hour)
            if key not in agg:
                agg[key] = {"electricity_kw": 0.0, "water_gpm": 0.0, "hvac_kw": 0.0, "demand_kw": 0.0, "count": 0}
            agg[key]["electricity_kw"] += float(r.electricity_kw or 0)
            agg[key]["water_gpm"] += float(r.water_gpm or 0)
            agg[key]["hvac_kw"] += float(r.hvac_kw or 0)
            agg[key]["demand_kw"] += float(r.demand_kw or 0)
            agg[key]["count"] += 1
        result = []
        for (zone_id, hour), data in agg.items():
            cnt = data.pop("count")
            result.append({
                "zone_id": zone_id,
                "timestamp": hour.isoformat(),
                "electricity_kw": data["electricity_kw"] / cnt,
                "water_gpm": data["water_gpm"] / cnt,
                "hvac_kw": data["hvac_kw"] / cnt,
                "demand_kw": data["demand_kw"] / cnt,
            })
        log_event("energy_aggregate", facility_id=facility_id, start=start.isoformat(), end=end.isoformat(), count=len(result))
        record_metric("energy.aggregate.records", len(result), labels={"facility_id": facility_id})
        return result
