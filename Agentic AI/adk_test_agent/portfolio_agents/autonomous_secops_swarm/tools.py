"""Defensive cybersecurity and perimeter mitigation tools for Autonomous SecOps Swarm."""

import random
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from google.adk.tools import ToolContext
from .models import (
    ThreatFeedEntry,
    ThreatSeverity,
    AttackType,
    FirewallRule,
    ForensicReport,
    SOCTicket,
)

# Active Threat Intelligence Feed & SIEM Anomaly Repository
THREAT_FEED_DATABASE: Dict[str, Dict[str, Any]] = {
    "THR-2026-081": {
        "threat_id": "THR-2026-081",
        "ip_address": "198.51.100.44",
        "attack_type": AttackType.DDOS_AMPLIFICATION.value,
        "severity": ThreatSeverity.CRITICAL.value,
        "confidence_score": 0.98,
        "source_country": "RU",
        "payload_sample": "DNS ANY query amplification targeting 5G Roaming API Gateway (84 Gbps flood).",
    },
    "THR-2026-082": {
        "threat_id": "THR-2026-082",
        "ip_address": "203.0.113.19",
        "attack_type": AttackType.SQL_INJECTION.value,
        "severity": ThreatSeverity.HIGH.value,
        "confidence_score": 0.92,
        "source_country": "CN",
        "payload_sample": "UNION SELECT 1,username,password_hash FROM subscriber_auth_tokens--",
    },
    "THR-2026-083": {
        "threat_id": "THR-2026-083",
        "ip_address": "192.0.2.78",
        "attack_type": AttackType.CREDENTIAL_STUFFING.value,
        "severity": ThreatSeverity.HIGH.value,
        "confidence_score": 0.89,
        "source_country": "BR",
        "payload_sample": "Automated brute-force spraying against Self-Care 5G Portal (/api/v2/auth/token).",
    },
    "THR-2026-084": {
        "threat_id": "THR-2026-084",
        "ip_address": "198.51.100.99",
        "attack_type": AttackType.API_TELECOM_ABUSE.value,
        "severity": ThreatSeverity.MEDIUM.value,
        "confidence_score": 0.74,
        "source_country": "NL",
        "payload_sample": "Abnormal NEF (Network Exposure Function) location query frequency spike (450 req/sec).",
    },
}

ACTIVE_FIREWALL_RULES: Dict[str, Dict[str, Any]] = {}
SOC_DISPATCH_QUEUE: List[Dict[str, Any]] = []


def scan_threat_intelligence_feed(
    ip_or_domain: Optional[str] = None,
    severity_min: str = "HIGH",
) -> List[Dict[str, Any]]:
    """Scans external threat intelligence feeds and SIEM alerts for malicious activity targeting telecom and cloud APIs.

    Args:
        ip_or_domain: Optional specific IP address or domain to query (e.g., '198.51.100.44').
        severity_min: Minimum severity filter ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW').

    Returns:
        List of matching ThreatFeedEntry records with attack signatures and confidence scores.
    """
    severity_levels = {
        ThreatSeverity.CRITICAL.value: 4,
        ThreatSeverity.HIGH.value: 3,
        ThreatSeverity.MEDIUM.value: 2,
        ThreatSeverity.LOW.value: 1,
    }
    min_level = severity_levels.get(severity_min.upper(), 3)

    results = []
    for entry in THREAT_FEED_DATABASE.values():
        if ip_or_domain and entry["ip_address"] != ip_or_domain and ip_or_domain not in entry["payload_sample"]:
            continue
        entry_level = severity_levels.get(entry["severity"], 1)
        if entry_level >= min_level:
            results.append(ThreatFeedEntry(**entry).model_dump())

    return results


def deploy_firewall_countermeasure(
    target_ip: str,
    rule_type: str = "EDGE_DROP",
    action: str = "DROP",
    duration_minutes: int = 60,
    ctx: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Instantly provisions and deploys edge firewall ACLs, rate limiting, or BGP Flowspec blackholing on perimeter routers.

    Args:
        target_ip: Malicious IP address to quarantine (e.g., '198.51.100.44').
        rule_type: Policy mechanism ('EDGE_DROP', 'BGP_FLOWSPEC', 'RATE_LIMIT').
        action: Action to execute ('DROP', 'REJECT', 'BLACKHOLE', 'RATE_LIMIT').
        duration_minutes: Lease TTL in minutes before automatic rule expiry.
        ctx: Runtime ToolContext injected by Google ADK to track firewall audit trail.

    Returns:
        Structured FirewallRule confirmation with unique rule ID and perimeter router attribution.
    """
    rule_id = f"FW-RULE-{random.randint(1000, 9999)}"
    router = "RTR-EDGE-SCRUB-01" if "FLOWSPEC" in rule_type.upper() else "RTR-PERIMETER-NY-01"

    rule = FirewallRule(
        rule_id=rule_id,
        target_ip=target_ip,
        rule_type=rule_type,
        action=action,
        duration_minutes=duration_minutes,
        router_applied=router,
    )

    ACTIVE_FIREWALL_RULES[rule_id] = rule.model_dump()

    # Track in ADK tool context state if provided
    if ctx and hasattr(ctx, "state") and ctx.state is not None:
        firewall_log = ctx.state.get("deployed_firewall_rules", [])
        firewall_log.append(rule.model_dump())
        ctx.state["deployed_firewall_rules"] = firewall_log

    return {
        "status": "DEPLOYED",
        "rule": rule.model_dump(),
        "perimeter_status": f"Traffic from {target_ip} actively {action} on {router}.",
    }


def extract_forensic_iocs(threat_id: str) -> Dict[str, Any]:
    """Performs deep payload forensics to isolate Indicators of Compromise (IOCs), compute CVSS risk, and compile forensic timelines.

    Args:
        threat_id: Identifier of the detected threat (e.g., 'THR-2026-081').

    Returns:
        Structured ForensicReport with CVSS v3.1 score, IOC list, and timeline.
    """
    if threat_id not in THREAT_FEED_DATABASE:
        return {"error": f"Threat ID '{threat_id}' not found in SIEM feed."}

    entry = THREAT_FEED_DATABASE[threat_id]
    ip = entry["ip_address"]
    attack_type = entry["attack_type"]

    cvss = 9.8 if entry["severity"] == ThreatSeverity.CRITICAL.value else 8.2
    iocs = [
        f"IPv4:{ip}",
        f"ASN:AS{random.randint(10000, 60000)}",
        f"Signature:{attack_type}#v2026",
    ]

    timeline = [
        f"T-00m: Initial anomaly detected by Edge NetFlow collector for {ip}",
        f"T-02m: Behavioral signature matched known {attack_type} pattern",
        "T-03m: Automated threat hunter quarantined telemetry excerpt",
    ]

    report = ForensicReport(
        report_id=f"FORENSIC-REP-{datetime.now(timezone.utc).strftime('%H%M%S')}",
        threat_id=threat_id,
        target_asset="5G Telecom Gateway & NEF API",
        cvss_score=cvss,
        extracted_iocs=iocs,
        attack_timeline=timeline,
        risk_assessment=(
            f"High-impact {attack_type} originating from {entry['source_country']}. "
            "Requires immediate perimeter ACL enforcement and Tier-2 On-Call triage."
        ),
    )
    return report.model_dump()


def dispatch_soc_incident_ticket(
    incident_id: str,
    severity: str,
    summary: str,
    iocs: List[str],
    assigned_tier: str = "TIER_2",
) -> Dict[str, Any]:
    """Generates and dispatches a high-priority incident ticket to the 24/7 Security Operations Center (SOC) On-Call engineering team.

    Args:
        incident_id: Associated threat or incident ID.
        severity: Priority level ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW').
        summary: Brief incident description and containment summary.
        iocs: List of verified Indicators of Compromise.
        assigned_tier: Assigned incident response team ('TIER_1', 'TIER_2', 'TIER_3_FORENSICS').

    Returns:
        Structured SOCTicket confirmation with tracking ID and timestamp.
    """
    ticket_id = f"SOC-INC-{random.randint(1000, 9999)}"
    sev_enum = ThreatSeverity(severity.upper()) if severity.upper() in ThreatSeverity.__members__ else ThreatSeverity.HIGH

    ticket = SOCTicket(
        ticket_id=ticket_id,
        severity=sev_enum,
        assigned_tier=assigned_tier,
        title=f"[{sev_enum.value}] Automated Incident Containment for {incident_id}",
        description=summary,
        containment_status="CONTAINED",
        iocs=iocs,
    )

    SOC_DISPATCH_QUEUE.append(ticket.model_dump())

    return {
        "status": "DISPATCHED",
        "ticket": ticket.model_dump(),
        "pagerduty_escalation": "Triggered for Tier-2 On-Call SecOps Engineer",
    }
