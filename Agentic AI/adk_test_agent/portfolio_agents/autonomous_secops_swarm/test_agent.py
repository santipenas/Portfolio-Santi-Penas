"""Comprehensive unit and integration tests for Autonomous SecOps Swarm."""

import pytest
from portfolio_agents.autonomous_secops_swarm.agent import (
    root_agent,
    threat_hunter_agent,
    firewall_mitigator_agent,
    soc_dispatcher_agent,
)
from portfolio_agents.autonomous_secops_swarm.tools import (
    scan_threat_intelligence_feed,
    deploy_firewall_countermeasure,
    extract_forensic_iocs,
    dispatch_soc_incident_ticket,
    ACTIVE_FIREWALL_RULES,
)


def test_swarm_agent_hierarchy():
    assert root_agent.name == "autonomous_secops_swarm"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.sub_agents) == 3

    sub_names = [a.name for a in root_agent.sub_agents]
    assert "threat_hunter" in sub_names
    assert "firewall_mitigator" in sub_names
    assert "soc_dispatcher" in sub_names

    # Check specialized subagent tools
    assert len(threat_hunter_agent.tools) == 2
    assert len(firewall_mitigator_agent.tools) == 1
    assert len(soc_dispatcher_agent.tools) == 1


def test_scan_threat_intelligence_feed():
    all_high_critical = scan_threat_intelligence_feed(severity_min="HIGH")
    assert len(all_high_critical) >= 3
    for threat in all_high_critical:
        assert threat["severity"] in ["HIGH", "CRITICAL"]
        assert "ip_address" in threat
        assert "attack_type" in threat

    # Filter by specific IP
    specific = scan_threat_intelligence_feed(ip_or_domain="198.51.100.44")
    assert len(specific) == 1
    assert specific[0]["threat_id"] == "THR-2026-081"
    assert specific[0]["attack_type"] == "DDOS_AMPLIFICATION"


def test_deploy_firewall_countermeasure():
    result = deploy_firewall_countermeasure(
        target_ip="198.51.100.44",
        rule_type="BGP_FLOWSPEC",
        action="BLACKHOLE",
        duration_minutes=120,
    )
    assert result["status"] == "DEPLOYED"
    rule = result["rule"]
    assert "FW-RULE-" in rule["rule_id"]
    assert rule["target_ip"] == "198.51.100.44"
    assert rule["action"] == "BLACKHOLE"
    assert rule["duration_minutes"] == 120
    assert "RTR-EDGE-SCRUB-01" in rule["router_applied"]

    # Verify rule persisted in active rules
    assert rule["rule_id"] in ACTIVE_FIREWALL_RULES


def test_extract_forensic_iocs():
    forensics = extract_forensic_iocs("THR-2026-081")
    assert "error" not in forensics
    assert forensics["threat_id"] == "THR-2026-081"
    assert forensics["cvss_score"] >= 9.0
    assert len(forensics["extracted_iocs"]) >= 2
    assert any("198.51.100.44" in ioc for ioc in forensics["extracted_iocs"])
    assert len(forensics["attack_timeline"]) >= 3

    invalid = extract_forensic_iocs("THR-NONEXISTENT")
    assert "error" in invalid


def test_dispatch_soc_incident_ticket():
    dispatch = dispatch_soc_incident_ticket(
        incident_id="THR-2026-081",
        severity="CRITICAL",
        summary="Volumetric DDoS amplification attack quarantined at perimeter edge.",
        iocs=["IPv4:198.51.100.44", "ASN:AS64512"],
        assigned_tier="TIER_2",
    )
    assert dispatch["status"] == "DISPATCHED"
    ticket = dispatch["ticket"]
    assert "SOC-INC-" in ticket["ticket_id"]
    assert ticket["severity"] == "CRITICAL"
    assert ticket["assigned_tier"] == "TIER_2"
    assert ticket["containment_status"] == "CONTAINED"
    assert len(ticket["iocs"]) == 2
    assert "Tier-2" in dispatch["pagerduty_escalation"]
