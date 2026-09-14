"""
Relational Database Models for FacilityOps Enterprise Data Platform.
Covers Facilities, Buildings, Zones, Rooms, Assets, Sensors, Time-series readings,
Maintenance records, Work Orders, Security Events, Alerts, Workflows, Audit logs, and Users.
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(200), nullable=False)
    type = Column(String(50), default="Commercial Office")
    status = Column(String(30), default="Operational")
    created_at = Column(DateTime, default=datetime.utcnow)

    buildings = relationship("Building", back_populates="facility", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="facility")

class Building(Base):
    __tablename__ = "buildings"

    building_id = Column(String(50), primary_key=True, index=True)
    facility_id = Column(String(50), ForeignKey("facilities.facility_id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    floors = Column(Integer, default=5)
    total_area_sqft = Column(Integer, default=285000)

    facility = relationship("Facility", back_populates="buildings")
    zones = relationship("Zone", back_populates="building", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="building")

class Zone(Base):
    __tablename__ = "zones"

    zone_id = Column(String(50), primary_key=True, index=True)
    building_id = Column(String(50), ForeignKey("buildings.building_id"), nullable=False, index=True)
    floor = Column(Integer, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    zone_type = Column(String(50), default="Office")  # Office, Laboratory, DataCenter, Mechanical, Lobby
    security_tier = Column(String(50), default="Operational")  # Public, Operational, Restricted, High-Security
    area_sqft = Column(Integer, default=10000)
    capacity = Column(Integer, default=100)
    hvac_setpoint_c = Column(Float, default=21.5)

    building = relationship("Building", back_populates="zones")
    rooms = relationship("Room", back_populates="zone", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="zone")
    energy_readings = relationship("EnergyReading", back_populates="zone")
    occupancy_events = relationship("OccupancyEvent", back_populates="zone")
    security_events = relationship("SecurityEvent", back_populates="zone")

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(String(50), primary_key=True, index=True)
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    capacity = Column(Integer, default=20)
    utilization_pct = Column(Float, default=0.0)

    zone = relationship("Zone", back_populates="rooms")

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(String(50), primary_key=True, index=True)
    facility_id = Column(String(50), ForeignKey("facilities.facility_id"), nullable=False)
    building_id = Column(String(50), ForeignKey("buildings.building_id"), nullable=False)
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    asset_type = Column(String(50), nullable=False)  # Chiller, Boiler, AHU, Pump, Transformer, Elevator, CRAC
    criticality = Column(String(30), default="Medium")  # Low, Medium, High, Critical
    installation_date = Column(String(30), default="2021-01-01")
    status = Column(String(30), default="Healthy")  # Healthy, Good, Warning, Critical
    health_score = Column(Float, default=95.0, index=True)
    condition_score = Column(Float, default=95.0)
    failure_probability_pct = Column(Float, default=5.0)
    rated_kw = Column(Float, default=50.0)
    current_kw = Column(Float, default=35.0)
    vibration_rms = Column(Float, default=1.0)
    baseline_vibration = Column(Float, default=1.0)
    temperature_c = Column(Float, default=45.0)
    baseline_temp = Column(Float, default=45.0)
    rul_hours = Column(Float, default=20000.0)
    running_hours = Column(Float, default=5000.0)

    facility = relationship("Facility", back_populates="assets")
    building = relationship("Building", back_populates="assets")
    zone = relationship("Zone", back_populates="assets")
    sensors = relationship("Sensor", back_populates="asset", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="asset")
    work_orders = relationship("WorkOrder", back_populates="asset")

class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(String(50), primary_key=True, index=True)
    asset_id = Column(String(50), ForeignKey("assets.asset_id"), nullable=True, index=True)
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=True, index=True)
    sensor_type = Column(String(50), nullable=False)  # Power, Temperature, Vibration, Flow, CO2, Humidity, Motion
    unit = Column(String(20), default="kW")
    status = Column(String(30), default="Online")  # Online, Degraded, Offline, Faulty
    last_reading = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="sensors")

class EnergyReading(Base):
    __tablename__ = "energy_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(30), nullable=False, index=True)
    facility_id = Column(String(50), default="FAC-HQ-01", index=True)
    building_id = Column(String(50), default="BLD-APEX-01")
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=False, index=True)
    electricity_kw = Column(Float, default=0.0)
    water_gpm = Column(Float, default=0.0)
    hvac_kw = Column(Float, default=0.0)
    demand_kw = Column(Float, default=0.0)

    zone = relationship("Zone", back_populates="energy_readings")

    __table_args__ = (
        Index("ix_energy_zone_time", "zone_id", "timestamp"),
    )

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String(50), ForeignKey("assets.asset_id"), nullable=False, index=True)
    maintenance_type = Column(String(50), default="Preventive")  # Predictive, Preventive, Corrective, Overhaul
    date = Column(String(30), nullable=False)
    technician = Column(String(100), default="Maintenance Staff")
    cost_usd = Column(Float, default=0.0)
    status = Column(String(30), default="Completed")
    notes = Column(Text, nullable=True)

    asset = relationship("Asset", back_populates="maintenance_records")

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(String(50), primary_key=True, index=True)
    asset_id = Column(String(50), ForeignKey("assets.asset_id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    priority = Column(String(30), default="Medium")  # Low, Medium, High, Critical
    assigned_team = Column(String(100), default="Mechanical")
    status = Column(String(30), default="Open")  # Open, Assigned, In Progress, Completed, Overdue
    created_date = Column(String(30), nullable=False)
    due_date = Column(String(30), nullable=False)
    completion_date = Column(String(30), nullable=True)
    maintenance_action = Column(Text, nullable=False)
    ai_trigger_reason = Column(Text, nullable=True)
    estimated_hours = Column(Float, default=3.0)
    estimated_cost_usd = Column(Float, default=500.0)

    asset = relationship("Asset", back_populates="work_orders")

class OccupancyEvent(Base):
    __tablename__ = "occupancy_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(30), nullable=False, index=True)
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=False, index=True)
    room_id = Column(String(50), nullable=True)
    occupancy_count = Column(Integer, default=0)
    utilization_pct = Column(Float, default=0.0)

    zone = relationship("Zone", back_populates="occupancy_events")

    __table_args__ = (
        Index("ix_occupancy_zone_time", "zone_id", "timestamp"),
    )

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String(50), primary_key=True, index=True)
    zone_id = Column(String(50), ForeignKey("zones.zone_id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)  # BadgeGranted, BadgeDenied, IntrusionDetected, Loitering, Tailgating
    severity = Column(String(30), default="Information", index=True)  # Information, Low, Medium, High, Critical
    timestamp = Column(String(30), nullable=False, index=True)
    source = Column(String(50), default="AccessControl")  # AccessControl, CCTV_Vision, PerimeterSensor
    status = Column(String(30), default="Logged")  # Logged, UnderInvestigation, Escorted, Closed
    portal_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)

    zone = relationship("Zone", back_populates="security_events")

    __table_args__ = (
        Index("ix_security_zone_time", "zone_id", "timestamp"),
    )

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(50), primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)  # Energy, Maintenance, Occupancy, Security, Cost, Facility Critical
    severity = Column(String(30), nullable=False, index=True)  # Information, Low, Medium, High, Critical
    timestamp = Column(String(30), nullable=False, index=True)
    location = Column(String(150), nullable=False)
    source_agent = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    ai_explanation = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    status = Column(String(30), default="Created", index=True)  # Created, Acknowledged, Assigned, Resolved, Closed
    acknowledged_by = Column(String(100), nullable=True)
    assigned_to = Column(String(100), nullable=True)
    resolved_at = Column(String(30), nullable=True)

    __table_args__ = (
        Index("ix_alert_cat_sev", "category", "severity"),
    )

class WorkflowAction(Base):
    __tablename__ = "workflow_actions"

    id = Column(String(50), primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)  # hvac_setpoint, dispatch_maint, security_lockdown, peak_shave
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    target_system = Column(String(100), default="BMS")
    payload_json = Column(Text, nullable=True)
    status = Column(String(30), default="PendingApproval", index=True)  # PendingApproval, Approved, Rejected, Executed
    requested_by = Column(String(100), default="AI Agent")
    approved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(String(50), nullable=True)
    username = Column(String(100), default="System")
    action = Column(String(100), nullable=False)  # Login, TriggerScenario, ApproveWorkflow, DispatchWorkOrder, UpdateSetpoint
    resource = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)  # Executive, FacilityManager, MaintenanceTeam, SecurityTeam
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
