"""
Evaluation & Comparative Benchmarking Module.
Evaluates Trained PPO Agent vs Heuristic Baselines on the Unseen Test Dataset (Days 25–31).
Outputs Energy reduction (%), Cost savings ($), Carbon Abatement, and SLA Compliance.
"""
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any
from stable_baselines3 import PPO

from src.env.base_station_env import BaseStationEnergyEnv
from src.models.baselines import AlwaysOnPolicy, StaticTimerPolicy, DynamicThresholdPolicy


def run_evaluation_episode(env: BaseStationEnergyEnv, policy) -> Dict[str, float]:
    obs, _ = env.reset()
    done = False
    
    total_energy_kwh = 0.0
    total_energy_saved_kwh = 0.0
    total_opex = 0.0
    total_carbon = 0.0
    total_demand_vol = 0.0
    total_delivered_vol = 0.0
    total_dropped_conns = 0
    sla_violations = 0
    steps = 0
    
    actions_count = {0: 0, 1: 0, 2: 0}
    
    while not done:
        # Determine action
        if hasattr(policy, "predict"):
            out = policy.predict(obs, deterministic=True)
            action = out[0] if isinstance(out, tuple) else out
            if isinstance(action, np.ndarray):
                action = int(action.item())
            else:
                action = int(action)
        else:
            action = int(policy(obs))
            
        actions_count[action] = actions_count.get(action, 0) + 1
        
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        total_energy_kwh += info["energy_kwh"]
        total_energy_saved_kwh += info["energy_saved_kwh"]
        total_opex += info["opex_cost"]
        total_carbon += info["carbon_kg"]
        total_demand_vol += info["demand_throughput"]
        total_delivered_vol += info["delivered_throughput"]
        total_dropped_conns += info["dropped_connections"]
        if info["sla_compliant"] < 1.0:
            sla_violations += 1
            
        steps += 1
        
    baseline_energy_kwh = (1000.0 * steps) / 1000.0
    energy_saved_pct = (total_energy_saved_kwh / baseline_energy_kwh * 100.0) if baseline_energy_kwh > 0 else 0.0
    sla_compliance_pct = ((steps - sla_violations) / steps * 100.0) if steps > 0 else 100.0
    
    return {
        "steps": steps,
        "energy_consumed_kwh": round(total_energy_kwh, 2),
        "energy_saved_kwh": round(total_energy_saved_kwh, 2),
        "energy_saved_pct": round(energy_saved_pct, 2),
        "opex_cost_usd": round(total_opex, 2),
        "carbon_kg_co2": round(total_carbon, 2),
        "sla_compliance_pct": round(sla_compliance_pct, 2),
        "total_dropped_conns": int(total_dropped_conns),
        "actions_distribution": actions_count
    }


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    test_file = os.path.join(data_dir, "cellular_bs_traffic_kpi_test.csv")
    model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "ppo_bs_energy_agent.zip")
    
    print("==================================================")
    print("Evaluating Policies on Unseen Test Set (Days 25–31)")
    print("==================================================")
    
    # Initialize Test Environment
    env = BaseStationEnergyEnv(traffic_file=test_file, target_cell="Cell_1")
    
    policies = {
        "Always-On (Baseline)": AlwaysOnPolicy(),
        "Static Night Timer": StaticTimerPolicy(),
        "Dynamic Threshold Rule": DynamicThresholdPolicy(),
    }
    
    # Load trained PPO agent if available
    if os.path.exists(model_path):
        ppo_agent = PPO.load(model_path)
        policies["RL Agent (PPO)"] = ppo_agent
    else:
        print(f"Notice: Trained model {model_path} not found yet. Run train_ppo.py first.")
        
    results = {}
    for name, policy in policies.items():
        res = run_evaluation_episode(env, policy)
        results[name] = res
        print(f"\n--- {name} ---")
        print(f"Energy Consumed: {res['energy_consumed_kwh']} kWh (Saved: {res['energy_saved_pct']}%)")
        print(f"OPEX Cost: ${res['opex_cost_usd']} | Carbon: {res['carbon_kg_co2']} kg CO2")
        print(f"SLA Compliance: {res['sla_compliance_pct']}% | Dropped Connections: {res['total_dropped_conns']}")
        print(f"Action Split (0=Active, 1=Shallow, 2=Deep): {res['actions_distribution']}")
        
    out_file = os.path.join(os.path.dirname(__file__), "..", "..", "models", "evaluation_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nEvaluation results successfully exported to: {out_file}")


if __name__ == "__main__":
    main()
