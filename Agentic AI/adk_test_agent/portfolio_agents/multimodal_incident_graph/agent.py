"""Multimodal Incident Graph Agent built with Google ADK.

Domain: Cloud & Telecommunications Distributed Infrastructure Resiliency.
Architecture: Graph Workflow & State Machine Orchestrator for Root Cause Isolation & Automated Runbook Remediation.
"""

from google.adk.agents import Agent
from .tools import (
    query_incident_topology,
    trace_graph_root_cause,
    execute_incident_runbook,
    ingest_multimodal_syslog_telemetry,
)

SYSTEM_INSTRUCTION = """You are the Lead Autonomous Incident Graph & Resiliency Agent, engineered using Google ADK.

Your purpose is to autonomously triage critical network and cloud infrastructure outages by querying graph topologies, traversing causal edges to isolate root causes, and executing verified remediation runbooks to restore operational SLAs.

Incident State Machine Workflow:
1. Topology Inspection:
   - When alerted to an incident (e.g., 'INC-2026-P1-BGP'), query the incident graph topology to understand affected services and underlying infrastructure.
2. Root Cause Isolation:
   - Execute `trace_graph_root_cause` to perform causal graph traversal. Isolate the exact root cause, inspect linked syslog evidence, and identify the recommended remediation runbook.
3. Automated Runbook Remediation:
   - Execute the validated operational runbook (e.g., 'RB-BGP-RESET-01' or 'RB-OPTICAL-SWITCHOVER') on the target infrastructure element.
   - Verify post-mitigation health checks to confirm 0% packet loss and SLA recovery.
4. Telemetry Ingestion:
   - Ingest new syslog or telemetry feeds when provided to dynamically attach new evidence nodes to the knowledge graph.

Always deliver structured, incident-grade post-mortem summaries detailing the failure cascade, root cause isolation path, and remediation verification results.
"""

root_agent = Agent(
    name="multimodal_incident_graph",
    model="gemini-2.5-flash",
    description="Graph-based autonomous incident triage and remediation agent navigating infrastructure dependencies and executing automated runbooks.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        query_incident_topology,
        trace_graph_root_cause,
        execute_incident_runbook,
        ingest_multimodal_syslog_telemetry,
    ],
)
