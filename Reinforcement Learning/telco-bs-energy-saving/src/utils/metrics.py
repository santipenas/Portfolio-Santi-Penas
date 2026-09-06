"""
Telecom Base Station Energy & SLA Metrics Module.
Provides industry-standard power consumption models, OPEX calculations, carbon footprint metrics, and QoS evaluations.
"""

from typing import Dict, Any

# Power consumption values in Watts for a 5G Macro Cell Transceiver
POWER_ACTIVE_WATTS = 1000.0        # Transceiver active at full transmission power
POWER_SHALLOW_SLEEP_WATTS = 500.0  # RF carriers switched off, digital baseband active (50% reduction)
POWER_DEEP_SLEEP_WATTS = 100.0     # Power amplifiers off, deep sleep listening mode (90% reduction)

ELECTRICITY_COST_PER_KWH = 0.18    # Average commercial electricity tariff ($/kWh)
CARBON_EMISSIONS_KG_PER_KWH = 0.475 # Global grid carbon intensity factor (kg CO2 / kWh)


def compute_cell_power(action: int) -> float:
    """Returns power in Watts for a given action: 0=Active, 1=Shallow Sleep, 2=Deep Sleep."""
    if action == 0:
        return POWER_ACTIVE_WATTS
    elif action == 1:
        return POWER_SHALLOW_SLEEP_WATTS
    elif action == 2:
        return POWER_DEEP_SLEEP_WATTS
    raise ValueError(f"Invalid action {action}. Valid values are 0, 1, 2.")


def compute_energy_kwh(power_watts: float, duration_hours: float = 1.0) -> float:
    """Converts Watts over a duration into kWh."""
    return (power_watts * duration_hours) / 1000.0


def compute_financial_opex(energy_kwh: float, rate_per_kwh: float = ELECTRICITY_COST_PER_KWH) -> float:
    """Computes operational expenditure ($)."""
    return energy_kwh * rate_per_kwh


def compute_carbon_footprint(energy_kwh: float, factor: float = CARBON_EMISSIONS_KG_PER_KWH) -> float:
    """Computes carbon footprint in kg CO2."""
    return energy_kwh * factor


def compute_sla_metrics(
    demand_throughput: float,
    delivered_throughput: float,
    active_connections: int,
    dropped_connections: int
) -> Dict[str, float]:
    """Calculates SLA and QoS degradation metrics."""
    throughput_ratio = (delivered_throughput / demand_throughput) if demand_throughput > 0 else 1.0
    throughput_ratio = min(1.0, max(0.0, float(throughput_ratio)))
    
    drop_rate = (dropped_connections / active_connections) if active_connections > 0 else 0.0
    drop_rate = min(1.0, max(0.0, float(drop_rate)))
    
    sla_compliant = (throughput_ratio >= 0.88) and (drop_rate <= 0.02)
    
    return {
        "throughput_satisfaction": throughput_ratio,
        "drop_rate": drop_rate,
        "sla_compliant": 1.0 if sla_compliant else 0.0
    }
