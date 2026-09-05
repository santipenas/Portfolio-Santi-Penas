"""Pydantic models for Enterprise RAG Knowledge."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AudienceLevel(str, Enum):
    CTO = "CTO"
    PRINCIPAL_ARCHITECT = "PRINCIPAL_ARCHITECT"
    LEAD_ENGINEER = "LEAD_ENGINEER"
    SOC_DIRECTOR = "SOC_DIRECTOR"


class DocumentChunk(BaseModel):
    chunk_id: str = Field(..., description="Unique chunk identifier")
    doc_id: str = Field(..., description="Parent specification document ID")
    title: str = Field(..., description="Document title")
    section: str = Field(..., description="Section title or number")
    content: str = Field(..., description="Text content excerpt")
    similarity_score: float = Field(default=0.0, description="Cosine similarity score (0.0 to 1.0)")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SpecificationDocument(BaseModel):
    doc_id: str = Field(..., description="Authoritative document ID (e.g., SPEC-5G-SA-001)")
    title: str = Field(..., description="Official document title")
    version: str = Field(..., description="Version string (e.g., v3.2.0)")
    author: str = Field(..., description="Authoring organization or committee")
    summary: str = Field(..., description="High-level executive abstract")
    sections: List[str] = Field(default_factory=list, description="Available document sections")
    tags: List[str] = Field(default_factory=list, description="Domain classification tags")
    last_revised: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CitationValidationResult(BaseModel):
    claim: str = Field(..., description="Claim evaluated for technical correctness")
    doc_id: str = Field(..., description="Referenced specification ID")
    section: str = Field(..., description="Referenced document section")
    verified: bool = Field(..., description="Whether claim is grounded in source text")
    citation_snippet: str = Field(..., description="Extracted supporting source quote")
    confidence_score: float = Field(..., description="Verification confidence score")


class ExecutiveBriefing(BaseModel):
    briefing_id: str = Field(..., description="Unique briefing report identifier")
    topic: str = Field(..., description="Subject of the briefing")
    target_audience: AudienceLevel = Field(..., description="Target executive audience")
    executive_summary: str = Field(..., description="Concise high-level synthesis")
    architectural_analysis: str = Field(..., description="Deep technical breakdown")
    compliance_citations: List[Dict[str, Any]] = Field(default_factory=list)
    strategic_recommendations: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
