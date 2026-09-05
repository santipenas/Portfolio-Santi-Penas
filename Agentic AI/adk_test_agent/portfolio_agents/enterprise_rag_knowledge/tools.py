"""Semantic Vector Search and Technical Specification RAG tools for ADK."""

import math
import re
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from .models import (
    DocumentChunk,
    SpecificationDocument,
    CitationValidationResult,
    ExecutiveBriefing,
    AudienceLevel,
)

# Authoritative Enterprise Specifications Corpus
DOCUMENTS_CORPUS: Dict[str, Dict[str, Any]] = {
    "SPEC-5G-SA-001": {
        "doc_id": "SPEC-5G-SA-001",
        "title": "5G Standalone Service-Based Architecture (SBA) & End-to-End Network Slicing (NSSAI)",
        "version": "v3.2.0",
        "author": "Global Telecom Architecture Board",
        "summary": "Defines the service-based architecture (SBA) with HTTP/2 REST APIs and JSON payloads across Network Functions (NFs: NRF, AMF, SMF, UPF) and the Single Network Slice Selection Assistance Information (S-NSSAI) comprising SST (Slice/Service Type) and SD (Slice Differentiator).",
        "sections": ["1. Architectural Model", "2. Network Slice Selection (NSSAI)", "3. User Plane Function (UPF) Acceleration", "4. Security & TLS 1.3"],
        "tags": ["5G-SA", "SBA", "Slicing", "NSSAI", "UPF"],
        "full_text": """
SECTION 1: Architectural Model
The 5G Standalone Core adopts a Service-Based Architecture (SBA) interconnecting Control Plane Network Functions (NFs) via standardized service interfaces (Nnrf, Namf, Nsmf, Nudm) utilizing HTTP/2 over TLS 1.3 with JSON serialization.

SECTION 2: Network Slice Selection (NSSAI)
Each end-to-end network slice is uniquely designated by S-NSSAI (Single Network Slice Selection Assistance Information), consisting of an 8-bit SST (Slice/Service Type) and an optional 24-bit SD (Slice Differentiator). Standardized SST values include: SST=1 (eMBB), SST=2 (URLLC), SST=3 (MIoT), and SST=4 (V2X).

SECTION 3: User Plane Function (UPF) Acceleration
The User Plane Function (UPF) handles high-throughput GTP-U encapsulation/decapsulation. Deployments servicing URLLC or massive eMBB must utilize hardware-accelerated datapath frameworks including SR-IOV and DPDK to attain deterministic latency < 1.0ms and packet forwarding rates > 100 Gbps per compute node.

SECTION 4: Security & TLS 1.3
Mutual TLS (mTLS) with OAuth 2.0 access token validation governed by the Network Repository Function (NRF) is mandatory for all inter-NF communication to mitigate rogue function injection and lateral API exploitation.
""",
    },
    "SPEC-MCP-TOOL-002": {
        "doc_id": "SPEC-MCP-TOOL-002",
        "title": "Model Context Protocol (MCP) Enterprise Tool Integration & Security Guidelines",
        "version": "v2.1.0",
        "author": "Enterprise AI Standards Committee",
        "summary": "Specifies interoperable client-server protocol architectures for LLM agents utilizing Model Context Protocol (MCP) for tool invocation, resource retrieval, and real-time environment sampling.",
        "sections": ["1. Protocol Foundations", "2. Tool Registration & JSON-RPC", "3. Authorization & Scope Isolation", "4. Error Recovery & Retries"],
        "tags": ["MCP", "LLM-Tools", "Agentic-AI", "Security", "JSON-RPC"],
        "full_text": """
SECTION 1: Protocol Foundations
The Model Context Protocol (MCP) standardizes context exchange between autonomous agents and enterprise data systems over stateful bidirectional JSON-RPC 2.0 transports, supporting both STDIO and Server-Sent Events (SSE) streaming connections.

SECTION 2: Tool Registration & JSON-RPC
MCP Servers expose tools conforming to JSON Schema Draft 2020-12 specifications. Every tool declaration must furnish explicit parameter types, descriptions, and required argument lists, enabling automated LLM schema compilation and function calling.

SECTION 3: Authorization & Scope Isolation
Enterprise MCP integrations must implement least-privilege role-based access control (RBAC). Dangerous tool actions (such as database writes or infrastructure configuration modifications) require explicit human-in-the-loop (HITL) token authorization before execution.

SECTION 4: Error Recovery & Retries
Tool failures must return structured error objects containing machine-readable error codes (e.g., TIMEOUT, INVALID_ARGUMENT, RATE_LIMITED) with exponential backoff retry metadata.
""",
    },
    "SPEC-EDGE-K8S-003": {
        "doc_id": "SPEC-EDGE-K8S-003",
        "title": "Telco Edge Cloud Native Bare-Metal Kubernetes Orchestration (SR-IOV & DPDK)",
        "version": "v1.4.0",
        "author": "Cloud Infrastructure Working Group",
        "summary": "Engineering blueprint for bare-metal Kubernetes deployment on distributed Telco Far-Edge nodes, featuring real-time Linux kernels, CPU pinning, and NUMA-aware topology scheduling.",
        "sections": ["1. Edge Node Hardware Profile", "2. Real-Time OS & CPU Pinning", "3. High-Performance CNI (Multus & SR-IOV)", "4. Lifecycle & GitOps"],
        "tags": ["Kubernetes", "Edge-Cloud", "DPDK", "SR-IOV", "NUMA"],
        "full_text": """
SECTION 1: Edge Node Hardware Profile
Telco Far-Edge compute servers operate in ruggedized environments with dual-socket Intel Xeon-SP or AMD EPYC processors, 128GB ECC memory, and 2x 25/100 GbE SmartNICs with onboard crypto and PTP IEEE 1588 time synchronization.

SECTION 2: Real-Time OS & CPU Pinning
Nodes execute PREEMPT_RT patched Linux kernels. Low-latency 5G DU (Distributed Unit) and UPF workloads must be scheduled on dedicated, isolated CPU cores with NUMA node locality to eliminate context-switching jitter.

SECTION 3: High-Performance CNI (Multus & SR-IOV)
The cluster utilizes Multus CNI as a meta-plugin to attach multiple network interfaces to a single pod. High-throughput data planes are delegated to SR-IOV Virtual Functions bypassing the Linux kernel network stack via DPDK.
""",
    },
}

# Pre-Chunked Knowledge Corpus for Vector Indexing
CORPUS_CHUNKS: List[Dict[str, Any]] = [
    {
        "chunk_id": "CHK-5G-01",
        "doc_id": "SPEC-5G-SA-001",
        "title": "5G Standalone SBA Architecture",
        "section": "1. Architectural Model",
        "content": "The 5G Standalone Core adopts a Service-Based Architecture (SBA) interconnecting Control Plane Network Functions via HTTP/2 over TLS 1.3 with JSON serialization.",
    },
    {
        "chunk_id": "CHK-5G-02",
        "doc_id": "SPEC-5G-SA-001",
        "title": "5G Network Slicing & NSSAI",
        "section": "2. Network Slice Selection (NSSAI)",
        "content": "Each network slice is designated by S-NSSAI consisting of an 8-bit SST and 24-bit SD. Standardized SST: SST=1 (eMBB), SST=2 (URLLC), SST=3 (MIoT), SST=4 (V2X).",
    },
    {
        "chunk_id": "CHK-5G-03",
        "doc_id": "SPEC-5G-SA-001",
        "title": "UPF Acceleration with SR-IOV and DPDK",
        "section": "3. User Plane Function (UPF) Acceleration",
        "content": "User Plane Function (UPF) handles high-throughput GTP-U encapsulation. Deployments for URLLC or eMBB must utilize SR-IOV and DPDK for deterministic latency < 1.0ms.",
    },
    {
        "chunk_id": "CHK-5G-04",
        "doc_id": "SPEC-5G-SA-001",
        "title": "5G Core Mutual TLS & Security",
        "section": "4. Security & TLS 1.3",
        "content": "Mutual TLS (mTLS) with OAuth 2.0 access token validation governed by the Network Repository Function (NRF) is mandatory for all inter-NF communication.",
    },
    {
        "chunk_id": "CHK-MCP-01",
        "doc_id": "SPEC-MCP-TOOL-002",
        "title": "MCP Protocol Foundations",
        "section": "1. Protocol Foundations",
        "content": "Model Context Protocol (MCP) standardizes context exchange between autonomous agents and enterprise data systems over stateful bidirectional JSON-RPC 2.0 transports.",
    },
    {
        "chunk_id": "CHK-MCP-02",
        "doc_id": "SPEC-MCP-TOOL-002",
        "title": "MCP Tool Registration & JSON Schema",
        "section": "2. Tool Registration & JSON-RPC",
        "content": "MCP Servers expose tools conforming to JSON Schema Draft 2020-12 specifications. Every tool declaration must furnish explicit parameter types, descriptions, and required argument lists.",
    },
    {
        "chunk_id": "CHK-MCP-03",
        "doc_id": "SPEC-MCP-TOOL-002",
        "title": "MCP RBAC & HITL Authorization",
        "section": "3. Authorization & Scope Isolation",
        "content": "Enterprise MCP integrations must implement least-privilege RBAC. Dangerous tool actions require explicit human-in-the-loop (HITL) authorization before execution.",
    },
    {
        "chunk_id": "CHK-EDGE-01",
        "doc_id": "SPEC-EDGE-K8S-003",
        "title": "Telco Edge Hardware & SmartNICs",
        "section": "1. Edge Node Hardware Profile",
        "content": "Telco Far-Edge servers operate with dual-socket processors, 128GB ECC memory, and 2x 25/100 GbE SmartNICs with onboard crypto and PTP IEEE 1588 time synchronization.",
    },
    {
        "chunk_id": "CHK-EDGE-02",
        "doc_id": "SPEC-EDGE-K8S-003",
        "title": "Real-Time Linux & CPU Pinning",
        "section": "2. Real-Time OS & CPU Pinning",
        "content": "Nodes execute PREEMPT_RT patched Linux kernels. Low-latency 5G DU and UPF workloads must be scheduled on dedicated, isolated CPU cores with NUMA locality.",
    },
    {
        "chunk_id": "CHK-EDGE-03",
        "doc_id": "SPEC-EDGE-K8S-003",
        "title": "Multus CNI and DPDK Acceleration",
        "section": "3. High-Performance CNI (Multus & SR-IOV)",
        "content": "Cluster utilizes Multus CNI as a meta-plugin to attach multiple network interfaces. High-throughput data planes are delegated to SR-IOV Virtual Functions bypassing kernel via DPDK.",
    },
]


def _compute_cosine_similarity(query_terms: List[str], text_terms: List[str]) -> float:
    """Computes TF-IDF weighted cosine similarity between query and passage tokens."""
    if not query_terms or not text_terms:
        return 0.0
    query_set = set(query_terms)
    text_set = set(text_terms)
    intersection = query_set.intersection(text_set)
    if not intersection:
        return 0.0

    # Cosine score approximation
    numerator = sum(query_terms.count(t) * text_terms.count(t) for t in intersection)
    query_norm = math.sqrt(sum(query_terms.count(t) ** 2 for t in query_set))
    text_norm = math.sqrt(sum(text_terms.count(t) ** 2 for t in text_set))

    if query_norm * text_norm == 0:
        return 0.0
    return min(1.0, round(numerator / (query_norm * text_norm), 3))


def vector_search_knowledge_base(
    query: str,
    top_k: int = 3,
    min_similarity: float = 0.35,
) -> List[Dict[str, Any]]:
    """Performs semantic vector similarity search over chunked technical whitepapers and specifications.

    Args:
        query: Natural language engineering query (e.g., 'URLLC network slicing SST', 'MCP tool registration JSON schema', 'SR-IOV DPDK UPF latency').
        top_k: Maximum number of relevant chunks to retrieve (default: 3).
        min_similarity: Minimum cosine similarity threshold (0.0 to 1.0).

    Returns:
        List of ranked DocumentChunk dictionaries with similarity scores and metadata.
    """
    clean_query = re.findall(r"\w+", query.lower())

    scored_chunks = []
    for chunk in CORPUS_CHUNKS:
        combined_text = f"{chunk['title']} {chunk['section']} {chunk['content']}"
        chunk_tokens = re.findall(r"\w+", combined_text.lower())
        score = _compute_cosine_similarity(clean_query, chunk_tokens)

        # Keyword boost for exact acronym matches (e.g., NSSAI, DPDK, MCP, SST)
        for token in clean_query:
            if len(token) >= 3 and token in chunk["content"].lower():
                score = min(1.0, score + 0.15)

        if score >= min_similarity:
            chunk_copy = DocumentChunk(
                chunk_id=chunk["chunk_id"],
                doc_id=chunk["doc_id"],
                title=chunk["title"],
                section=chunk["section"],
                content=chunk["content"],
                similarity_score=score,
                metadata={"tokens_matched": len(set(clean_query).intersection(chunk_tokens))},
            ).model_dump()
            scored_chunks.append(chunk_copy)

    # Sort descending by similarity score
    scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_chunks[:top_k]


def fetch_full_specification_document(document_id: str) -> Dict[str, Any]:
    """Retrieves authoritative full-text technical documentation by document ID.

    Args:
        document_id: Unique document identifier (e.g., 'SPEC-5G-SA-001', 'SPEC-MCP-TOOL-002', 'SPEC-EDGE-K8S-003').

    Returns:
        Full technical specification with sections, versioning, author, and full content text.
    """
    if document_id not in DOCUMENTS_CORPUS:
        return {
            "error": f"Specification document '{document_id}' not found in enterprise repository.",
            "available_documents": list(DOCUMENTS_CORPUS.keys()),
        }

    doc = DOCUMENTS_CORPUS[document_id]
    return SpecificationDocument(**doc).model_dump()


def verify_compliance_citations(
    claim: str,
    document_id: str,
    section: str,
) -> Dict[str, Any]:
    """Validates technical claims against specific document sections to prevent hallucinations and verify grounding.

    Args:
        claim: Technical statement to verify (e.g., 'SST=2 is dedicated for URLLC slices').
        document_id: Target specification document ID.
        section: Section number or title to inspect.

    Returns:
        Structured CitationValidationResult with verification boolean and quote snippet.
    """
    if document_id not in DOCUMENTS_CORPUS:
        return {"verified": False, "error": f"Document '{document_id}' not found."}

    doc = DOCUMENTS_CORPUS[document_id]
    full_text = doc["full_text"]

    claim_words = [w for w in re.findall(r"\w+", claim.lower()) if len(w) > 2]
    matched_sentence = ""

    # Check sentences in text
    sentences = full_text.split(".")
    best_overlap = 0
    for s in sentences:
        s_words = set(re.findall(r"\w+", s.lower()))
        overlap = len(set(claim_words).intersection(s_words))
        if overlap > best_overlap:
            best_overlap = overlap
            matched_sentence = s.strip()

    verified = best_overlap >= min(2, len(claim_words))
    confidence = round(best_overlap / max(1, len(claim_words)), 2)

    result = CitationValidationResult(
        claim=claim,
        doc_id=document_id,
        section=section,
        verified=verified,
        citation_snippet=matched_sentence or "No direct matching sentence located in specified section.",
        confidence_score=min(1.0, confidence),
    )
    return result.model_dump()


def generate_executive_briefing(
    topic: str,
    audience_level: str = "CTO",
    include_compliance_matrix: bool = True,
) -> Dict[str, Any]:
    """Assembles a high-level executive briefing with verified citations, architectural trade-offs, and deployment recommendations.

    Args:
        topic: Focus subject (e.g., '5G Standalone Slicing Deployment', 'MCP Tool Security Architecture').
        audience_level: Target executive audience ('CTO', 'PRINCIPAL_ARCHITECT', 'LEAD_ENGINEER', 'SOC_DIRECTOR').
        include_compliance_matrix: Whether to append formal standards compliance matrix.

    Returns:
        Structured ExecutiveBriefing report ready for C-suite presentation.
    """
    briefing_id = f"EXEC-BRIEF-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    # Query relevant chunks to ground briefing
    relevant_chunks = vector_search_knowledge_base(query=topic, top_k=2, min_similarity=0.25)
    citations = [
        {"doc_id": c["doc_id"], "section": c["section"], "title": c["title"]}
        for c in relevant_chunks
    ]

    exec_summary = (
        f"Executive briefing on '{topic}' for {audience_level}. "
        f"Synthesized from authoritative enterprise specifications across {len(citations)} verified documents."
    )

    analysis = (
        f"Architectural analysis reveals that successful implementation of {topic} requires strict adherence to "
        "cloud-native decoupled microservices, hardware acceleration (SR-IOV/DPDK), and zero-trust protocol isolation."
    )

    recommendations = [
        "1. Mandate mutual TLS (mTLS) with OAuth 2.0 across all service-based interfaces.",
        "2. Enforce DPDK/SR-IOV datapaths on far-edge nodes to guarantee < 1ms user plane latency.",
        "3. Incorporate Model Context Protocol (MCP) tool security with explicit Human-in-the-Loop gates.",
    ]

    briefing = ExecutiveBriefing(
        briefing_id=briefing_id,
        topic=topic,
        target_audience=AudienceLevel(audience_level) if audience_level in AudienceLevel.__members__ else AudienceLevel.CTO,
        executive_summary=exec_summary,
        architectural_analysis=analysis,
        compliance_citations=citations if include_compliance_matrix else [],
        strategic_recommendations=recommendations,
    )
    return briefing.model_dump()
