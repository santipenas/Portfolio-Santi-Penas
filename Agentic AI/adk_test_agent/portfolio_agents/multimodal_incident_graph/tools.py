"""Graph-based incident topology and automated runbook tools for ADK."""

from collections import deque
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from google.adk.tools import ToolContext
from .models import (
    NodeType,
    RelationType,
    GraphNode,
    GraphEdge,
    IncidentSeverity,
    IncidentLifecycle,
    RunbookExecutionResult,
)

# In-Memory Incident Graph Topology Knowledge Base
GRAPH_NODES: Dict[str, Dict[str, Any]] = {
    "INC-2026-P1-BGP": {
        "id": "INC-2026-P1-BGP",
        "type": NodeType.INCIDENT.value,
        "label": "Total 5G User-Plane Blackhole in US-East Data Center",
        "attributes": {
            "severity": IncidentSeverity.P1.value,
            "lifecycle": IncidentLifecycle.INVESTIGATING.value,
            "packet_drop_pct": 98.4,
            "impacted_subscribers": 142000,
        },
    },
    "SVC-5G-UPF-EAST": {
        "id": "SVC-5G-UPF-EAST",
        "type": NodeType.SERVICE.value,
        "label": "5G Core User Plane Function (UPF) Cluster East",
        "attributes": {"cluster_status": "DEGRADED", "active_tunnels": 2200},
    },
    "INFRA-ROUTER-BGP-01": {
        "id": "INFRA-ROUTER-BGP-01",
        "type": NodeType.INFRASTRUCTURE.value,
        "label": "Edge Peering Router AS65001-NYC-01",
        "attributes": {"firmware": "XR-7.9.2", "bgp_peer": "198.51.100.1", "state": "UNREACHABLE"},
    },
    "RC-BGP-ROUTE-LEAK": {
        "id": "RC-BGP-ROUTE-LEAK",
        "type": NodeType.ROOT_CAUSE.value,
        "label": "BGP Autonomous System Path Hijack / Invalid Route Leak",
        "attributes": {
            "confidence_score": 0.96,
            "origin_asn": 64512,
            "prefix_hijacked": "198.51.100.0/24",
        },
    },
    "RB-BGP-RESET-01": {
        "id": "RB-BGP-RESET-01",
        "type": NodeType.RUNBOOK.value,
        "label": "Automated BGP Peering Prefix Filter Flush & Neighbor Soft-Reset",
        "attributes": {
            "target_system": "INFRA-ROUTER-BGP-01",
            "estimated_recovery_time_s": 12,
            "safe_for_automated_execution": True,
        },
    },
    "EVID-SYSLOG-0941": {
        "id": "EVID-SYSLOG-0941",
        "type": NodeType.EVIDENCE.value,
        "label": "Syslog: %ROUTING-BGP-3-MAXPFX: Prefix limit exceeded on peer 198.51.100.1",
        "attributes": {"severity": "CRITICAL", "source": "INFRA-ROUTER-BGP-01"},
    },
    "INC-2026-P2-OPTICAL": {
        "id": "INC-2026-P2-OPTICAL",
        "type": NodeType.INCIDENT.value,
        "label": "DWDM Optical Transceiver Power Degradation",
        "attributes": {
            "severity": IncidentSeverity.P2.value,
            "lifecycle": IncidentLifecycle.DETECTED.value,
            "optical_rx_dbm": -28.4,
        },
    },
    "INFRA-DWDM-CHASSIS-04": {
        "id": "INFRA-DWDM-CHASSIS-04",
        "type": NodeType.INFRASTRUCTURE.value,
        "label": "Core DWDM Optical Transport Switch Metro-Ring",
        "attributes": {"line_rate": "400Gbps", "ber_rate": 1.4e-3},
    },
    "RC-OPTICAL-FIBER-FLAP": {
        "id": "RC-OPTICAL-FIBER-FLAP",
        "type": NodeType.ROOT_CAUSE.value,
        "label": "Physical Fiber Micro-Bend & High Attenuation Loss",
        "attributes": {"confidence_score": 0.91, "attenuation_db": 14.2},
    },
    "RB-OPTICAL-SWITCHOVER": {
        "id": "RB-OPTICAL-SWITCHOVER",
        "type": NodeType.RUNBOOK.value,
        "label": "Hitless Optical Protection Switchover (1+1 APS)",
        "attributes": {"safe_for_automated_execution": True},
    },
}

GRAPH_EDGES: List[Dict[str, Any]] = [
    {"source": "INC-2026-P1-BGP", "target": "SVC-5G-UPF-EAST", "relation": RelationType.IMPACTS.value, "weight": 1.0},
    {"source": "SVC-5G-UPF-EAST", "target": "INFRA-ROUTER-BGP-01", "relation": RelationType.HOSTED_ON.value, "weight": 0.95},
    {"source": "INFRA-ROUTER-BGP-01", "target": "RC-BGP-ROUTE-LEAK", "relation": RelationType.CAUSED_BY.value, "weight": 0.96},
    {"source": "RC-BGP-ROUTE-LEAK", "target": "EVID-SYSLOG-0941", "relation": RelationType.DETECTED_BY.value, "weight": 0.98},
    {"source": "RC-BGP-ROUTE-LEAK", "target": "RB-BGP-RESET-01", "relation": RelationType.RESOLVED_BY.value, "weight": 1.0},
    {"source": "INC-2026-P2-OPTICAL", "target": "INFRA-DWDM-CHASSIS-04", "relation": RelationType.IMPACTS.value, "weight": 0.9},
    {"source": "INFRA-DWDM-CHASSIS-04", "target": "RC-OPTICAL-FIBER-FLAP", "relation": RelationType.CAUSED_BY.value, "weight": 0.92},
    {"source": "RC-OPTICAL-FIBER-FLAP", "target": "RB-OPTICAL-SWITCHOVER", "relation": RelationType.RESOLVED_BY.value, "weight": 1.0},
]


def query_incident_topology(
    incident_id: Optional[str] = None,
    node_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Queries the multimodal incident topology graph for active nodes, relationships, and operational context.

    Args:
        incident_id: Optional incident ID to filter graph nodes related to a specific outage (e.g., 'INC-2026-P1-BGP').
        node_type: Optional filter by node type ('Incident', 'Service', 'Infrastructure', 'RootCause', 'Runbook', 'Evidence').

    Returns:
        List of matching graph node records with their properties and edge connections.
    """
    results = []
    for node_id, node in GRAPH_NODES.items():
        if node_type and node["type"].lower() != node_type.lower():
            continue
        if incident_id and incident_id not in node_id and incident_id not in str(node.get("attributes", {})):
            # Check edge connectivity if specific incident requested
            connected = any(
                (e["source"] == incident_id and e["target"] == node_id)
                or (e["target"] == incident_id and e["source"] == node_id)
                for e in GRAPH_EDGES
            )
            if not connected and node["id"] != incident_id:
                continue

        # Attach outgoing and incoming edge metadata
        outgoing = [e for e in GRAPH_EDGES if e["source"] == node_id]
        incoming = [e for e in GRAPH_EDGES if e["target"] == node_id]
        results.append({
            **node,
            "outgoing_edges": outgoing,
            "incoming_edges": incoming,
        })
    return results


def trace_graph_root_cause(incident_id: str) -> Dict[str, Any]:
    """Navigates graph edges using breadth-first traversal to discover the underlying root cause and associated runbook.

    Args:
        incident_id: Incident identifier to diagnose (e.g., 'INC-2026-P1-BGP').

    Returns:
        Diagnostic trace containing the root cause node, causal path, evidence log references, and remediation runbook.
    """
    if incident_id not in GRAPH_NODES:
        return {"error": f"Incident '{incident_id}' not found in topology graph."}

    # BFS traversal starting from the incident node
    queue = deque([[incident_id]])
    visited = {incident_id}
    root_cause_node = None
    remediation_runbook = None
    evidence_nodes = []
    causal_path = []

    while queue:
        path = queue.popleft()
        current_node_id = path[-1]
        current_node = GRAPH_NODES.get(current_node_id, {})

        if current_node.get("type") == NodeType.ROOT_CAUSE.value:
            root_cause_node = current_node
            causal_path = path

            # Find runbooks and evidence connected to this root cause
            for edge in GRAPH_EDGES:
                if edge["source"] == current_node_id:
                    target = GRAPH_NODES.get(edge["target"], {})
                    if edge["relation"] == RelationType.RESOLVED_BY.value or target.get("type") == NodeType.RUNBOOK.value:
                        remediation_runbook = target
                    elif edge["relation"] == RelationType.DETECTED_BY.value or target.get("type") == NodeType.EVIDENCE.value:
                        evidence_nodes.append(target)
            break

        # Explore outgoing edges
        for edge in GRAPH_EDGES:
            if edge["source"] == current_node_id and edge["target"] not in visited:
                visited.add(edge["target"])
                queue.append(path + [edge["target"]])

    if not root_cause_node:
        return {
            "incident_id": incident_id,
            "status": "ROOT_CAUSE_NOT_FOUND",
            "message": "Graph traversal did not locate a terminal RootCause node.",
        }

    # Update incident state in graph
    GRAPH_NODES[incident_id]["attributes"]["lifecycle"] = IncidentLifecycle.ROOT_CAUSE_ISOLATED.value

    return {
        "incident_id": incident_id,
        "incident_label": GRAPH_NODES[incident_id]["label"],
        "lifecycle_state": IncidentLifecycle.ROOT_CAUSE_ISOLATED.value,
        "root_cause": root_cause_node,
        "causal_graph_path": [
            {"node_id": nid, "label": GRAPH_NODES.get(nid, {}).get("label", nid)}
            for nid in causal_path
        ],
        "evidence": evidence_nodes,
        "recommended_runbook": remediation_runbook,
    }


def execute_incident_runbook(
    runbook_id: str,
    target_node: str,
    parameters: Optional[Dict[str, Any]] = None,
    ctx: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Executes an automated infrastructure remediation runbook linked to an incident root cause.

    Args:
        runbook_id: Identifier of the runbook to execute (e.g., 'RB-BGP-RESET-01', 'RB-OPTICAL-SWITCHOVER').
        target_node: Target infrastructure node ID (e.g., 'INFRA-ROUTER-BGP-01').
        parameters: Optional execution overrides or authentication tokens.
        ctx: Runtime ToolContext injected by Google ADK to persist runbook execution telemetry.

    Returns:
        Structured RunbookExecutionResult detailing verification checks, restored metrics, and state update.
    """
    if runbook_id not in GRAPH_NODES:
        return {"status": "FAILED", "error": f"Runbook '{runbook_id}' not found in operational catalog."}

    runbook = GRAPH_NODES[runbook_id]

    # Map runbook to incident
    incident_id = "INC-2026-P1-BGP" if "BGP" in runbook_id else "INC-2026-P2-OPTICAL"

    steps = [
        f"1. Pre-check: Verified telemetry on target node {target_node}",
        f"2. Execution: Dispatched automated operational payload for {runbook_id}",
        "3. Convergence: Awaited BGP/transport topology convergence (1.2s)",
        "4. Post-check: Confirmed 0% packet loss and normal latency thresholds",
    ]

    # Update graph node states
    if incident_id in GRAPH_NODES:
        GRAPH_NODES[incident_id]["attributes"]["lifecycle"] = IncidentLifecycle.VERIFIED_RESOLVED.value
        GRAPH_NODES[incident_id]["attributes"]["packet_drop_pct"] = 0.0

    if target_node in GRAPH_NODES:
        GRAPH_NODES[target_node]["attributes"]["state"] = "ONLINE_OPERATIONAL"

    result = RunbookExecutionResult(
        runbook_id=runbook_id,
        target_node=target_node,
        status="SUCCESS",
        verification_passed=True,
        remediated_incident_id=incident_id,
        execution_steps=steps,
        metrics_restored={
            "packet_drop_pct": 0.0,
            "upstream_reachability": "100%",
            "service_sla": "RESTORED",
        },
    )

    if ctx and hasattr(ctx, "state") and ctx.state is not None:
        executed_runbooks = ctx.state.get("executed_runbooks", [])
        executed_runbooks.append(result.model_dump())
        ctx.state["executed_runbooks"] = executed_runbooks

    return result.model_dump()


def ingest_multimodal_syslog_telemetry(
    source_system: str,
    raw_log_excerpt: str,
    anomaly_score_threshold: float = 0.75,
) -> Dict[str, Any]:
    """Ingests and parses unstructured syslog entries and optical telemetry, linking them as new evidence in the incident graph.

    Args:
        source_system: Originating network element (e.g., 'INFRA-ROUTER-BGP-01', 'INFRA-DWDM-CHASSIS-04').
        raw_log_excerpt: Raw multiline syslog string or hardware trap message.
        anomaly_score_threshold: Sensitivity threshold for flagging anomalous telemetry.

    Returns:
        Structured evidence ingestion report including generated evidence node ID and correlation edge.
    """
    evidence_id = f"EVID-{datetime.now(timezone.utc).strftime('%H%M%S')}"
    anomaly_detected = (
        "exceeded" in raw_log_excerpt.lower()
        or "flap" in raw_log_excerpt.lower()
        or "fail" in raw_log_excerpt.lower()
        or "error" in raw_log_excerpt.lower()
    )

    confidence = 0.94 if anomaly_detected else 0.40

    if anomaly_detected and confidence >= anomaly_score_threshold:
        # Create and link new evidence node dynamically in graph
        GRAPH_NODES[evidence_id] = {
            "id": evidence_id,
            "type": NodeType.EVIDENCE.value,
            "label": f"Dynamically Parsed Telemetry: {raw_log_excerpt[:60]}...",
            "attributes": {
                "source": source_system,
                "confidence": confidence,
                "raw_log": raw_log_excerpt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }
        GRAPH_EDGES.append({
            "source": source_system,
            "target": evidence_id,
            "relation": RelationType.DETECTED_BY.value,
            "weight": confidence,
        })

    return {
        "evidence_id": evidence_id if anomaly_detected else None,
        "source_system": source_system,
        "anomaly_detected": anomaly_detected,
        "confidence_score": confidence,
        "status": "NODE_LINKED" if anomaly_detected else "NORMAL_TELEMETRY_LOGGED",
    }
