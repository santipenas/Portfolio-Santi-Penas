"""Autonomous SecOps Swarm Agent built with Google ADK.

Domain: Cyber Security, Threat Hunting & Autonomous Perimeter Defense.
Architecture: Hierarchical Multi-Agent Swarm with Coordinator & 3 Specialized Subagents.
"""

from google.adk.agents import Agent
from .tools import (
    scan_threat_intelligence_feed,
    deploy_firewall_countermeasure,
    extract_forensic_iocs,
    dispatch_soc_incident_ticket,
)

# 1. Specialized Threat Hunter Subagent
threat_hunter_agent = Agent(
    name="threat_hunter",
    model="gemini-2.5-flash",
    description="Specialized subagent responsible for scanning global threat feeds, SIEM logs, identifying malicious attack vectors, and extracting forensic IOCs.",
    instruction="""You are the Threat Hunter Specialist subagent in the Autonomous SecOps Swarm.
Your responsibility:
- Ingest real-time threat intelligence feeds using `scan_threat_intelligence_feed`.
- Perform forensic analysis on active attacks using `extract_forensic_iocs`.
- Identify Indicators of Compromise (IOCs) and determine CVSS risk severity.
Hand off verified threat targets to the Firewall Mitigator or SOC Dispatcher.
""",
    tools=[scan_threat_intelligence_feed, extract_forensic_iocs],
)

# 2. Specialized Perimeter Defense & Firewall Mitigator Subagent
firewall_mitigator_agent = Agent(
    name="firewall_mitigator",
    model="gemini-2.5-flash",
    description="Specialized subagent responsible for provisioning and deploying edge firewall ACLs, rate limiting, and BGP Flowspec blackholing.",
    instruction="""You are the Perimeter Firewall Mitigation Specialist subagent.
Your responsibility:
- Rapidly neutralize malicious IPs by deploying edge ACLs and scrubbing rules using `deploy_firewall_countermeasure`.
- Select appropriate rule actions ('DROP', 'REJECT', 'BLACKHOLE', 'RATE_LIMIT') depending on whether the attack is volumetric DDoS or targeted injection.
- Confirm perimeter policy enforcement and return active rule IDs (FW-RULE-XXXX).
""",
    tools=[deploy_firewall_countermeasure],
)

# 3. Specialized SOC Dispatcher Subagent
soc_dispatcher_agent = Agent(
    name="soc_dispatcher",
    model="gemini-2.5-flash",
    description="Specialized subagent responsible for compiling formal security incident packages and dispatching P1/P2 tickets to On-Call engineering.",
    instruction="""You are the SOC Dispatcher Specialist subagent.
Your responsibility:
- Compile executive forensic summaries containing verified IOCs, CVSS scores, and containment status.
- Dispatch high-priority incident tickets to the Security Operations Center using `dispatch_soc_incident_ticket`.
- Confirm on-call notification and ticket tracking IDs.
""",
    tools=[dispatch_soc_incident_ticket],
)

# 4. Swarm Coordinator Root Agent
SWARM_COORDINATOR_INSTRUCTION = """You are the Autonomous SecOps Swarm Coordinator Agent, engineered using Google ADK.

You lead a defensive multi-agent security swarm defending critical telecom infrastructure, cloud APIs, and subscriber data repositories against active cyber threats.

Swarm Architecture & Delegation:
1. Threat Discovery & Triage:
   - Delegate threat hunting and IOC extraction to the `threat_hunter` subagent, or invoke `scan_threat_intelligence_feed` and `extract_forensic_iocs` directly.
2. Perimeter Countermeasures:
   - Delegate active perimeter containment to the `firewall_mitigator` subagent, or invoke `deploy_firewall_countermeasure` to provision immediate edge block rules.
3. Incident Documentation & SOC Dispatch:
   - Delegate ticket logging to the `soc_dispatcher` subagent, or invoke `dispatch_soc_incident_ticket` to notify Tier-2 On-Call engineers.

Execution Philosophy:
- Prioritize rapid containment of CRITICAL and HIGH severity attacks (DDoS, SQLi, Auth Brute-Force).
- Always enforce least-privilege edge rules and document full forensic audit trails with IOCs and CVSS metrics.
"""

root_agent = Agent(
    name="autonomous_secops_swarm",
    model="gemini-2.5-flash",
    description="Autonomous cybersecurity multi-agent swarm coordinator orchestrating threat hunting, perimeter firewall containment, and SOC escalation.",
    instruction=SWARM_COORDINATOR_INSTRUCTION,
    sub_agents=[
        threat_hunter_agent,
        firewall_mitigator_agent,
        soc_dispatcher_agent,
    ],
    tools=[
        scan_threat_intelligence_feed,
        deploy_firewall_countermeasure,
        extract_forensic_iocs,
        dispatch_soc_incident_ticket,
    ],
)
