"""
Database CRUD and Repository Access Layer for FacilityOps.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models import (
    Facility, Building, Zone, Room, Asset, Sensor,
    EnergyReading, MaintenanceRecord, WorkOrder, OccupancyEvent, SecurityEvent,
    Alert, WorkflowAction, AuditLog, User
)

def log_audit(db: Session, action: str, resource: str, details: str = "", username: str = "System", user_id: str = None):
    """Writes an entry to the audit log."""
    log = AuditLog(
        timestamp=datetime.utcnow(),
        user_id=user_id,
        username=username,
        action=action,
        resource=resource,
        details=details
    )
    db.add(log)
    db.commit()

# Facility & Building
def get_facility(db: Session, facility_id: str = "FAC-HQ-01") -> Optional[Facility]:
    return db.query(Facility).filter(Facility.facility_id == facility_id).first()

def get_zones(db: Session, floor: Optional[int] = None) -> List[Zone]:
    q = db.query(Zone)
    if floor is not None:
        q = q.filter(Zone.floor == floor)
    return q.all()

def get_zone_by_id(db: Session, zone_id: str) -> Optional[Zone]:
    return db.query(Zone).filter(Zone.zone_id == zone_id).first()

# Assets
def get_assets(db: Session, criticality: Optional[str] = None, status: Optional[str] = None) -> List[Asset]:
    q = db.query(Asset)
    if criticality:
        q = q.filter(Asset.criticality == criticality)
    if status:
        q = q.filter(Asset.status == status)
    return q.all()

def get_asset_by_id(db: Session, asset_id: str) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.asset_id == asset_id).first()

def update_asset_telemetry(db: Session, asset_id: str, vibration: float, temp: float, kw: float, health: float) -> Optional[Asset]:
    asset = get_asset_by_id(db, asset_id)
    if asset:
        asset.vibration_rms = vibration
        asset.temperature_c = temp
        asset.current_kw = kw
        asset.health_score = health
        asset.status = "Critical" if health < 50 else "Warning" if health < 70 else "Good" if health < 85 else "Healthy"
        db.commit()
        db.refresh(asset)
    return asset

# Work Orders
def get_work_orders(db: Session, status: Optional[str] = None) -> List[WorkOrder]:
    q = db.query(WorkOrder).order_by(desc(WorkOrder.created_date))
    if status:
        q = q.filter(WorkOrder.status == status)
    return q.all()

def create_work_order(db: Session, wo_data: Dict[str, Any], created_by: str = "System") -> WorkOrder:
    wo = WorkOrder(
        id=wo_data.get("id", f"WO-2026-{int(datetime.utcnow().timestamp())%100000}"),
        asset_id=wo_data["asset_id"],
        title=wo_data["title"],
        priority=wo_data.get("priority", "Medium"),
        assigned_team=wo_data.get("assigned_team", "Mechanical"),
        status="Open",
        created_date=datetime.now().strftime("%Y-%m-%d"),
        due_date=wo_data.get("due_date", (datetime.now()).strftime("%Y-%m-%d")),
        maintenance_action=wo_data.get("maintenance_action", "Predictive intervention"),
        ai_trigger_reason=wo_data.get("ai_trigger_reason", "AI Condition-based Alert"),
        estimated_hours=float(wo_data.get("estimated_hours", 3.0)),
        estimated_cost_usd=float(wo_data.get("estimated_cost_usd", 500.0))
    )
    db.add(wo)
    db.commit()
    db.refresh(wo)
    log_audit(db, "CreateWorkOrder", f"WorkOrder:{wo.id}", f"Dispatched for asset {wo.asset_id}", username=created_by)
    return wo

def update_work_order_status(db: Session, wo_id: str, new_status: str, updated_by: str = "System") -> Optional[WorkOrder]:
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if wo:
        wo.status = new_status
        if new_status == "Completed":
            wo.completion_date = datetime.now().strftime("%Y-%m-%d")
        db.commit()
        db.refresh(wo)
        log_audit(db, "UpdateWorkOrderStatus", f"WorkOrder:{wo_id}", f"Status transitioned to {new_status}", username=updated_by)
    return wo

# Alerts
def get_alerts(db: Session, category: Optional[str] = None, severity: Optional[str] = None, status: Optional[str] = None) -> List[Alert]:
    q = db.query(Alert).order_by(desc(Alert.timestamp))
    if category and category != "All":
        q = q.filter(Alert.category == category)
    if severity and severity != "All":
        q = q.filter(Alert.severity == severity)
    if status and status != "All":
        q = q.filter(Alert.status == status)
    return q.all()

def create_alert(db: Session, alert_data: Dict[str, Any]) -> Alert:
    alert = Alert(
        id=alert_data.get("id", f"ALT-{int(datetime.utcnow().timestamp()*1000)%1000000}"),
        category=alert_data["category"],
        severity=alert_data.get("severity", "Medium"),
        timestamp=alert_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        location=alert_data.get("location", "Building Wide"),
        source_agent=alert_data.get("source_agent", "Orchestrator"),
        title=alert_data["title"],
        description=alert_data["description"],
        evidence=alert_data.get("evidence", ""),
        ai_explanation=alert_data.get("ai_explanation", ""),
        recommendation=alert_data.get("recommendation", ""),
        status="Created"
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def update_alert_status(db: Session, alert_id: str, new_status: str, user: str = "System", assigned_to: str = None) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = new_status
        if new_status == "Acknowledged":
            alert.acknowledged_by = user
        elif new_status == "Assigned" and assigned_to:
            alert.assigned_to = assigned_to
        elif new_status in ["Resolved", "Closed"]:
            alert.resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.commit()
        db.refresh(alert)
        log_audit(db, "UpdateAlertStatus", f"Alert:{alert_id}", f"Status changed to {new_status} by {user}", username=user)
    return alert

# Workflows
def create_workflow_action(db: Session, action_data: Dict[str, Any], requested_by: str = "AI Agent") -> WorkflowAction:
    wf = WorkflowAction(
        id=action_data.get("id", f"WFA-{int(datetime.utcnow().timestamp()*1000)%1000000}"),
        action_type=action_data["action_type"],
        title=action_data["title"],
        description=action_data["description"],
        target_system=action_data.get("target_system", "BMS"),
        payload_json=action_data.get("payload_json", "{}"),
        status="PendingApproval",
        requested_by=requested_by
    )
    db.add(wf)
    db.commit()
    db.refresh(wf)
    log_audit(db, "CreateWorkflowAction", f"WorkflowAction:{wf.id}", f"Requires human approval: {wf.title}", username=requested_by)
    return wf

def approve_workflow_action(db: Session, wf_id: str, approved_by: str) -> Optional[WorkflowAction]:
    wf = db.query(WorkflowAction).filter(WorkflowAction.id == wf_id).first()
    if wf and wf.status == "PendingApproval":
        wf.status = "Approved"
        wf.approved_by = approved_by
        wf.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(wf)
        log_audit(db, "ApproveWorkflowAction", f"WorkflowAction:{wf_id}", f"Approved by {approved_by}", username=approved_by)
    return wf

def reject_workflow_action(db: Session, wf_id: str, rejected_by: str) -> Optional[WorkflowAction]:
    wf = db.query(WorkflowAction).filter(WorkflowAction.id == wf_id).first()
    if wf and wf.status == "PendingApproval":
        wf.status = "Rejected"
        wf.approved_by = rejected_by
        wf.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(wf)
        log_audit(db, "RejectWorkflowAction", f"WorkflowAction:{wf_id}", f"Rejected by {rejected_by}", username=rejected_by)
    return wf

# Ingestion records
def record_energy(db: Session, reading: Dict[str, Any]) -> EnergyReading:
    er = EnergyReading(
        timestamp=reading.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        facility_id=reading.get("facility_id", "FAC-HQ-01"),
        building_id=reading.get("building_id", "BLD-APEX-01"),
        zone_id=reading["zone_id"],
        electricity_kw=float(reading.get("electricity_kw", 0.0)),
        water_gpm=float(reading.get("water_gpm", 0.0)),
        hvac_kw=float(reading.get("hvac_kw", 0.0)),
        demand_kw=float(reading.get("demand_kw", 0.0))
    )
    db.add(er)
    db.commit()
    return er

def record_occupancy(db: Session, event: Dict[str, Any]) -> OccupancyEvent:
    oe = OccupancyEvent(
        timestamp=event.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        zone_id=event["zone_id"],
        room_id=event.get("room_id"),
        occupancy_count=int(event.get("occupancy_count", 0)),
        utilization_pct=float(event.get("utilization_pct", 0.0))
    )
    db.add(oe)
    db.commit()
    return oe

def record_security_event(db: Session, event: Dict[str, Any]) -> SecurityEvent:
    se = SecurityEvent(
        id=event.get("id", f"SEC-{int(datetime.utcnow().timestamp()*1000)%1000000}"),
        zone_id=event["zone_id"],
        event_type=event["event_type"],
        severity=event.get("severity", "Information"),
        timestamp=event.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        source=event.get("source", "AccessControl"),
        status=event.get("status", "Logged"),
        portal_id=event.get("portal_id"),
        details=event.get("details")
    )
    db.add(se)
    db.commit()
    return se

# Users
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username, User.is_active == True).first()
