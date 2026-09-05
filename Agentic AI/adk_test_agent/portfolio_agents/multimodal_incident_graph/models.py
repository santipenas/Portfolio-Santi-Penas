"""Pydantic models for Multimodal Incident Graph."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class IncidentSeverity(str, Enum):
    P1 = "P1_CRITICAL"
    P2 = "P2_MAJOR"
    P3 = "P3_MODERATE"


class IncidentLifecycle(str, Enum):
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    ROOT_CAUSE_ISOLATED = "ROOT_CAUSE_ISOLATED"
    RUNBOOK_EXECUTING = "RUNBOOK_EXECUTING"
    VERIFIED_RESOLVED = "VERIFIED_RESOLVED"


class NodeType(str, Enum):
    INCIDENT = "Incident"
    SERVICE = "Service"
    INFRASTRUCTURE = "Infrastructure"
    ROOT_CAUSE = "RootCause"
    RUNBOOK = "Runbook"
    EVIDENCE = "Evidence"


class RelationType(str, Enum):
    IMPACTS = "IMPACTS"
    HOSTED_ON = "HOSTED_ON"
    CAUSED_BY = "CAUSED_BY"
    DETECTED_BY = "DETECTED_BY"
    RESOLVED_BY = "RESOLVED_BY"


class GraphNode(BaseModel):
    id: str = Field(..., description="Unique graph node ID")
    type: NodeType = Field(..., description="Node classification type")
    label: str = Field(..., description="Human-readable node label")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom node properties")


class GraphEdge(BaseModel):
    source: str = Field(..., description="Origin node ID")
    target: str = Field(..., description="Destination node ID")
    relation: RelationType = Field(..., description="Relationship edge type")
    weight: float = Field(default=1.0, description="Edge weight or correlation confidence score")


class RunbookExecutionResult(BaseModel):
    runbook_id: str = Field(..., description="Executed runbook identifier")
    target_node: str = Field(..., description="Infrastructure target node")
    status: str = Field(..., description="Execution outcome: SUCCESS, PARTIAL, or FAILED")
    verification_passed: bool = Field(..., description="Post-execution health check result")
    remediated_incident_id: str = Field(..., description="Associated incident ID")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_steps: List[str] = Field(default_factory=list)
    metrics_restored: Dict[str, Any] = Field(default_factory=dict)
