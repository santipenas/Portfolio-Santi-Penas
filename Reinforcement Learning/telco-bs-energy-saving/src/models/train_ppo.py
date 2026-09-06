"""
Training Pipeline for Deep Reinforcement Learning Agent using PPO (Stable-Baselines3).
"""
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import os
import argparse
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback

from src.env.base_station_env import BaseStationEnergyEnv


def train(total_timesteps: int = 50000, target_cell: str = "Cell_1", model_save_path: str = "models/ppo_bs_energy_agent"):
    print(f"==================================================")
    print(f"Starting PPO Training for Base Station: {target_cell}")
    print(f"Target Total Timesteps: {total_timesteps:,}")
    print(f"==================================================")
    
    # Initialize environments
    env = BaseStationEnergyEnv(target_cell=target_cell)
    eval_env = BaseStationEnergyEnv(target_cell=target_cell)
    
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    # Configure PPO agent with optimized hyperparameters for tabular/time-series cellular state
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        verbose=1
    )
    
    # Train policy
    model.learn(total_timesteps=total_timesteps)
    
    # Save final model checkpoint
    model.save(model_save_path)
    print(f"\nModel successfully trained and saved to: {model_save_path}.zip")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PPO Agent for Base Station Energy Saving")
    parser.add_argument("--timesteps", type=int, default=30000, help="Total training timesteps")
    parser.add_argument("--cell", type=str, default="Cell_1", help="Target cell identifier")
    args = parser.parse_args()
    
    train(total_timesteps=args.timesteps, target_cell=args.cell)
