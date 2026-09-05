"""Comprehensive unit and integration tests for Enterprise RAG Knowledge."""

import pytest
from portfolio_agents.enterprise_rag_knowledge.agent import root_agent
from portfolio_agents.enterprise_rag_knowledge.tools import (
    vector_search_knowledge_base,
    fetch_full_specification_document,
    verify_compliance_citations,
    generate_executive_briefing,
    DOCUMENTS_CORPUS,
)


def test_root_agent_configuration():
    assert root_agent.name == "enterprise_rag_knowledge"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.tools) == 4
    tool_names = [getattr(t, "__name__", str(t)) for t in root_agent.tools]
    assert "vector_search_knowledge_base" in tool_names
    assert "fetch_full_specification_document" in tool_names
    assert "verify_compliance_citations" in tool_names
    assert "generate_executive_briefing" in tool_names
    assert "RAG" in root_agent.description or "rag" in root_agent.description


def test_vector_search_knowledge_base_5g():
    results = vector_search_knowledge_base(query="URLLC network slicing SST values", top_k=2)
    assert len(results) >= 1
    top_chunk = results[0]
    assert top_chunk["doc_id"] == "SPEC-5G-SA-001"
    assert top_chunk["similarity_score"] > 0.3
    assert "SST" in top_chunk["content"] or "slice" in top_chunk["content"].lower()


def test_vector_search_knowledge_base_mcp():
    results = vector_search_knowledge_base(query="Model Context Protocol MCP JSON-RPC tools", top_k=2)
    assert len(results) >= 1
    top_chunk = results[0]
    assert top_chunk["doc_id"] == "SPEC-MCP-TOOL-002"
    assert "MCP" in top_chunk["title"] or "JSON" in top_chunk["content"]


def test_fetch_full_specification_document():
    doc = fetch_full_specification_document("SPEC-5G-SA-001")
    assert "error" not in doc
    assert doc["doc_id"] == "SPEC-5G-SA-001"
    assert "5G Standalone" in doc["title"]
    assert len(doc["sections"]) >= 4
    assert "SBA" in doc["tags"]

    invalid_doc = fetch_full_specification_document("SPEC-DOES-NOT-EXIST")
    assert "error" in invalid_doc


def test_verify_compliance_citations():
    claim = "SST=2 represents URLLC standardized slice"
    result = verify_compliance_citations(
        claim=claim,
        document_id="SPEC-5G-SA-001",
        section="2. Network Slice Selection (NSSAI)",
    )
    assert result["verified"] is True
    assert result["doc_id"] == "SPEC-5G-SA-001"
    assert result["confidence_score"] > 0.0
    assert len(result["citation_snippet"]) > 0


def test_generate_executive_briefing():
    briefing = generate_executive_briefing(
        topic="5G Standalone Slicing Implementation",
        audience_level="CTO",
        include_compliance_matrix=True,
    )
    assert "briefing_id" in briefing
    assert briefing["topic"] == "5G Standalone Slicing Implementation"
    assert briefing["target_audience"] == "CTO"
    assert len(briefing["strategic_recommendations"]) >= 3
    assert len(briefing["compliance_citations"]) >= 1
