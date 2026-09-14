"""
Configuration, topology, asset registry, and operational thresholds
for the Agentic FacilityOps AI Platform.
"""

from typing import Dict, List, Any

BUILDING_NAME = "Apex Tower Global HQ"
TOTAL_FLOORS = 5
TOTAL_AREA_SQFT = 285_000

# Security zone tiers
ZONE_SECURITY_PUBLIC = "Public"
ZONE_SECURITY_OPERATIONAL = "Operational"
ZONE_SECURITY_RESTRICTED = "Restricted"
ZONE_SECURITY_HIGH = "High-Security"

# Facility Zones (5 Floors, 24 Zones)
FACILITY_ZONES: List[Dict[str, Any]] = [
    # Floor 1
    {"id": "Z-F1-01", "floor": 1, "name": "Main Atrium & Reception", "type": "Lobby", "area_sqft": 12000, "security": ZONE_SECURITY_PUBLIC, "capacity": 150, "hvac_setpoint": 22.0},
    {"id": "Z-F1-02", "floor": 1, "name": "Visitor Cafeteria & Lounge", "type": "Dining", "area_sqft": 10000, "security": ZONE_SECURITY_PUBLIC, "capacity": 180, "hvac_setpoint": 21.5},
    {"id": "Z-F1-03", "floor": 1, "name": "Loading Dock & Logistics", "type": "Logistics", "area_sqft": 8000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 25, "hvac_setpoint": 20.0},
    {"id": "Z-F1-04", "floor": 1, "name": "Security Operations Center", "type": "Security", "area_sqft": 4000, "security": ZONE_SECURITY_HIGH, "capacity": 15, "hvac_setpoint": 21.0},
    {"id": "Z-F1-05", "floor": 1, "name": "Main Electrical Ingress", "type": "Utility", "area_sqft": 6000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 5, "hvac_setpoint": 20.0},

    # Floor 2
    {"id": "Z-F2-01", "floor": 2, "name": "Hardware R&D Lab Alpha", "type": "Laboratory", "area_sqft": 14000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 60, "hvac_setpoint": 20.5},
    {"id": "Z-F2-02", "floor": 2, "name": "Hardware R&D Lab Beta", "type": "Laboratory", "area_sqft": 14000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 60, "hvac_setpoint": 20.5},
    {"id": "Z-F2-03", "floor": 2, "name": "Prototype Clean Room", "type": "Cleanroom", "area_sqft": 6000, "security": ZONE_SECURITY_HIGH, "capacity": 12, "hvac_setpoint": 19.5},
    {"id": "Z-F2-04", "floor": 2, "name": "Engineering Collaborative Zone", "type": "Office", "area_sqft": 16000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 140, "hvac_setpoint": 22.0},

    # Floor 3
    {"id": "Z-F3-01", "floor": 3, "name": "Operations Open Office North", "type": "Office", "area_sqft": 18000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 180, "hvac_setpoint": 22.0},
    {"id": "Z-F3-02", "floor": 3, "name": "Operations Open Office South", "type": "Office", "area_sqft": 18000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 180, "hvac_setpoint": 22.0},
    {"id": "Z-F3-03", "floor": 3, "name": "Auditorium & Conference Hub", "type": "Conference", "area_sqft": 10000, "security": ZONE_SECURITY_PUBLIC, "capacity": 220, "hvac_setpoint": 21.0},
    {"id": "Z-F3-04", "floor": 3, "name": "Focus Pods & Meeting Suites", "type": "Conference", "area_sqft": 6000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 40, "hvac_setpoint": 21.5},
    {"id": "Z-F3-05", "floor": 3, "name": "Floor 3 Telecommunications Closet", "type": "IT", "area_sqft": 2000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 4, "hvac_setpoint": 19.0},

    # Floor 4
    {"id": "Z-F4-01", "floor": 4, "name": "Executive Boardroom Suite", "type": "Executive", "area_sqft": 8000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 40, "hvac_setpoint": 21.5},
    {"id": "Z-F4-02", "floor": 4, "name": "C-Suite Executive Offices", "type": "Executive", "area_sqft": 14000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 50, "hvac_setpoint": 21.5},
    {"id": "Z-F4-03", "floor": 4, "name": "Global Strategy Briefing Room", "type": "Conference", "area_sqft": 6000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 35, "hvac_setpoint": 21.0},
    {"id": "Z-F4-04", "floor": 4, "name": "Legal & Finance Workspace", "type": "Office", "area_sqft": 14000, "security": ZONE_SECURITY_OPERATIONAL, "capacity": 110, "hvac_setpoint": 22.0},
    {"id": "Z-F4-05", "floor": 4, "name": "Executive Private Terrace", "type": "Lounge", "area_sqft": 8000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 60, "hvac_setpoint": 22.5},

    # Floor 5
    {"id": "Z-F5-01", "floor": 5, "name": "Mission Critical Data Center Alpha", "type": "DataCenter", "area_sqft": 16000, "security": ZONE_SECURITY_HIGH, "capacity": 20, "hvac_setpoint": 18.5},
    {"id": "Z-F5-02", "floor": 5, "name": "Data Center Backup UPS & Batteries", "type": "Utility", "area_sqft": 8000, "security": ZONE_SECURITY_HIGH, "capacity": 10, "hvac_setpoint": 19.0},
    {"id": "Z-F5-03", "floor": 5, "name": "Chiller Plant & Mechanical Penthouse", "type": "Mechanical", "area_sqft": 16000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 15, "hvac_setpoint": 20.0},
    {"id": "Z-F5-04", "floor": 5, "name": "Cooling Tower Deck", "type": "Rooftop", "area_sqft": 12000, "security": ZONE_SECURITY_RESTRICTED, "capacity": 10, "hvac_setpoint": 24.0},
    {"id": "Z-F5-05", "floor": 5, "name": "Primary Substation & Generator Room", "type": "Utility", "area_sqft": 8000, "security": ZONE_SECURITY_HIGH, "capacity": 8, "hvac_setpoint": 20.0},
]

# Asset Registry (50+ Industrial Assets)
ASSET_REGISTRY: List[Dict[str, Any]] = [
    # HVAC Chillers & Boilers
    {"id": "CH-01", "name": "Centrifugal Water Chiller 1 (Base)", "type": "Chiller", "zone_id": "Z-F5-03", "criticality": "Critical", "rated_kw": 420.0, "rated_cop": 5.8, "install_year": 2021, "baseline_vibration": 1.2, "baseline_temp": 48.0},
    {"id": "CH-02", "name": "Centrifugal Water Chiller 2 (Peak)", "type": "Chiller", "zone_id": "Z-F5-03", "criticality": "Critical", "rated_kw": 420.0, "rated_cop": 5.6, "install_year": 2020, "baseline_vibration": 1.4, "baseline_temp": 50.0},
    {"id": "CH-03", "name": "Magnetic Bearing Chiller 3 (Redundant)", "type": "Chiller", "zone_id": "Z-F5-03", "criticality": "High", "rated_kw": 350.0, "rated_cop": 6.2, "install_year": 2023, "baseline_vibration": 0.8, "baseline_temp": 44.0},
    {"id": "BLR-01", "name": "Condensing Hydronic Boiler 1", "type": "Boiler", "zone_id": "Z-F5-03", "criticality": "High", "rated_kw": 280.0, "rated_cop": 3.9, "install_year": 2021, "baseline_vibration": 1.0, "baseline_temp": 72.0},
    {"id": "BLR-02", "name": "Condensing Hydronic Boiler 2", "type": "Boiler", "zone_id": "Z-F5-03", "criticality": "Medium", "rated_kw": 280.0, "rated_cop": 3.8, "install_year": 2021, "baseline_vibration": 1.1, "baseline_temp": 71.0},

    # Cooling Towers
    {"id": "CT-01", "name": "Induced Draft Cooling Tower 1", "type": "CoolingTower", "zone_id": "Z-F5-04", "criticality": "High", "rated_kw": 75.0, "rated_cop": 4.5, "install_year": 2020, "baseline_vibration": 1.8, "baseline_temp": 32.0},
    {"id": "CT-02", "name": "Induced Draft Cooling Tower 2", "type": "CoolingTower", "zone_id": "Z-F5-04", "criticality": "High", "rated_kw": 75.0, "rated_cop": 4.5, "install_year": 2020, "baseline_vibration": 1.7, "baseline_temp": 33.0},

    # Primary & Secondary Water Pumps
    {"id": "PMP-01", "name": "Chilled Water Primary Pump 1", "type": "Pump", "zone_id": "Z-F5-03", "criticality": "High", "rated_kw": 45.0, "rated_cop": 4.0, "install_year": 2021, "baseline_vibration": 1.3, "baseline_temp": 42.0},
    {"id": "PMP-02", "name": "Chilled Water Primary Pump 2", "type": "Pump", "zone_id": "Z-F5-03", "criticality": "High", "rated_kw": 45.0, "rated_cop": 4.0, "install_year": 2021, "baseline_vibration": 1.4, "baseline_temp": 43.0},
    {"id": "PMP-03", "name": "Condenser Water Pump 1", "type": "Pump", "zone_id": "Z-F5-03", "criticality": "Medium", "rated_kw": 37.0, "rated_cop": 3.9, "install_year": 2020, "baseline_vibration": 1.5, "baseline_temp": 45.0},
    {"id": "PMP-04", "name": "Condenser Water Pump 2", "type": "Pump", "zone_id": "Z-F5-03", "criticality": "Medium", "rated_kw": 37.0, "rated_cop": 3.9, "install_year": 2020, "baseline_vibration": 1.4, "baseline_temp": 44.0},
    {"id": "PMP-05", "name": "Domestic Water Booster Pump A", "type": "Pump", "zone_id": "Z-F1-05", "criticality": "Medium", "rated_kw": 22.0, "rated_cop": 3.5, "install_year": 2022, "baseline_vibration": 1.1, "baseline_temp": 38.0},
    {"id": "PMP-06", "name": "Domestic Water Booster Pump B", "type": "Pump", "zone_id": "Z-F1-05", "criticality": "Medium", "rated_kw": 22.0, "rated_cop": 3.5, "install_year": 2022, "baseline_vibration": 1.0, "baseline_temp": 37.0},

    # Air Handling Units (AHU-01 to AHU-08)
    {"id": "AHU-F1-01", "name": "Floor 1 Atrium VAV AHU", "type": "AHU", "zone_id": "Z-F1-01", "criticality": "Medium", "rated_kw": 30.0, "rated_cop": 4.2, "install_year": 2021, "baseline_vibration": 1.2, "baseline_temp": 35.0},
    {"id": "AHU-F1-02", "name": "Floor 1 Logistics & Ops AHU", "type": "AHU", "zone_id": "Z-F1-03", "criticality": "Medium", "rated_kw": 25.0, "rated_cop": 4.0, "install_year": 2021, "baseline_vibration": 1.1, "baseline_temp": 34.0},
    {"id": "AHU-F2-01", "name": "Floor 2 Labs Clean Supply AHU", "type": "AHU", "zone_id": "Z-F2-01", "criticality": "Critical", "rated_kw": 45.0, "rated_cop": 4.5, "install_year": 2022, "baseline_vibration": 0.9, "baseline_temp": 31.0},
    {"id": "AHU-F2-02", "name": "Floor 2 Engineering Core AHU", "type": "AHU", "zone_id": "Z-F2-04", "criticality": "Medium", "rated_kw": 35.0, "rated_cop": 4.1, "install_year": 2021, "baseline_vibration": 1.2, "baseline_temp": 35.0},
    {"id": "AHU-F3-01", "name": "Floor 3 North Wing AHU", "type": "AHU", "zone_id": "Z-F3-01", "criticality": "Medium", "rated_kw": 40.0, "rated_cop": 4.2, "install_year": 2020, "baseline_vibration": 1.3, "baseline_temp": 36.0},
    {"id": "AHU-F3-02", "name": "Floor 3 South Wing AHU", "type": "AHU", "zone_id": "Z-F3-02", "criticality": "Medium", "rated_kw": 40.0, "rated_cop": 4.1, "install_year": 2020, "baseline_vibration": 1.4, "baseline_temp": 37.0},
    {"id": "AHU-F4-01", "name": "Floor 4 Executive Wing AHU", "type": "AHU", "zone_id": "Z-F4-01", "criticality": "High", "rated_kw": 30.0, "rated_cop": 4.6, "install_year": 2022, "baseline_vibration": 0.8, "baseline_temp": 30.0},
    {"id": "AHU-F4-02", "name": "Floor 4 Conference & Boardroom AHU", "type": "AHU", "zone_id": "Z-F4-03", "criticality": "Medium", "rated_kw": 25.0, "rated_cop": 4.3, "install_year": 2022, "baseline_vibration": 0.9, "baseline_temp": 32.0},

    # Data Center Precision CRACs (CRAC-01 to CRAC-04)
    {"id": "CRAC-01", "name": "Mission Data Center CRAC 1", "type": "CRAC", "zone_id": "Z-F5-01", "criticality": "Critical", "rated_kw": 65.0, "rated_cop": 4.8, "install_year": 2023, "baseline_vibration": 0.7, "baseline_temp": 28.0},
    {"id": "CRAC-02", "name": "Mission Data Center CRAC 2", "type": "CRAC", "zone_id": "Z-F5-01", "criticality": "Critical", "rated_kw": 65.0, "rated_cop": 4.8, "install_year": 2023, "baseline_vibration": 0.8, "baseline_temp": 29.0},
    {"id": "CRAC-03", "name": "Mission Data Center CRAC 3", "type": "CRAC", "zone_id": "Z-F5-01", "criticality": "Critical", "rated_kw": 65.0, "rated_cop": 4.7, "install_year": 2023, "baseline_vibration": 0.7, "baseline_temp": 28.0},
    {"id": "CRAC-04", "name": "Mission Data Center CRAC 4 (Standby)", "type": "CRAC", "zone_id": "Z-F5-01", "criticality": "Critical", "rated_kw": 65.0, "rated_cop": 4.9, "install_year": 2023, "baseline_vibration": 0.6, "baseline_temp": 27.0},

    # Electrical Substation, Switchgear & Transformers
    {"id": "XFMR-01", "name": "Main Step-Down Transformer 2.5MVA", "type": "Transformer", "zone_id": "Z-F1-05", "criticality": "Critical", "rated_kw": 2500.0, "rated_cop": 1.0, "install_year": 2019, "baseline_vibration": 0.5, "baseline_temp": 62.0},
    {"id": "XFMR-02", "name": "Redundant Transformer 2.5MVA", "type": "Transformer", "zone_id": "Z-F5-05", "criticality": "Critical", "rated_kw": 2500.0, "rated_cop": 1.0, "install_year": 2021, "baseline_vibration": 0.4, "baseline_temp": 58.0},
    {"id": "SWG-01", "name": "Main 480V Switchgear Lineup", "type": "Switchgear", "zone_id": "Z-F1-05", "criticality": "Critical", "rated_kw": 3000.0, "rated_cop": 1.0, "install_year": 2019, "baseline_vibration": 0.2, "baseline_temp": 38.0},
    {"id": "UPS-01", "name": "Central Modular Double-Conversion UPS 1", "type": "UPS", "zone_id": "Z-F5-02", "criticality": "Critical", "rated_kw": 800.0, "rated_cop": 1.0, "install_year": 2022, "baseline_vibration": 0.1, "baseline_temp": 33.0},
    {"id": "UPS-02", "name": "Central Modular Double-Conversion UPS 2", "type": "UPS", "zone_id": "Z-F5-02", "criticality": "Critical", "rated_kw": 800.0, "rated_cop": 1.0, "install_year": 2022, "baseline_vibration": 0.1, "baseline_temp": 32.0},
    {"id": "GEN-01", "name": "Emergency Diesel Generator 2000kW A", "type": "Generator", "zone_id": "Z-F5-05", "criticality": "Critical", "rated_kw": 2000.0, "rated_cop": 1.0, "install_year": 2020, "baseline_vibration": 0.2, "baseline_temp": 25.0},
    {"id": "GEN-02", "name": "Emergency Diesel Generator 2000kW B", "type": "Generator", "zone_id": "Z-F5-05", "criticality": "Critical", "rated_kw": 2000.0, "rated_cop": 1.0, "install_year": 2020, "baseline_vibration": 0.2, "baseline_temp": 24.0},

    # Vertical Conveyance / Elevators
    {"id": "ELV-01", "name": "High-Speed Passenger Elevator 1", "type": "Elevator", "zone_id": "Z-F1-01", "criticality": "Medium", "rated_kw": 28.0, "rated_cop": 1.0, "install_year": 2020, "baseline_vibration": 1.0, "baseline_temp": 32.0},
    {"id": "ELV-02", "name": "High-Speed Passenger Elevator 2", "type": "Elevator", "zone_id": "Z-F1-01", "criticality": "Medium", "rated_kw": 28.0, "rated_cop": 1.0, "install_year": 2020, "baseline_vibration": 1.1, "baseline_temp": 33.0},
    {"id": "ELV-03", "name": "High-Speed Passenger Elevator 3", "type": "Elevator", "zone_id": "Z-F1-01", "criticality": "Medium", "rated_kw": 28.0, "rated_cop": 1.0, "install_year": 2020, "baseline_vibration": 0.9, "baseline_temp": 31.0},
    {"id": "ELV-04", "name": "Heavy Freight Elevator 4", "type": "Elevator", "zone_id": "Z-F1-03", "criticality": "High", "rated_kw": 45.0, "rated_cop": 1.0, "install_year": 2019, "baseline_vibration": 1.6, "baseline_temp": 36.0},

    # Main Utility Ingress Meters
    {"id": "MTR-ELEC-MAIN", "name": "Grid Utility Primary Feeder Smart Meter", "type": "Meter", "zone_id": "Z-F1-05", "criticality": "Critical", "rated_kw": 4000.0, "rated_cop": 1.0, "install_year": 2022, "baseline_vibration": 0.0, "baseline_temp": 28.0},
    {"id": "MTR-WATER-MAIN", "name": "Municipal Water Main Digital Ultrasonic Meter", "type": "Meter", "zone_id": "Z-F1-05", "criticality": "Critical", "rated_kw": 0.0, "rated_cop": 1.0, "install_year": 2021, "baseline_vibration": 0.0, "baseline_temp": 20.0},
    {"id": "MTR-WATER-ROOF", "name": "Cooling Tower Make-Up Water Sub-Meter", "type": "Meter", "zone_id": "Z-F5-04", "criticality": "High", "rated_kw": 0.0, "rated_cop": 1.0, "install_year": 2021, "baseline_vibration": 0.0, "baseline_temp": 22.0},
]

# Economic & Carbon Parameters
TARIFF_CONFIG = {
    "peak_kwh_rate": 0.245,        # $ / kWh during 12:00 - 18:00
    "standard_kwh_rate": 0.165,    # $ / kWh during 08:00 - 12:00 & 18:00 - 22:00
    "offpeak_kwh_rate": 0.098,     # $ / kWh during 22:00 - 08:00
    "water_rate_per_gal": 0.0055,  # $ / gallon ($5.50 per 1000 gal)
    "carbon_kg_per_kwh": 0.385,    # Scope 2 grid emissions factor (kg CO2e / kWh)
}

# Facility Health Score Weights
HEALTH_SCORE_WEIGHTS = {
    "energy": 0.20,
    "maintenance": 0.25,
    "occupancy": 0.15,
    "security": 0.15,
    "cost": 0.15,
    "sustainability": 0.10,
}
