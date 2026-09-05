"""Pydantic data models for Telco NOC Optimizer."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TowerStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    WARNING = "WARNING"
    CONGESTED = "CONGESTED"
    CRITICAL_OVERLOAD = "CRITICAL_OVERLOAD"


class CellTowerMetrics(BaseModel):
    tower_id: str = Field(..., description="Unique cell tower identifier (e.g., TWR-5G-NY-01)")
    region: str = Field(..., description="Geographical deployment region (e.g., North-East, West)")
    carrier_band: str = Field(..., description="Frequency band (e.g., n78 3.5GHz, n258 mmWave)")
    connected_users: int = Field(..., description="Active RRC connected subscribers")
    prb_utilization_pct: float = Field(..., description="Physical Resource Block utilization percentage")
    latency_ms: float = Field(..., description="User-plane round-trip latency in milliseconds")
    packet_loss_pct: float = Field(..., description="User-plane packet loss percentage")
    status: TowerStatus = Field(..., description="Operational status based on 3GPP thresholds")
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MitigationType(str, Enum):
    LOAD_BALANCE_XN = "load_balance_xn"
    POWER_BOOST_MIMO = "power_boost_mimo"
    CARRIER_AGGREGATION_STEER = "carrier_aggregation_steer"
    REROUTE_TRAFFIC = "reroute_traffic"


class MitigationResult(BaseModel):
    ticket_id: str = Field(..., description="Audit incident ticket ID (e.g., NOC-INC-2026-XXXX)")
    tower_id: str = Field(..., description="Target cell tower ID")
    action_executed: MitigationType = Field(..., description="Action taken to mitigate network congestion")
    status: str = Field(..., description="Execution status: SUCCESS or FAILED")
    prb_reduction_pct: float = Field(..., description="Expected reduction in PRB load")
    projected_latency_ms: float = Field(..., description="Expected post-mitigation user plane latency")
    standard_applied: str = Field(..., description="3GPP reference standard guiding the action")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: Dict[str, Any] = Field(default_factory=dict)


class SLAImpactEstimate(BaseModel):
    tower_id: str = Field(..., description="Target cell tower ID")
    active_subscribers_impacted: int = Field(..., description="Subscribers suffering degraded QoS")
    estimated_penalty_usd: float = Field(..., description="Estimated SLA breach liability cost in USD")
    compliance_risk: str = Field(..., description="Risk level: LOW, MEDIUM, HIGH, or SEVERE")
    recommendation: str = Field(..., description="Remediation recommendation")
