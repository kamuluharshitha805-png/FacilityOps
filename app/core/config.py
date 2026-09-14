"""
Enterprise Configuration Management for FacilityOps AI Platform.
Supports environment variable overrides via Pydantic BaseSettings.
"""

from typing import Dict, List, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic FacilityOps AI Platform"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    
    # Relational Database Configuration
    DATABASE_URL: str = Field(default=f"sqlite:///{BASE_DIR / 'facilityops.db'}", validation_alias="DATABASE_URL")
    DB_ECHO: bool = False
    
    # Security & JWT Authentication
    JWT_SECRET_KEY: str = Field(default="facilityops-enterprise-secret-key-super-secure-2026", validation_alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Rate Limiting & Safety
    MAX_REQUESTS_PER_MINUTE: int = 300
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SEC: float = 30.0
    
    # Facility Topology Defaults
    DEFAULT_FACILITY_ID: str = "FAC-HQ-01"
    DEFAULT_FACILITY_NAME: str = "Apex Tower Global HQ"
    DEFAULT_BUILDING_ID: str = "BLD-APEX-01"
    
    # Utility Tariffs ($/unit)
    TARIFF_PEAK_KWH: float = 0.245
    TARIFF_STANDARD_KWH: float = 0.165
    TARIFF_OFFPEAK_KWH: float = 0.098
    TARIFF_WATER_GAL: float = 0.0055
    GRID_CARBON_FACTOR_KG_KWH: float = 0.385
    
    # Facility Health Score Weights (must sum to 1.0)
    WEIGHT_ENERGY: float = 0.20
    WEIGHT_MAINTENANCE: float = 0.25
    WEIGHT_OCCUPANCY: float = 0.15
    WEIGHT_SECURITY: float = 0.15
    WEIGHT_COST: float = 0.15
    WEIGHT_SUSTAINABILITY: float = 0.10

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
