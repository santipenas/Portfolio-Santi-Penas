"""Domain tools for Telco NOC Optimizer."""

import random
from typing import Optional, List, Dict, Any
from google.adk.tools import ToolContext
from .models import (
    CellTowerMetrics,
    TowerStatus,
    MitigationType,
    MitigationResult,
    SLAImpactEstimate,
)

# Simulated Telco Infrastructure Database
TOWER_REGISTRY: Dict[str, Dict[str, Any]] = {
    "TWR-5G-NY-01": {
        "tower_id": "TWR-5G-NY-01",
        "region": "North-East",
        "carrier_band": "n78 (3.5 GHz)",
        "connected_users": 1840,
        "prb_utilization_pct": 94.2,
        "latency_ms": 48.5,
        "packet_loss_pct": 3.8,
        "status": TowerStatus.CRITICAL_OVERLOAD.value,
    },
    "TWR-5G-NY-02": {
        "tower_id": "TWR-5G-NY-02",
        "region": "North-East",
        "carrier_band": "n258 (24 GHz mmWave)",
        "connected_users": 420,
        "prb_utilization_pct": 38.0,
        "latency_ms": 6.2,
        "packet_loss_pct": 0.05,
        "status": TowerStatus.OPTIMAL.value,
    },
    "TWR-5G-CHI-05": {
        "tower_id": "TWR-5G-CHI-05",
        "region": "Midwest",
        "carrier_band": "n77 (3.7 GHz)",
        "connected_users": 1450,
        "prb_utilization_pct": 86.5,
        "latency_ms": 29.1,
        "packet_loss_pct": 1.4,
        "status": TowerStatus.CONGESTED.value,
    },
    "TWR-5G-SFO-09": {
        "tower_id": "TWR-5G-SFO-09",
        "region": "West",
        "carrier_band": "n78 (3.5 GHz)",
        "connected_users": 790,
        "prb_utilization_pct": 62.0,
        "latency_ms": 11.4,
        "packet_loss_pct": 0.2,
        "status": TowerStatus.OPTIMAL.value,
    },
    "TWR-5G-MIA-03": {
        "tower_id": "TWR-5G-MIA-03",
        "region": "South-East",
        "carrier_band": "n71 (600 MHz Low-Band)",
        "connected_users": 1210,
        "prb_utilization_pct": 79.4,
        "latency_ms": 22.0,
        "packet_loss_pct": 0.9,
        "status": TowerStatus.WARNING.value,
    },
}

# Standardized 3GPP Technical Specifications Reference Base
STANDARDS_DB: Dict[str, Dict[str, str]] = {
    "TS 38.401": {
        "title": "NG-RAN Architecture Description",
        "scope": "Defines the overall architecture of NG-RAN, focusing on gNB-CU and gNB-DU separation and the Xn interface for intra-RAT inter-gNB load coordination.",
        "remediation_guideline": "For high PRB congestion exceeding 85%, trigger inter-gNB handover via Xn-AP interface to adjacent underutilized cells (TS 38.401 Section 8.2).",
    },
    "TS 23.501": {
        "title": "System Architecture for the 5G System (5GS)",
        "scope": "Defines QoS Flows, 5QI mappings, URLLC requirements, and slicing policies (NSSAI).",
        "remediation_guideline": "URLLC services require end-to-end latency < 10ms and packet loss < 10^-5. When latency exceeds 30ms, prioritize QoS Flow preemption or frequency steering.",
    },
    "TS 38.331": {
        "title": "Radio Resource Control (RRC) Protocol Specification",
        "scope": "Covers RRC connection establishment, reconfiguration, carrier aggregation (CA) SCell addition/activation, and secondary cell group modification.",
        "remediation_guideline": "Trigger RRC Connection Reconfiguration to activate secondary cells on complementary carrier bands or dynamic power boosting for high-capacity massive MIMO arrays.",
    },
}


def get_cell_tower_telemetry(
    region: Optional[str] = None,
    status_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Ingests real-time telemetry metrics from 5G/LTE cell towers across network regions.

    Args:
        region: Optional filter by geographical region (e.g., 'North-East', 'West', 'Midwest').
        status_filter: Optional filter by status ('OPTIMAL', 'WARNING', 'CONGESTED', 'CRITICAL_OVERLOAD').

    Returns:
        List of cell tower metric records matching criteria.
    """
    results = []
    for tower in TOWER_REGISTRY.values():
        if region and tower["region"].lower() != region.lower():
            continue
        if status_filter and tower["status"].lower() != status_filter.lower():
            continue
        results.append(CellTowerMetrics(**tower).model_dump())
    return results


def execute_mitigation_action(
    tower_id: str,
    action: str,
    target_param: Optional[float] = None,
    ctx: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Executes an automated network optimization or congestion mitigation procedure on a target cell tower.

    Args:
        tower_id: Identifier of the cell tower experiencing degraded performance (e.g., 'TWR-5G-NY-01').
        action: Remediation action to execute ('load_balance_xn', 'power_boost_mimo', 'carrier_aggregation_steer', 'reroute_traffic').
        target_param: Optional parameter value (e.g., percentage of traffic to steer or dBm boost).
        ctx: Runtime ToolContext injected by Google ADK to track session history.

    Returns:
        Structured MitigationResult containing action status, audit ticket ID, and projected post-mitigation metrics.
    """
    if tower_id not in TOWER_REGISTRY:
        return {
            "status": "FAILED",
            "error": f"Tower '{tower_id}' not found in network topology inventory.",
        }

    tower = TOWER_REGISTRY[tower_id]
    ticket_num = random.randint(1000, 9999)
    ticket_id = f"NOC-INC-2026-{ticket_num}"

    # Calculate expected mitigation impact
    old_prb = tower["prb_utilization_pct"]
    reduction = 22.5 if action == "load_balance_xn" else 15.0
    new_prb = max(35.0, round(old_prb - reduction, 1))
    new_latency = max(8.5, round(tower["latency_ms"] * 0.45, 1))

    # Apply updates in simulated database
    tower["prb_utilization_pct"] = new_prb
    tower["latency_ms"] = new_latency
    tower["status"] = TowerStatus.OPTIMAL.value if new_prb < 75.0 else TowerStatus.WARNING.value
    tower["packet_loss_pct"] = round(tower["packet_loss_pct"] * 0.2, 2)

    # Reference standard
    standard_map = {
        "load_balance_xn": "3GPP TS 38.401 Section 8.2 (NG-RAN Inter-gNB Xn-AP)",
        "carrier_aggregation_steer": "3GPP TS 38.331 (RRC SCell Activation)",
        "power_boost_mimo": "3GPP TS 38.104 (gNB Transmit Power Specification)",
        "reroute_traffic": "3GPP TS 23.501 (5GS QoS Flow Rerouting)",
    }

    result = MitigationResult(
        ticket_id=ticket_id,
        tower_id=tower_id,
        action_executed=action,  # type: ignore
        status="SUCCESS",
        prb_reduction_pct=reduction,
        projected_latency_ms=new_latency,
        standard_applied=standard_map.get(action, "3GPP TS 38.401"),
        details={
            "initial_prb_pct": old_prb,
            "post_mitigation_prb_pct": new_prb,
            "target_param": target_param,
            "connected_users": tower["connected_users"],
        },
    )

    # Record in ADK ToolContext state if available
    if ctx and hasattr(ctx, "state") and ctx.state is not None:
        mitigation_history = ctx.state.get("mitigation_history", [])
        mitigation_history.append(result.model_dump())
        ctx.state["mitigation_history"] = mitigation_history

    return result.model_dump()


def consult_3gpp_specifications(
    query: str,
    spec_number: Optional[str] = None,
) -> Dict[str, Any]:
    """Consults the official 3GPP Technical Specifications knowledge repository for telco compliance guidelines.

    Args:
        query: Specific domain topic to consult (e.g., 'Xn load balancing', 'URLLC latency SLA', 'massive MIMO').
        spec_number: Optional 3GPP specification identifier (e.g., 'TS 38.401', 'TS 23.501', 'TS 38.331').

    Returns:
        Matched 3GPP technical specification with authoritative engineering recommendations.
    """
    if spec_number and spec_number in STANDARDS_DB:
        return {
            "spec_number": spec_number,
            **STANDARDS_DB[spec_number],
            "query_matched": query,
        }

    # Search keyword match
    query_lower = query.lower()
    for spec, data in STANDARDS_DB.items():
        if (
            spec.lower() in query_lower
            or any(w in data["title"].lower() for w in query_lower.split())
            or any(w in data["scope"].lower() for w in query_lower.split())
        ):
            return {
                "spec_number": spec,
                **data,
                "query_matched": query,
            }

    # Default to primary architectural standard
    return {
        "spec_number": "TS 38.401",
        **STANDARDS_DB["TS 38.401"],
        "note": "Default 5G architecture reference applied.",
    }


def estimate_sla_financial_impact(
    tower_id: str,
    outage_duration_minutes: int = 15,
    penalty_rate_per_min: float = 120.0,
) -> Dict[str, Any]:
    """Estimates the SLA breach penalties and business financial risk for a congested or degraded cell tower.

    Args:
        tower_id: Identifier of the cell tower (e.g., 'TWR-5G-NY-01').
        outage_duration_minutes: Estimated duration of network impairment in minutes.
        penalty_rate_per_min: Contractual enterprise SLA penalty rate per minute in USD.

    Returns:
        Structured SLAImpactEstimate with subscriber impact, liability amount, and risk classification.
    """
    tower = TOWER_REGISTRY.get(tower_id)
    if not tower:
        return {"error": f"Tower '{tower_id}' not found."}

    users = tower["connected_users"]
    penalty = round(outage_duration_minutes * penalty_rate_per_min * (users / 500.0), 2)

    risk = "SEVERE" if penalty > 5000.0 or tower["status"] == TowerStatus.CRITICAL_OVERLOAD.value else (
        "HIGH" if penalty > 2500.0 else "MEDIUM"
    )

    recommendation = (
        f"Immediately execute load_balance_xn on {tower_id} to transfer active UEs to adjacent cell "
        f"to prevent ${penalty:,.2f} USD enterprise SLA breach."
    )

    estimate = SLAImpactEstimate(
        tower_id=tower_id,
        active_subscribers_impacted=users,
        estimated_penalty_usd=penalty,
        compliance_risk=risk,
        recommendation=recommendation,
    )
    return estimate.model_dump()
