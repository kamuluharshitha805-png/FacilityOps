"""
Initial Database Seeder for FacilityOps.
Creates all database tables and populates facilities, buildings, zones, rooms,
assets, sensors, default RBAC users, and initial operational records.
"""

import logging
from datetime import datetime, timedelta
from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.config import FACILITY_ZONES, ASSET_REGISTRY
from app.db.models import (
    Facility, Building, Zone, Room, Asset, Sensor,
    EnergyReading, OccupancyEvent, SecurityEvent, WorkOrder, MaintenanceRecord, Alert, User
)

logger = logging.getLogger("facilityops.seed")

def seed_database():
    """Initializes schema and seeds baseline dataset if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Facility).first():
            logger.info("Database already initialized and seeded.")
            return

        logger.info("Seeding initial facility topology and relational data...")

        # 1. Facility & Building
        fac = Facility(
            facility_id="FAC-HQ-01",
            name="Apex Tower Global HQ",
            location="Metropolis Tech District, Sector 4",
            type="Commercial & Industrial R&D",
            status="Operational"
        )
        bld = Building(
            building_id="BLD-APEX-01",
            facility_id="FAC-HQ-01",
            name="Apex Main Tower",
            floors=5,
            total_area_sqft=285000
        )
        db.add(fac)
        db.add(bld)
        db.flush()

        # 2. Zones & Rooms
        for z in FACILITY_ZONES:
            zone_obj = Zone(
                zone_id=z["id"],
                building_id="BLD-APEX-01",
                floor=z["floor"],
                name=z["name"],
                zone_type=z["type"],
                security_tier=z["security"],
                area_sqft=z["area_sqft"],
                capacity=z["capacity"],
                hvac_setpoint_c=z["hvac_setpoint"]
            )
            db.add(zone_obj)
            db.flush()

            # Add 2 rooms per zone
            r1 = Room(
                room_id=f"RM-{z['id']}-A",
                zone_id=z["id"],
                name=f"{z['name']} - Primary Suite",
                capacity=int(z["capacity"] * 0.6),
                utilization_pct=45.0
            )
            r2 = Room(
                room_id=f"RM-{z['id']}-B",
                zone_id=z["id"],
                name=f"{z['name']} - Auxiliary Wing",
                capacity=int(z["capacity"] * 0.4),
                utilization_pct=30.0
            )
            db.add(r1)
            db.add(r2)

        # 3. Assets & Sensors
        for a in ASSET_REGISTRY:
            asset_obj = Asset(
                asset_id=a["id"],
                facility_id="FAC-HQ-01",
                building_id="BLD-APEX-01",
                zone_id=a["zone_id"],
                name=a["name"],
                asset_type=a["type"],
                criticality=a["criticality"],
                installation_date=f"{a['install_year']}-06-15",
                status="Healthy",
                health_score=94.5,
                condition_score=94.0,
                failure_probability_pct=4.2,
                rated_kw=a["rated_kw"],
                current_kw=round(a["rated_kw"] * 0.72, 1) if a["rated_kw"] > 0 else 0.0,
                vibration_rms=a["baseline_vibration"],
                baseline_vibration=a["baseline_vibration"],
                temperature_c=a["baseline_temp"],
                baseline_temp=a["baseline_temp"],
                rul_hours=18500.0,
                running_hours=8200.0
            )
            db.add(asset_obj)
            db.flush()

            # Attach telemetry sensors
            if a["rated_kw"] > 0:
                db.add(Sensor(
                    sensor_id=f"SNR-PWR-{a['id']}",
                    asset_id=a["id"],
                    zone_id=a["zone_id"],
                    sensor_type="Power",
                    unit="kW",
                    status="Online",
                    last_reading=asset_obj.current_kw
                ))
            db.add(Sensor(
                sensor_id=f"SNR-VIB-{a['id']}",
                asset_id=a["id"],
                zone_id=a["zone_id"],
                sensor_type="Vibration",
                unit="mm/s",
                status="Online",
                last_reading=asset_obj.vibration_rms
            ))
            db.add(Sensor(
                sensor_id=f"SNR-TMP-{a['id']}",
                asset_id=a["id"],
                zone_id=a["zone_id"],
                sensor_type="Temperature",
                unit="°C",
                status="Online",
                last_reading=asset_obj.temperature_c
            ))

        # 4. Default RBAC Users
        users = [
            User(
                id="USR-001",
                username="executive",
                hashed_password=hash_password("exec123"),
                role="Executive",
                full_name="Elena Vance, Chief Operating Officer",
                email="exec@apex.facilityops.io"
            ),
            User(
                id="USR-002",
                username="manager",
                hashed_password=hash_password("mgr123"),
                role="FacilityManager",
                full_name="Marcus Brody, Lead Facility Director",
                email="manager@apex.facilityops.io"
            ),
            User(
                id="USR-003",
                username="maintenance",
                hashed_password=hash_password("maint123"),
                role="MaintenanceTeam",
                full_name="David Miller, Senior Mechanical Engineer",
                email="maint@apex.facilityops.io"
            ),
            User(
                id="USR-004",
                username="security",
                hashed_password=hash_password("sec123"),
                role="SecurityTeam",
                full_name="Sarah Chen, Security Operations Chief",
                email="security@apex.facilityops.io"
            ),
        ]
        db.add_all(users)

        # 5. Initial Work Orders
        today_str = datetime.now().strftime("%Y-%m-%d")
        wos = [
            WorkOrder(
                id="WO-2026-101",
                asset_id="PMP-03",
                title="Seal Flush Inspection & Coupling Realignment",
                priority="Medium",
                assigned_team="Hydronics Specialist Team",
                status="Assigned",
                created_date=today_str,
                due_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                maintenance_action="Laser shaft realignment and seal cartridge inspection.",
                ai_trigger_reason="Vibration RMS elevated by 0.35 mm/s with 1X rotational frequency peak harmonics.",
                estimated_hours=3.5,
                estimated_cost_usd=650.0
            ),
            WorkOrder(
                id="WO-2026-102",
                asset_id="AHU-F2-01",
                title="HEPA Filter Differential Pressure & Belt Tension Check",
                priority="High",
                assigned_team="Cleanroom HVAC Controls Lead",
                status="In Progress",
                created_date=today_str,
                due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                maintenance_action="Verify filter delta-P and re-tension supply fan belts.",
                ai_trigger_reason="Filter delta-P increased to 1.4 in. w.g. Fan slip ratio +6%.",
                estimated_hours=4.0,
                estimated_cost_usd=1200.0
            )
        ]
        db.add_all(wos)

        # 6. Initial Security Events
        now = datetime.now()
        sec_events = [
            SecurityEvent(
                id="SEC-EV-901",
                zone_id="Z-F5-01",
                event_type="AccessDeniedBiometric",
                severity="Medium",
                timestamp=(now - timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
                source="MantrapBiometricReader",
                status="Logged",
                portal_id="MTRP-F5-01",
                details="Clearance denial level 4 on guest credential."
            ),
            SecurityEvent(
                id="SEC-EV-902",
                zone_id="Z-F1-03",
                event_type="DeliveryBayDoorCycle",
                severity="Information",
                timestamp=(now - timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S"),
                source="LogisticsPortal",
                status="Closed",
                portal_id="BAY-DOOR-02",
                details="Manifest plate match automated roller door open."
            )
        ]
        db.add_all(sec_events)

        # 7. Initial Alerts
        alerts = [
            Alert(
                id="ALT-MA-201",
                category="Maintenance",
                severity="Medium",
                timestamp=(now - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S"),
                location="Floor 5 Mechanical Penthouse (PMP-03)",
                source_agent="Predictive Maintenance Agent",
                title="Condenser Pump 1 Mechanical Coupling Degradation",
                description="Vibration elevated to 1.85 mm/s (+25% above nominal baseline).",
                evidence="Vibration sensor SNR-VIB-PMP-03 FFT spectrum reveals 1X harmonic peak.",
                ai_explanation="Mechanical shaft misalignment inducing harmonic resonance across bearing frame.",
                recommendation="Perform laser shaft realignment and check mechanical seal lubricity.",
                status="Assigned",
                assigned_to="Hydronics Specialist Team"
            ),
            Alert(
                id="ALT-EN-202",
                category="Energy",
                severity="Low",
                timestamp=(now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
                location="Floor 3 Telecommunications (Z-F3-05)",
                source_agent="Energy Intelligence Agent",
                title="VAV Duct Static Pressure Inefficiency",
                description="Static pressure operating at 1.8 in. w.g. despite VAV terminal damper positions <45%.",
                evidence="BMS telemetry indicates static pressure reset schedule locked to manual floor.",
                ai_explanation="Static pressure loop not responding dynamically to terminal damper demand.",
                recommendation="Enable Trim-and-Respond dynamic static pressure reset.",
                status="Created"
            )
        ]
        db.add_all(alerts)

        # 8. Initial Time-Series Energy & Occupancy points
        for i in range(12):
            t_str = (now - timedelta(hours=i)).strftime("%Y-%m-%d %H:00:00")
            db.add(EnergyReading(
                timestamp=t_str,
                zone_id="Z-F1-01",
                electricity_kw=145.0,
                water_gpm=12.5,
                hvac_kw=82.0,
                demand_kw=152.0
            ))
            db.add(OccupancyEvent(
                timestamp=t_str,
                zone_id="Z-F1-01",
                occupancy_count=78,
                utilization_pct=52.0
            ))

        db.commit()
        logger.info("Initial database seeding completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed database: {e}", exc_info=True)
        raise e
    finally:
        db.close()
