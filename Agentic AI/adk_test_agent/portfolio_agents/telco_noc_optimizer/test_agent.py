"""Comprehensive unit and integration tests for Telco NOC Optimizer."""

import pytest
from portfolio_agents.telco_noc_optimizer.agent import root_agent
from portfolio_agents.telco_noc_optimizer.tools import (
    get_cell_tower_telemetry,
    execute_mitigation_action,
    consult_3gpp_specifications,
    estimate_sla_financial_impact,
    TOWER_REGISTRY,
)


def test_root_agent_configuration():
    assert root_agent.name == "telco_noc_optimizer"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.tools) == 4
    tool_names = [getattr(t, "__name__", str(t)) for t in root_agent.tools]
    assert "get_cell_tower_telemetry" in tool_names
    assert "execute_mitigation_action" in tool_names
    assert "consult_3gpp_specifications" in tool_names
    assert "estimate_sla_financial_impact" in tool_names
    assert "5G" in root_agent.description


def test_get_cell_tower_telemetry_all():
    telemetry = get_cell_tower_telemetry()
    assert len(telemetry) >= 5
    for record in telemetry:
        assert "tower_id" in record
        assert "prb_utilization_pct" in record
        assert "status" in record


def test_get_cell_tower_telemetry_filters():
    ne_towers = get_cell_tower_telemetry(region="North-East")
    assert len(ne_towers) >= 2
    for t in ne_towers:
        assert t["region"] == "North-East"

    optimal_towers = get_cell_tower_telemetry(status_filter="OPTIMAL")
    assert len(optimal_towers) >= 1
    for t in optimal_towers:
        assert t["status"] == "OPTIMAL"


def test_execute_mitigation_action():
    # Target tower with high PRB
    tower_id = "TWR-5G-NY-01"
    initial_prb = TOWER_REGISTRY[tower_id]["prb_utilization_pct"]

    result = execute_mitigation_action(
        tower_id=tower_id,
        action="load_balance_xn",
        target_param=25.0,
    )

    assert result["status"] == "SUCCESS"
    assert "NOC-INC-2026-" in result["ticket_id"]
    assert result["tower_id"] == tower_id
    assert result["action_executed"] == "load_balance_xn"
    assert result["prb_reduction_pct"] > 0
    assert result["projected_latency_ms"] < 30.0
    assert "TS 38.401" in result["standard_applied"]

    # Verify state mutation in registry
    assert TOWER_REGISTRY[tower_id]["prb_utilization_pct"] < initial_prb


def test_execute_mitigation_invalid_tower():
    res = execute_mitigation_action(tower_id="NON-EXISTENT", action="load_balance_xn")
    assert res["status"] == "FAILED"
    assert "error" in res


def test_consult_3gpp_specifications():
    spec_xn = consult_3gpp_specifications(query="Xn load balancing", spec_number="TS 38.401")
    assert spec_xn["spec_number"] == "TS 38.401"
    assert "NG-RAN" in spec_xn["title"]

    spec_urllc = consult_3gpp_specifications(query="URLLC QoS latency")
    assert "TS 23.501" in spec_urllc["spec_number"] or "TS 38.401" in spec_urllc["spec_number"]


def test_estimate_sla_financial_impact():
    impact = estimate_sla_financial_impact(tower_id="TWR-5G-CHI-05", outage_duration_minutes=20)
    assert "estimated_penalty_usd" in impact
    assert impact["estimated_penalty_usd"] > 0
    assert impact["active_subscribers_impacted"] == 1450
    assert impact["compliance_risk"] in ["HIGH", "SEVERE", "MEDIUM"]
    assert "remediation" in impact.get("recommendation", "").lower() or "load_balance" in impact.get("recommendation", "")
