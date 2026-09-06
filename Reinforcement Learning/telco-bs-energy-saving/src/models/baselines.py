"""
Baseline Benchmark Policies for Base Station Energy-Saving.
Provides:
  1. AlwaysOnPolicy: Standard telecom baseline (100% active, 0% savings, high OPEX).
  2. StaticTimerPolicy: Conventional nighttime sleep rule (sleeps 01:00 to 06:00).
  3. DynamicThresholdPolicy: Classical rule-based thresholding on traffic load.
"""
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import numpy as np
from typing import Dict, Any


class AlwaysOnPolicy:
    """Baseline policy keeping all transceivers active at 100% power."""
    def predict(self, observation: np.ndarray, deterministic: bool = True) -> int:
        return 0


class StaticTimerPolicy:
    """
    Conventional timer policy:
    Enters deep sleep strictly during nighttime hours (01:00 to 06:00),
    regardless of real-time bursty traffic demand.
    """
    def predict(self, observation: np.ndarray, deterministic: bool = True) -> int:
        # observation[4] is sin(hour), observation[5] is cos(hour)
        sin_h = observation[4]
        cos_h = observation[5]
        angle = np.arctan2(sin_h, cos_h)
        if angle < 0:
            angle += 2 * np.pi
        hour = (angle / (2 * np.pi)) * 24.0
        
        if 1.0 <= hour <= 6.0:
            return 2  # Deep sleep
        return 0      # Active


class DynamicThresholdPolicy:
    """
    Dynamic rule-based policy:
    Sleeps when observed downlink throughput falls below fixed percentage thresholds.
    """
    def __init__(self, low_threshold: float = 0.15, medium_threshold: float = 0.40):
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold

    def predict(self, observation: np.ndarray, deterministic: bool = True) -> int:
        norm_traffic = observation[0]  # Normalized ThpVolDl
        if norm_traffic < self.low_threshold:
            return 2  # Deep sleep
        elif norm_traffic < self.medium_threshold:
            return 1  # Shallow sleep
        return 0      # Active
