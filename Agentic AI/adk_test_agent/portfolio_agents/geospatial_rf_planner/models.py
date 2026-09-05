"""Pydantic models for Geospatial RF Planner."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    MODERATE = "MODERATE"
    LOW = "LOW"


class CellSiteLocation(BaseModel):
    site_id: str = Field(..., description="Unique cell site identifier (e.g., SITE-NYC-001)")
    name: str = Field(..., description="Descriptive site location name")
    region: str = Field(..., description="Metropolitan borough or administrative region")
    latitude: float = Field(..., description="WGS84 latitude coordinate in decimal degrees")
    longitude: float = Field(..., description="WGS84 longitude coordinate in decimal degrees")
    band: str = Field(..., description="Deployed frequency carrier band")
    azimuth_deg: int = Field(..., description="Antenna main beam bore-sight azimuth angle (0-359 degrees)")
    tilt_deg: float = Field(..., description="Antenna mechanical and electrical tilt angle in degrees")
    height_m: float = Field(..., description="Antenna height Above Ground Level (AGL) in meters")
    tx_power_dbm: float = Field(..., description="Equivalent Isotropically Radiated Power (EIRP) in dBm")
    coverage_radius_m: float = Field(..., description="Effective nominal coverage radius in meters")


class CoverageHole(BaseModel):
    hole_id: str = Field(..., description="Unique coverage gap identifier (e.g., GAP-4070-7401)")
    latitude: float = Field(..., description="Centroid latitude of dark spot")
    longitude: float = Field(..., description="Centroid longitude of dark spot")
    radius_m: float = Field(..., description="Radius of unserved zone in meters")
    estimated_rsrp_dbm: float = Field(..., description="Estimated Reference Signal Received Power in dBm (< -105 dBm)")
    severity: SeverityLevel = Field(..., description="Coverage impairment severity")
    nearest_serving_site: str = Field(..., description="Nearest cell site id")


class InterferenceAnalysis(BaseModel):
    source_site: str = Field(..., description="Evaluating transmitter site ID")
    interfering_site: str = Field(..., description="Adjacent interfering site ID")
    separation_distance_m: float = Field(..., description="Inter-site physical distance in meters")
    angular_overlap_deg: float = Field(..., description="Bore-sight beam collision angle in degrees")
    sinr_penalty_db: float = Field(..., description="Signal-to-Interference-plus-Noise-Ratio degradation in dB")
    collision_risk: SeverityLevel = Field(..., description="Risk of pilot pollution and throughput loss")


class AntennaOptimizationPlan(BaseModel):
    site_id: str = Field(..., description="Target cell site ID")
    current_azimuth_deg: int = Field(..., description="Baseline azimuth angle")
    recommended_azimuth_deg: int = Field(..., description="Optimized azimuth angle to eliminate blind spot")
    current_tilt_deg: float = Field(..., description="Baseline antenna downtilt")
    recommended_tilt_deg: float = Field(..., description="Recommended electrical downtilt to control overshooting")
    expected_sinr_gain_db: float = Field(..., description="Predicted SINR improvement in dB")
    expected_coverage_lift_pct: float = Field(..., description="Predicted footprint expansion percentage")
    rationale: str = Field(..., description="Engineering explanation of spatial adjustment")


class GeoJSONFeature(BaseModel):
    type: str = Field(default="Feature")
    geometry: Dict[str, Any] = Field(..., description="GeoJSON geometry object (Point, Polygon)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Feature attributes and telemetry")


class GeoJSONFeatureCollection(BaseModel):
    type: str = Field(default="FeatureCollection")
    features: List[GeoJSONFeature] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
