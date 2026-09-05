"""Pydantic data models for Autonomous SecOps Swarm."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ThreatSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AttackType(str, Enum):
    DDOS_AMPLIFICATION = "DDOS_AMPLIFICATION"
    SQL_INJECTION = "SQL_INJECTION"
    CREDENTIAL_STUFFING = "CREDENTIAL_STUFFING"
    API_TELECOM_ABUSE = "API_TELECOM_ABUSE"


class ThreatFeedEntry(BaseModel):
    threat_id: str = Field(..., description="Unique threat intelligence ID (e.g., THR-2026-081)")
    ip_address: str = Field(..., description="Malicious source IPv4/IPv6 address")
    attack_type: AttackType = Field(..., description="Classified attack vector")
    severity: ThreatSeverity = Field(..., description="Risk severity tier")
    confidence_score: float = Field(..., description="Detection confidence score (0.0 to 1.0)")
    source_country: str = Field(..., description="GeoIP attribution")
    payload_sample: str = Field(..., description="Extracted malicious payload or signature excerpt")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class FirewallRule(BaseModel):
    rule_id: str = Field(..., description="Generated edge firewall ACL identifier (e.g., FW-RULE-8841)")
    target_ip: str = Field(..., description="Blocked or rate-limited IP address")
    rule_type: str = Field(..., description="ACL policy type: EDGE_DROP, BGP_FLOWSPEC, or RATE_LIMIT")
    action: str = Field(..., description="Action: DROP, REJECT, RATE_LIMIT, or BLACKHOLE")
    duration_minutes: int = Field(default=60, description="Active lease TTL in minutes")
    router_applied: str = Field(..., description="Edge perimeter router executing the rule")
    deployed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ForensicReport(BaseModel):
    report_id: str = Field(..., description="Unique forensics report ID")
    threat_id: str = Field(..., description="Correlated threat identifier")
    target_asset: str = Field(..., description="Targeted internal service or API gateway")
    cvss_score: float = Field(..., description="CVSS v3.1 base severity score (0.0 to 10.0)")
    extracted_iocs: List[str] = Field(default_factory=list, description="Indicators of Compromise")
    attack_timeline: List[str] = Field(default_factory=list)
    risk_assessment: str = Field(..., description="Executive risk assessment summary")


class SOCTicket(BaseModel):
    ticket_id: str = Field(..., description="Automated SOC incident ticket identifier (e.g., SOC-INC-7819)")
    severity: ThreatSeverity = Field(..., description="Incident priority tier")
    assigned_tier: str = Field(default="TIER_2", description="Assigned SOC response tier")
    title: str = Field(..., description="Incident summary title")
    description: str = Field(..., description="Detailed briefing for on-call responder")
    containment_status: str = Field(..., description="CONTAINED, MITIGATING, or ACTIVE_THREAT")
    iocs: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
