"""Pydantic data models for Telco Churn Data Analyst."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ContractType(str, Enum):
    MONTH_TO_MONTH = "Month-to-Month"
    ONE_YEAR = "One-Year"
    TWO_YEAR = "Two-Year"


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class StatisticalSummary(BaseModel):
    total_records: int = Field(..., description="Total number of evaluated subscriber records")
    churn_rate_pct: float = Field(..., description="Overall baseline subscriber churn percentage")
    avg_monthly_charges_usd: float = Field(..., description="Average Monthly Recurring Revenue (ARPU) in USD")
    avg_tenure_months: float = Field(..., description="Average subscriber account tenure in months")
    feature_correlations: Dict[str, float] = Field(
        default_factory=dict,
        description="Pearson correlation coefficient of numerical metrics with churn",
    )
    missing_values_count: int = Field(default=0, description="Total missing or corrupted data points")
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CohortRiskAnalysis(BaseModel):
    grouping_feature: str = Field(..., description="Categorical feature used for cohort segmentation")
    cohorts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Cohort breakdown with subscriber counts, churn rates, and monthly revenue impact",
    )
    highest_risk_cohort: str = Field(..., description="Segment exhibiting the highest churn vulnerability")
    key_finding: str = Field(..., description="Executive statistical takeaway")


class SubscriberRiskProfile(BaseModel):
    customer_id: str = Field(..., description="Unique subscriber ID (e.g., SUB-00042)")
    tenure_months: int = Field(..., description="Tenure duration in months")
    monthly_charges_usd: float = Field(..., description="Current monthly subscription charge")
    contract_type: str = Field(..., description="Active contract commitment")
    churn_probability_pct: float = Field(..., description="Predicted churn likelihood (0% to 100%)")
    risk_tier: RiskTier = Field(..., description="Assigned risk tier (LOW, MEDIUM, HIGH, CRITICAL)")
    top_risk_drivers: List[str] = Field(
        default_factory=list,
        description="Primary behavioral or QoS factors elevating churn risk",
    )
    estimated_clv_loss_usd: float = Field(
        ..., description="Expected Customer Lifetime Value (CLV) lost if subscriber departs"
    )


class RetentionCampaign(BaseModel):
    campaign_id: str = Field(..., description="Unique campaign tracking code (e.g., RET-2026-Q1)")
    target_risk_tier: RiskTier = Field(..., description="Target subscriber risk segment")
    eligible_subscribers_count: int = Field(..., description="Number of subscribers targeted")
    allocated_budget_usd: float = Field(..., description="Total intervention budget in USD")
    recommended_interventions: List[str] = Field(default_factory=list)
    expected_retained_subscribers: int = Field(..., description="Projected retained customers based on conversion lift")
    projected_annual_revenue_saved_usd: float = Field(
        ..., description="Estimated annualized recurring revenue protected in USD"
    )
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
