"""Comprehensive unit and integration tests for Telco Churn Data Analyst."""

import pytest
from portfolio_agents.telco_churn_data_analyst.agent import root_agent
from portfolio_agents.telco_churn_data_analyst.tools import (
    load_and_profile_dataset,
    perform_cohort_risk_analysis,
    predict_subscriber_churn_probability,
    generate_retention_campaign,
)


def test_root_agent_configuration():
    assert root_agent.name == "telco_churn_data_analyst"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.tools) == 4
    tool_names = [getattr(t, "__name__", str(t)) for t in root_agent.tools]
    assert "load_and_profile_dataset" in tool_names
    assert "perform_cohort_risk_analysis" in tool_names
    assert "predict_subscriber_churn_probability" in tool_names
    assert "generate_retention_campaign" in tool_names
    assert "churn" in root_agent.description.lower()


def test_load_and_profile_dataset():
    profile = load_and_profile_dataset()
    assert profile["total_records"] >= 1000
    assert 10.0 <= profile["churn_rate_pct"] <= 55.0
    assert profile["avg_monthly_charges_usd"] > 40.0
    assert profile["avg_tenure_months"] > 10.0
    assert "feature_correlations" in profile
    corrs = profile["feature_correlations"]
    assert "tech_support_calls" in corrs
    assert "dropped_call_rate" in corrs


def test_perform_cohort_risk_analysis_contract():
    analysis = perform_cohort_risk_analysis(group_by_col="contract_type")
    assert "error" not in analysis
    assert len(analysis["cohorts"]) >= 3
    assert analysis["highest_risk_cohort"] == "Month-to-Month"
    assert "Month-to-Month" in analysis["key_finding"]


def test_perform_cohort_risk_analysis_invalid():
    res = perform_cohort_risk_analysis(group_by_col="non_existent_column")
    assert "error" in res


def test_predict_subscriber_churn_probability():
    profile = predict_subscriber_churn_probability("SUB-00001")
    assert "churn_probability_pct" in profile
    assert 5.0 <= profile["churn_probability_pct"] <= 96.0
    assert profile["risk_tier"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert len(profile["top_risk_drivers"]) >= 1
    assert profile["estimated_clv_loss_usd"] > 0


def test_generate_retention_campaign():
    campaign = generate_retention_campaign(risk_tier="HIGH", budget_usd_per_user=40.0)
    assert "campaign_id" in campaign
    assert campaign["eligible_subscribers_count"] > 0
    assert campaign["allocated_budget_usd"] > 0
    assert campaign["expected_retained_subscribers"] > 0
    assert campaign["projected_annual_revenue_saved_usd"] > 0
    assert len(campaign["recommended_interventions"]) >= 3
