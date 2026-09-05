"""Data Science and Churn Analytics tools for Telco Churn Data Analyst."""

import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
from google.adk.tools import ToolContext
from .models import (
    StatisticalSummary,
    CohortRiskAnalysis,
    SubscriberRiskProfile,
    RetentionCampaign,
    RiskTier,
)

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "subscriber_churn_data.csv"
_DATAFRAME_CACHE: Optional[pd.DataFrame] = None


def _get_dataframe(file_path: Optional[str] = None) -> pd.DataFrame:
    """Loads and caches subscriber dataset."""
    global _DATAFRAME_CACHE
    path = Path(file_path) if file_path else DEFAULT_DATA_PATH
    if _DATAFRAME_CACHE is None or file_path is not None:
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found at {path}")
        _DATAFRAME_CACHE = pd.read_csv(path)
    return _DATAFRAME_CACHE


def load_and_profile_dataset(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Loads telecom subscriber usage dataset and computes exploratory data analysis (EDA) and statistical correlations.

    Args:
        file_path: Optional path to a CSV dataset. If omitted, uses the default telecom subscriber repository.

    Returns:
        Structured StatisticalSummary containing record counts, baseline churn rate, ARPU, and Pearson correlation coefficients.
    """
    df = _get_dataframe(file_path)

    total_records = int(len(df))
    churn_rate = round(float(df["churned"].mean() * 100), 2)
    avg_arpu = round(float(df["monthly_charges_usd"].mean()), 2)
    avg_tenure = round(float(df["tenure_months"].mean()), 1)

    # Compute correlation matrix with churn
    numeric_cols = [
        "tenure_months",
        "monthly_charges_usd",
        "tech_support_calls",
        "avg_data_usage_gb",
        "packet_loss_pct",
        "dropped_call_rate",
        "device_5g_enabled",
    ]
    correlations = {}
    for col in numeric_cols:
        if col in df.columns:
            corr_val = float(df[col].corr(df["churned"]))
            correlations[col] = round(corr_val, 3)

    summary = StatisticalSummary(
        total_records=total_records,
        churn_rate_pct=churn_rate,
        avg_monthly_charges_usd=avg_arpu,
        avg_tenure_months=avg_tenure,
        feature_correlations=correlations,
        missing_values_count=int(df.isna().sum().sum()),
    )
    return summary.model_dump()


def perform_cohort_risk_analysis(
    group_by_col: str = "contract_type",
    metric_col: str = "monthly_charges_usd",
) -> Dict[str, Any]:
    """Performs categorical cohort segmentation to identify customer segments with disproportionate churn and revenue risk.

    Args:
        group_by_col: Categorical column to segment by ('contract_type', 'device_5g_enabled', 'tech_support_calls').
        metric_col: Numeric metric to aggregate (default: 'monthly_charges_usd').

    Returns:
        Structured CohortRiskAnalysis with cohort sizes, churn percentages, and key statistical findings.
    """
    df = _get_dataframe()

    if group_by_col not in df.columns:
        return {"error": f"Column '{group_by_col}' not found. Available: {list(df.columns)}"}

    grouped = (
        df.groupby(group_by_col)
        .agg(
            total_subscribers=("customer_id", "count"),
            churned_subscribers=("churned", "sum"),
            churn_rate_pct=("churned", lambda x: round(float(x.mean() * 100), 2)),
            avg_metric=(metric_col, lambda x: round(float(x.mean()), 2)),
            total_revenue_at_risk=(
                metric_col,
                lambda x: round(float(x[df.loc[x.index, "churned"] == 1].sum()), 2),
            ),
        )
        .reset_index()
    )

    cohorts = grouped.to_dict(orient="records")
    highest_risk = max(cohorts, key=lambda c: c["churn_rate_pct"])

    finding = (
        f"Subscribers in the '{highest_risk[group_by_col]}' cohort exhibit the highest churn rate at "
        f"{highest_risk['churn_rate_pct']}% with ${highest_risk['total_revenue_at_risk']:,.2f} USD in monthly revenue at risk."
    )

    analysis = CohortRiskAnalysis(
        grouping_feature=group_by_col,
        cohorts=cohorts,
        highest_risk_cohort=str(highest_risk[group_by_col]),
        key_finding=finding,
    )
    return analysis.model_dump()


def predict_subscriber_churn_probability(customer_id: str) -> Dict[str, Any]:
    """Calculates multi-factor churn probability and isolates top risk drivers for a specific subscriber.

    Args:
        customer_id: Unique subscriber account ID (e.g., 'SUB-00042').

    Returns:
        Structured SubscriberRiskProfile with probability percentage, risk tier, drivers, and CLV at risk.
    """
    df = _get_dataframe()
    match = df[df["customer_id"] == customer_id]

    if match.empty:
        # Fallback to random sample if specific ID not found
        row = df.sample(1).iloc[0]
        customer_id = str(row["customer_id"])
    else:
        row = match.iloc[0]

    # Calculate risk score based on multi-factor modeling
    score = 0.15
    drivers = []

    if str(row["contract_type"]) == "Month-to-Month":
        score += 0.30
        drivers.append("Contractual: Month-to-Month commitment lacks long-term retention lock-in.")

    if float(row["tech_support_calls"]) >= 3:
        score += 0.25
        drivers.append(f"Customer Service: Elevated friction with {row['tech_support_calls']} tech support calls.")

    if float(row["dropped_call_rate"]) > 2.0:
        score += 0.20
        drivers.append(f"QoS Impairment: High call drop rate ({row['dropped_call_rate']}%) breaching SLA.")

    if int(row["tenure_months"]) < 6:
        score += 0.15
        drivers.append("Tenure Vulnerability: Early lifecycle subscriber (< 6 months tenure).")

    if float(row["monthly_charges_usd"]) > 85.0:
        score += 0.10
        drivers.append(f"Price Sensitivity: High monthly fee (${row['monthly_charges_usd']:.2f} USD/mo).")

    prob = min(96.0, max(5.0, round(score * 100, 1)))

    tier = RiskTier.CRITICAL if prob >= 75.0 else (
        RiskTier.HIGH if prob >= 50.0 else (
            RiskTier.MEDIUM if prob >= 30.0 else RiskTier.LOW
        )
    )

    # Customer Lifetime Value estimation (24-month horizon)
    clv_loss = round(float(row["monthly_charges_usd"]) * 24.0 * (prob / 100.0), 2)

    profile = SubscriberRiskProfile(
        customer_id=customer_id,
        tenure_months=int(row["tenure_months"]),
        monthly_charges_usd=float(row["monthly_charges_usd"]),
        contract_type=str(row["contract_type"]),
        churn_probability_pct=prob,
        risk_tier=tier,
        top_risk_drivers=drivers or ["Standard baseline subscriber profile."],
        estimated_clv_loss_usd=clv_loss,
    )
    return profile.model_dump()


def generate_retention_campaign(
    risk_tier: str = "HIGH",
    budget_usd_per_user: float = 35.0,
    ctx: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Designs an automated, targeted customer retention campaign for at-risk subscriber cohorts.

    Args:
        risk_tier: Target risk segment ('CRITICAL', 'HIGH', 'MEDIUM').
        budget_usd_per_user: Allocated promotional/retention spend per eligible customer in USD.
        ctx: Runtime ToolContext injected by Google ADK to track campaign history in session state.

    Returns:
        Structured RetentionCampaign with projected conversion lift and annualized recurring revenue protected.
    """
    df = _get_dataframe()
    tier_upper = risk_tier.upper()

    # Filter eligible users
    if tier_upper == "CRITICAL":
        eligible = df[(df["contract_type"] == "Month-to-Month") & (df["tech_support_calls"] >= 3)]
    elif tier_upper == "HIGH":
        eligible = df[(df["contract_type"] == "Month-to-Month") | (df["dropped_call_rate"] > 2.0)]
    else:
        eligible = df[df["tenure_months"] < 12]

    count = max(1, len(eligible))
    total_budget = round(count * budget_usd_per_user, 2)

    # Expected conversion lift (estimated 32% retention rate on targeted interventions)
    conversion_rate = 0.32
    retained_users = int(count * conversion_rate)
    avg_monthly = float(eligible["monthly_charges_usd"].mean()) if not eligible.empty else 75.0
    annual_saved = round(retained_users * avg_monthly * 12.0, 2)

    interventions = [
        f"1. Priority Tech Support: Assign dedicated tier-2 concierge routing for {tier_upper} subscribers.",
        f"2. Incentive Offer: Deliver 15% discount for migrating from Month-to-Month to a 12-month contract.",
        "3. Network Quality Guarantee: Complimentary 5G Unlimited Ultra Data speed boost for 6 months.",
    ]

    campaign_id = f"RET-CAMP-{datetime.now(timezone.utc).strftime('%YQ1-%H%M%S')}"

    campaign = RetentionCampaign(
        campaign_id=campaign_id,
        target_risk_tier=RiskTier(tier_upper) if tier_upper in RiskTier.__members__ else RiskTier.HIGH,
        eligible_subscribers_count=count,
        allocated_budget_usd=total_budget,
        recommended_interventions=interventions,
        expected_retained_subscribers=retained_users,
        projected_annual_revenue_saved_usd=annual_saved,
    )

    if ctx and hasattr(ctx, "state") and ctx.state is not None:
        campaigns = ctx.state.get("retention_campaigns", [])
        campaigns.append(campaign.model_dump())
        ctx.state["retention_campaigns"] = campaigns

    return campaign.model_dump()
