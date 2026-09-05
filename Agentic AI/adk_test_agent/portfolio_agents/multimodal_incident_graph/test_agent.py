"""Comprehensive unit and integration tests for Multimodal Incident Graph."""

import pytest
from portfolio_agents.multimodal_incident_graph.agent import root_agent
from portfolio_agents.multimodal_incident_graph.tools import (
    query_incident_topology,
    trace_graph_root_cause,
    execute_incident_runbook,
    ingest_multimodal_syslog_telemetry,
    GRAPH_NODES,
)


def test_root_agent_configuration():
    assert root_agent.name == "multimodal_incident_graph"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.tools) == 4
    tool_names = [getattr(t, "__name__", str(t)) for t in root_agent.tools]
    assert "query_incident_topology" in tool_names
    assert "trace_graph_root_cause" in tool_names
    assert "execute_incident_runbook" in tool_names
    assert "ingest_multimodal_syslog_telemetry" in tool_names
    assert "Incident" in root_agent.description or "incident" in root_agent.description


def test_query_incident_topology_all():
    nodes = query_incident_topology()
    assert len(nodes) >= 6
    assert any(n["id"] == "INC-2026-P1-BGP" for n in nodes)
    assert any(n["id"] == "INFRA-ROUTER-BGP-01" for n in nodes)


def test_query_incident_topology_filters():
    infra_nodes = query_incident_topology(node_type="Infrastructure")
    assert len(infra_nodes) >= 2
    for n in infra_nodes:
        assert n["type"] == "Infrastructure"

    incident_nodes = query_incident_topology(incident_id="INC-2026-P1-BGP")
    assert len(incident_nodes) >= 1


def test_trace_graph_root_cause_p1_bgp():
    trace = trace_graph_root_cause(incident_id="INC-2026-P1-BGP")
    assert "error" not in trace
    assert trace["incident_id"] == "INC-2026-P1-BGP"
    assert trace["lifecycle_state"] == "ROOT_CAUSE_ISOLATED"
    assert trace["root_cause"]["id"] == "RC-BGP-ROUTE-LEAK"
    assert trace["recommended_runbook"]["id"] == "RB-BGP-RESET-01"
    assert len(trace["evidence"]) >= 1
    assert len(trace["causal_graph_path"]) >= 3


def test_trace_graph_root_cause_invalid():
    res = trace_graph_root_cause(incident_id="INC-NONEXISTENT-999")
    assert "error" in res


def test_execute_incident_runbook():
    result = execute_incident_runbook(
        runbook_id="RB-BGP-RESET-01",
        target_node="INFRA-ROUTER-BGP-01",
    )
    assert result["status"] == "SUCCESS"
    assert result["verification_passed"] is True
    assert result["runbook_id"] == "RB-BGP-RESET-01"
    assert len(result["execution_steps"]) == 4
    assert result["metrics_restored"]["packet_drop_pct"] == 0.0

    # Verify incident state transitioned to resolved
    incident = GRAPH_NODES["INC-2026-P1-BGP"]
    assert incident["attributes"]["lifecycle"] == "VERIFIED_RESOLVED"


def test_ingest_multimodal_syslog_telemetry():
    raw_log = "%ROUTING-BGP-3-MAXPFX: Prefix limit exceeded on peer 198.51.100.1, state down"
    report = ingest_multimodal_syslog_telemetry(
        source_system="INFRA-ROUTER-BGP-01",
        raw_log_excerpt=raw_log,
    )
    assert report["anomaly_detected"] is True
    assert report["status"] == "NODE_LINKED"
    assert report["evidence_id"] is not None

    # Normal log test
    normal_report = ingest_multimodal_syslog_telemetry(
        source_system="INFRA-ROUTER-BGP-01",
        raw_log_excerpt="Heartbeat status healthy and active",
    )
    assert normal_report["anomaly_detected"] is False
    assert normal_report["status"] == "NORMAL_TELEMETRY_LOGGED"
