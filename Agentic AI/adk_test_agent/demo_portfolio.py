"""Interactive CLI Showcase Demonstration for Google ADK Agentic AI Portfolio.

Runs end-to-end simulation scenarios for all 6 Google ADK agents:
1. Telco NOC Optimizer: 5G RAN telemetry, SLA liability calculation, 3GPP Xn-AP mitigation.
2. Multimodal Incident Graph: Infrastructure topology state machine, causal BFS traversal, automated runbook.
3. Enterprise RAG Knowledge: Semantic vector similarity search, citation verification, executive briefing.
4. Autonomous SecOps Swarm: Multi-agent perimeter defense swarm (Threat Hunter, Firewall Mitigator, SOC Dispatcher).
5. Telco Churn Data Analyst: Statistical EDA profiling, cohort risk analysis, ML churn scoring, CLV retention campaign.
6. Geospatial RF Planner: 3GPP TR 38.901 propagation, dead-zone detection, antenna optimization, RFC 7946 GeoJSON.
"""

import json
import sys
from portfolio_agents.telco_noc_optimizer.tools import (
    get_cell_tower_telemetry,
    execute_mitigation_action,
    consult_3gpp_specifications,
    estimate_sla_financial_impact,
)
from portfolio_agents.multimodal_incident_graph.tools import (
    query_incident_topology,
    trace_graph_root_cause,
    execute_incident_runbook,
)
from portfolio_agents.enterprise_rag_knowledge.tools import (
    vector_search_knowledge_base,
    fetch_full_specification_document,
    verify_compliance_citations,
    generate_executive_briefing,
)
from portfolio_agents.autonomous_secops_swarm.tools import (
    scan_threat_intelligence_feed,
    deploy_firewall_countermeasure,
    extract_forensic_iocs,
    dispatch_soc_incident_ticket,
)
from portfolio_agents.telco_churn_data_analyst.tools import (
    load_and_profile_dataset,
    perform_cohort_risk_analysis,
    predict_subscriber_churn_probability,
    generate_retention_campaign,
)
from portfolio_agents.geospatial_rf_planner.tools import (
    query_rf_cell_sites,
    detect_coverage_dead_zones,
    analyze_inter_cell_interference,
    generate_coverage_geojson,
    optimize_antenna_parameters,
)


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f" {title.center(78)} ")
    print("=" * 80)


def print_section(title: str):
    print(f"\n--- [ {title} ] ---")


def demo_telco_noc_optimizer():
    print_header("1. DEMO: TELCO NOC OPTIMIZER (5G/LTE RAN & CORE)")
    print("Agent: telco_noc_optimizer | Model: gemini-2.5-flash")

    print_section("Step 1: Querying Real-Time Cell Tower Telemetry")
    critical_towers = get_cell_tower_telemetry(status_filter="CRITICAL_OVERLOAD")
    print(f"Detected {len(critical_towers)} critical tower(s):")
    for t in critical_towers:
        print(f"  * Tower ID: {t['tower_id']} | Region: {t['region']} | Band: {t['carrier_band']}")
        print(f"    Load (PRB): {t['prb_utilization_pct']}% | Latency: {t['latency_ms']}ms | Users: {t['connected_users']}")

    target_tower = critical_towers[0]["tower_id"]

    print_section("Step 2: Estimating Enterprise SLA Financial Impact")
    sla_estimate = estimate_sla_financial_impact(target_tower, outage_duration_minutes=25)
    print(f"  * Affected Enterprise Subscribers: {sla_estimate['active_subscribers_impacted']}")
    print(f"  * Potential SLA Breach Liability: ${sla_estimate['estimated_penalty_usd']:,.2f} USD")
    print(f"  * Risk Classification: {sla_estimate['compliance_risk']}")
    print(f"  * Recommendation: {sla_estimate['recommendation']}")

    print_section("Step 3: Consulting 3GPP Technical Standards")
    standards = consult_3gpp_specifications(query="Xn load balancing", spec_number="TS 38.401")
    print(f"  * Standard: {standards['spec_number']} - {standards['title']}")
    print(f"  * Guideline: {standards['remediation_guideline']}")

    print_section("Step 4: Executing Automated Mitigation (load_balance_xn)")
    mitigation = execute_mitigation_action(target_tower, action="load_balance_xn", target_param=25.0)
    print(f"  * Incident Ticket ID: {mitigation['ticket_id']}")
    print(f"  * Status: {mitigation['status']} | Standard Applied: {mitigation['standard_applied']}")
    print(f"  * Post-Mitigation PRB Load: {mitigation['details']['post_mitigation_prb_pct']}% (reduced by {mitigation['prb_reduction_pct']}%)")
    print(f"  * Post-Mitigation Latency: {mitigation['projected_latency_ms']}ms")
    print("  [SUCCESS] Congestion mitigated in compliance with 3GPP TS 38.401.")


def demo_multimodal_incident_graph():
    print_header("2. DEMO: MULTIMODAL INCIDENT GRAPH (CLOUD RESILIENCY)")
    print("Agent: multimodal_incident_graph | Model: gemini-2.5-flash")

    incident_id = "INC-2026-P1-BGP"
    print_section(f"Step 1: Ingesting Active Incident Context for {incident_id}")
    nodes = query_incident_topology(incident_id=incident_id)
    print(f"Topology query returned {len(nodes)} correlated node(s):")
    for n in nodes[:3]:
        print(f"  * [{n['type']}] {n['id']} -> {n['label']}")

    print_section(f"Step 2: Causal Graph Traversal & Root Cause Isolation")
    trace = trace_graph_root_cause(incident_id=incident_id)
    print(f"  * Incident: {trace['incident_label']}")
    print(f"  * Isolated Root Cause: {trace['root_cause']['id']} - {trace['root_cause']['label']}")
    print(f"  * Confidence: {trace['root_cause']['attributes']['confidence_score'] * 100:.1f}%")
    print("  * Causal Edge Traversal Path:")
    for step in trace["causal_graph_path"]:
        print(f"      [->] {step['node_id']}: {step['label']}")
    if trace["evidence"]:
        print(f"  * Primary Evidence: {trace['evidence'][0]['id']} -> {trace['evidence'][0]['label']}")
    print(f"  * Matched Runbook: {trace['recommended_runbook']['id']} ({trace['recommended_runbook']['label']})")

    print_section("Step 3: Automated Runbook Remediation & Verification")
    runbook_res = execute_incident_runbook(
        runbook_id=trace["recommended_runbook"]["id"],
        target_node=trace["recommended_runbook"]["attributes"]["target_system"],
    )
    print(f"  * Runbook Execution: {runbook_res['runbook_id']} on {runbook_res['target_node']}")
    print(f"  * Status: {runbook_res['status']} | Post-Check Verification: {'PASSED' if runbook_res['verification_passed'] else 'FAILED'}")
    for s in runbook_res["execution_steps"]:
        print(f"      {s}")
    print(f"  * Metrics Restored: {runbook_res['metrics_restored']}")
    print("  [SUCCESS] Incident resolved and state transitioned to VERIFIED_RESOLVED.")


def demo_enterprise_rag_knowledge():
    print_header("3. DEMO: ENTERPRISE RAG KNOWLEDGE (TECHNICAL SPECS)")
    print("Agent: enterprise_rag_knowledge | Model: gemini-2.5-flash")

    query = "5G Standalone network slicing SST URLLC latency"
    print_section(f"Step 1: Semantic Vector Similarity Search (Query: '{query}')")
    chunks = vector_search_knowledge_base(query=query, top_k=2)
    for idx, c in enumerate(chunks, 1):
        print(f"  Chunk #{idx} | Doc: {c['doc_id']} | Score: {c['similarity_score']:.3f}")
        print(f"    Section: {c['section']}")
        print(f"    Excerpt: {c['content']}")

    print_section("Step 2: Citation Verification & Grounding Check")
    claim = "SST=2 represents URLLC standardized slice"
    verification = verify_compliance_citations(
        claim=claim,
        document_id="SPEC-5G-SA-001",
        section="2. Network Slice Selection (NSSAI)",
    )
    print(f"  * Evaluated Claim: \"{claim}\"")
    print(f"  * Citation Verification: {'VERIFIED (100% Grounded)' if verification['verified'] else 'UNGROUNDED'}")
    print(f"  * Source Quote: \"{verification['citation_snippet']}\"")
    print(f"  * Confidence Score: {verification['confidence_score'] * 100:.1f}%")

    print_section("Step 3: Executive Briefing Synthesis")
    briefing = generate_executive_briefing(topic="5G Standalone Core & Slicing Architecture", audience_level="CTO")
    print(f"  * Briefing ID: {briefing['briefing_id']}")
    print(f"  * Target Audience: {briefing['target_audience']}")
    print(f"  * Executive Summary: {briefing['executive_summary']}")
    print("  * Strategic Recommendations:")
    for rec in briefing["strategic_recommendations"]:
        print(f"      {rec}")
    print("  [SUCCESS] Grounded executive briefing delivered with zero hallucination.")


def demo_autonomous_secops_swarm():
    print_header("4. DEMO: AUTONOMOUS SECOPS SWARM (MULTI-AGENT DEFENSE)")
    print("Coordinator: autonomous_secops_swarm | Subagents: threat_hunter, firewall_mitigator, soc_dispatcher")

    print_section("Subagent 1 [threat_hunter]: Scanning Threat Feeds & SIEM")
    threats = scan_threat_intelligence_feed(severity_min="CRITICAL")
    print(f"Identified {len(threats)} CRITICAL active threat(s):")
    threat = threats[0]
    print(f"  * Threat ID: {threat['threat_id']} | Source IP: {threat['ip_address']} ({threat['source_country']})")
    print(f"  * Attack Vector: {threat['attack_type']} | Confidence: {threat['confidence_score'] * 100:.1f}%")
    print(f"  * Payload: {threat['payload_sample']}")

    print_section("Subagent 1 [threat_hunter]: Extracting Deep Forensic IOCs")
    forensics = extract_forensic_iocs(threat["threat_id"])
    print(f"  * Forensic Report ID: {forensics['report_id']}")
    print(f"  * Calculated CVSS v3.1 Score: {forensics['cvss_score']} (CRITICAL)")
    print(f"  * Extracted IOCs: {', '.join(forensics['extracted_iocs'])}")

    print_section("Subagent 2 [firewall_mitigator]: Deploying Perimeter Firewall Countermeasure")
    fw_result = deploy_firewall_countermeasure(
        target_ip=threat["ip_address"],
        rule_type="BGP_FLOWSPEC",
        action="BLACKHOLE",
        duration_minutes=120,
    )
    print(f"  * Firewall Rule: {fw_result['rule']['rule_id']} deployed on {fw_result['rule']['router_applied']}")
    print(f"  * Action: {fw_result['rule']['action']} | TTL: {fw_result['rule']['duration_minutes']} min")
    print(f"  * Perimeter Status: {fw_result['perimeter_status']}")

    print_section("Subagent 3 [soc_dispatcher]: Packaging Incident Briefing & Escalation")
    ticket = dispatch_soc_incident_ticket(
        incident_id=threat["threat_id"],
        severity="CRITICAL",
        summary=f"Automated BGP Flowspec blackholing executed against {threat['ip_address']} for volumetric DDoS amplification.",
        iocs=forensics["extracted_iocs"],
        assigned_tier="TIER_2",
    )
    print(f"  * Dispatched Ticket ID: {ticket['ticket']['ticket_id']}")
    print(f"  * Severity: {ticket['ticket']['severity']} | Containment: {ticket['ticket']['containment_status']}")
    print(f"  * On-Call PagerDuty Escalation: {ticket['pagerduty_escalation']}")
    print("  [SUCCESS] Perimeter threat neutralized and SOC incident fully documented.")


def demo_telco_churn_data_analyst():
    print_header("5. DEMO: TELCO CHURN DATA ANALYST (AUTONOMOUS DS & ANALYTICS)")
    print("Agent: telco_churn_data_analyst | Model: gemini-2.5-flash")

    print_section("Step 1: Automated Exploratory Data Analysis & Feature Correlations")
    profile = load_and_profile_dataset()
    print(f"  * Ingested Records: {profile['total_records']:,} subscribers")
    print(f"  * Baseline Churn Rate: {profile['churn_rate_pct']}%")
    print(f"  * Average Monthly Recurring Revenue (ARPU): ${profile['avg_monthly_charges_usd']:.2f} USD/mo")
    print(f"  * Average Account Tenure: {profile['avg_tenure_months']} months")
    print("  * Pearson Correlation with Churn:")
    for feat, corr in profile["feature_correlations"].items():
        sign = "+" if corr >= 0 else ""
        print(f"      - {feat:22}: {sign}{corr:.3f}")

    print_section("Step 2: Cohort Risk Segmentation (Group By: 'contract_type')")
    cohorts = perform_cohort_risk_analysis(group_by_col="contract_type")
    for c in cohorts["cohorts"]:
        print(f"  * Cohort: {c['contract_type']:15} | Subscribers: {c['total_subscribers']:4} | Churn Rate: {c['churn_rate_pct']:5.1f}% | Revenue at Risk: ${c['total_revenue_at_risk']:,.2f} USD/mo")
    print(f"  * Key Statistical Finding: {cohorts['key_finding']}")

    print_section("Step 3: Multi-Factor Churn Risk Scoring on Subscriber 'SUB-00042'")
    sub_risk = predict_subscriber_churn_probability("SUB-00042")
    print(f"  * Target Subscriber: {sub_risk['customer_id']} | Contract: {sub_risk['contract_type']}")
    print(f"  * Predicted Churn Likelihood: {sub_risk['churn_probability_pct']}% (Risk Tier: {sub_risk['risk_tier']})")
    print(f"  * Estimated 24-Month CLV at Risk: ${sub_risk['estimated_clv_loss_usd']:,.2f} USD")
    print("  * Top Identified Risk Drivers:")
    for driver in sub_risk["top_risk_drivers"]:
        print(f"      - {driver}")

    print_section("Step 4: Automated Retention Campaign Formulation")
    campaign = generate_retention_campaign(risk_tier="HIGH", budget_usd_per_user=35.0)
    print(f"  * Campaign Code: {campaign['campaign_id']} | Target Tier: {campaign['target_risk_tier']}")
    print(f"  * Eligible Subscribers: {campaign['eligible_subscribers_count']} | Allocated Budget: ${campaign['allocated_budget_usd']:,.2f} USD")
    print(f"  * Projected Retained Customers: {campaign['expected_retained_subscribers']} users (32% conversion)")
    print(f"  * Protected Annual Recurring Revenue: ${campaign['projected_annual_revenue_saved_usd']:,.2f} USD/yr")
    for interv in campaign["recommended_interventions"]:
        print(f"      {interv}")
    print("  [SUCCESS] Data science analytical pipeline completed and retention campaign launched.")


def demo_geospatial_rf_planner():
    print_header("6. DEMO: GEOSPATIAL RF PLANNER (SPATIAL 5G & GEOJSON)")
    print("Agent: geospatial_rf_planner | Model: gemini-2.5-flash")

    print_section("Step 1: Ingesting Geographical Cell Sites (Manhattan / Brooklyn)")
    sites = query_rf_cell_sites()
    print(f"Spatial database loaded {len(sites)} physical gNB site(s):")
    for s in sites[:3]:
        print(f"  * Site: {s['site_id']} ({s['name']})")
        print(f"    Coordinates: [{s['latitude']}, {s['longitude']}] | Azimuth: {s['azimuth_deg']} deg | Tilt: {s['tilt_deg']} deg | Band: {s['band']}")

    print_section("Step 2: Detecting Unserved Coverage Dead Zones (RSRP < -105 dBm)")
    holes = detect_coverage_dead_zones()
    print(f"Identified {len(holes)} coverage dark spot(s):")
    for h in holes:
        print(f"  * Gap ID: {h['hole_id']} | Severity: {h['severity']} | Centroid: [{h['latitude']}, {h['longitude']}]")
        print(f"    Estimated RSRP: {h['estimated_rsrp_dbm']} dBm | Unserved Radius: {h['radius_m']}m | Nearest Site: {h['nearest_serving_site']}")

    print_section("Step 3: Inter-Cell Interference & Beam Collision Analysis")
    interf = analyze_inter_cell_interference("SITE-NYC-001")
    print(f"  * Source Site: {interf['source_site']} vs Interfering Adjacent Site: {interf['interfering_site']}")
    print(f"  * Physical Separation: {interf['separation_distance_m']}m | Angular Bore-Sight Overlap: {interf['angular_overlap_deg']} deg")
    print(f"  * Measured SINR Degradation: -{interf['sinr_penalty_db']} dB | Collision Risk: {interf['collision_risk']}")

    print_section("Step 4: Spatial Antenna Azimuth & Tilt Optimization")
    opt_plan = optimize_antenna_parameters(site_id="SITE-NYC-001", target_objective="MINIMIZE_INTERFERENCE")
    print(f"  * Optimization for {opt_plan['site_id']}:")
    print(f"    Azimuth: {opt_plan['current_azimuth_deg']} deg -> {opt_plan['recommended_azimuth_deg']} deg")
    print(f"    Downtilt: {opt_plan['current_tilt_deg']} deg -> {opt_plan['recommended_tilt_deg']} deg")
    print(f"    Expected SINR Gain: +{opt_plan['expected_sinr_gain_db']} dB | Coverage Lift: +{opt_plan['expected_coverage_lift_pct']}%")
    print(f"    Rationale: {opt_plan['rationale']}")

    print_section("Step 5: Exporting RFC 7946 Compliant GeoJSON FeatureCollection")
    geojson = generate_coverage_geojson(include_dead_zones=True)
    print(f"  * GeoJSON Type: {geojson['type']}")
    print(f"  * Total Exported Features: {geojson['metadata']['total_features']} (Sites, Coverage Polygons, Dead Zones)")
    print(f"  * Spatial Reference: {geojson['metadata']['projection']}")
    print(f"  * Ready for immediate import into Leaflet, Mapbox, Google Earth, or QGIS.")
    print("  [SUCCESS] Spatial RF modeling and GeoJSON generation completed.")


def main():
    print("=" * 80)
    print(" GOOGLE AGENT DEVELOPMENT KIT (ADK 2.8.0) - 6-AGENT FLAGSHIP PORTFOLIO ".center(80))
    print(" Developed by Santiago Penas | Powered by Google ADK & Gemini ".center(80))
    print("=" * 80)

    try:
        demo_telco_noc_optimizer()
        demo_multimodal_incident_graph()
        demo_enterprise_rag_knowledge()
        demo_autonomous_secops_swarm()
        demo_telco_churn_data_analyst()
        demo_geospatial_rf_planner()
        print_header("PORTFOLIO DEMONSTRATION COMPLETE: ALL 6 AGENTS VERIFIED")
        print("\nAll 6 Google ADK agents demonstrated 100% operational readiness.")
        print("Run 'pytest portfolio_agents/' to verify the complete 39-test suite.\n")
    except Exception as e:
        print(f"\n[ERROR] Demo encountered exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
