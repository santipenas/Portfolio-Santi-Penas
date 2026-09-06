# 🌿 Autonomous Green Base Station Energy-Saving RL Controller (O-RAN rApp)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Gymnasium](https://img.shields.io/badge/Gymnasium-1.0.0-green.svg)](https://gymnasium.farama.org/)
[![Stable-Baselines3](https://img.shields.io/badge/Stable--Baselines3-2.5.0-orange.svg)](https://stable-baselines3.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io/)
[![UV](https://img.shields.io/badge/uv-fast%20packaging-purple.svg)](https://docs.astral.sh/uv/)

An end-to-end, production-grade **Reinforcement Learning (RL)** project designed for the telecommunications industry. This repository implements, trains, and deploys an autonomous **O-RAN (Open Radio Access Network) Non-RT/Near-RT RIC rApp** agent that dynamically schedules 5G base station power sleep states (*Active*, *Shallow Sleep*, *Deep Sleep*) to cut cellular network electricity consumption and OPEX while strictly maintaining Quality of Service (QoS) and Service Level Agreement (SLA) compliance.

---

## 📑 Table of Contents
1. [Executive Summary & Problem Statement](#-1-executive-summary--problem-statement)
2. [Telecom 101: Understanding Cellular Power Consumption](#-2-telecom-101-understanding-cellular-power-consumption)
3. [The Dataset & Physical Topology](#-3-the-dataset--physical-topology)
4. [Reinforcement Learning Explained (For Non-RL Specialists)](#-4-reinforcement-learning-explained-for-non-rl-specialists)
5. [MDP Formulation: State, Action, and Reward Shaping](#-5-mdp-formulation-state-action-and-reward-shaping)
6. [Why PPO? (Proximal Policy Optimization)](#-6-why-ppo-proximal-policy-optimization)
7. [How the Training Pipeline Works](#-7-how-the-training-pipeline-works)
8. [Benchmark Comparisons & Financial Impact](#-8-benchmark-comparisons--financial-impact)
9. [Project Architecture & Directory Layout](#-9-project-architecture--directory-layout)
10. [Quick-Start Guide (Installation & Execution)](#-10-quick-start-guide-installation--execution)

---

## 🎯 1. Executive Summary & Problem Statement

### The Problem
* **Massive Energy Footprint**: Telecommunication networks consume over **130 TWh of electricity globally per year**, producing millions of tons of CO2.
* **The Culprit (RAN)**: Between **70% and 80%** of a mobile operator's total electrical power is consumed directly by the **Radio Access Network (RAN)**—the cell towers, antennas, and base stations transmitting radio signals to our phones.
* **Legacy "Always-On" Waste**: Traditional cell towers operate at **100% full transmission power 24/7/365**, regardless of whether 2,000 people are streaming video at 2:00 PM or the street is completely empty at 4:00 AM.
* **Why Static Timers Fail**: Telecom operators historically attempted crude heuristic rules, like scheduling sleep strictly between 01:00 and 05:00. However, whenever unexpected night events occur (e.g., late-night concerts, traffic diversions, sports celebrations), static timers cause severe network congestion, call drops, and contractual SLA penalties.

### The Autonomous RL Solution
This project deploys an autonomous **AI Controller (rApp)** that runs on the O-RAN RAN Intelligent Controller (RIC). It monitors traffic demand, active user sessions, radio channel conditions, and neighboring cell capacities every hour. It makes sub-second, intelligent decisions:
1. Keeps antennas in **Full Active Power** during high or unpredictable demand.
2. Switches components into **Shallow Sleep** when traffic subsides.
3. Safely triggers **Deep Sleep** during low-demand windows, automatically offloading active mobile connections to overlapping neighboring sectors without dropping a single call.

---

## 📡 2. Telecom 101: Understanding Cellular Power Consumption

To understand this project without a telecom engineering background, here are the essential hardware concepts:

```
                            [ Macro Cell Site Tower ]
                                 /      |      \
                         Sector 1    Sector 2   Sector 3
                        (Azimuth 0°) (Azimuth 120°) (Azimuth 240°)
```

### The 3 Power States
Each 5G Macro Cell Transceiver operates across 3 standardized energy states modeled in this project:

| Power State | Power Draw | Operational Description | Traffic Handling |
|---|---|---|---|
| **0: Active** | **1,000 W** | All Power Amplifiers (PA) and Radio Frequency (RF) chains fully energized. | 100% capacity. Zero degradation risk. |
| **1: Shallow Sleep** | **500 W** (50% saved) | Power Amplifiers turn off between micro-bursts; digital baseband remains on. | Handles up to 60% of peak traffic without dropping connections. |
| **2: Deep Sleep** | **100 W** (90% saved) | Complete RF shutdown; standby listening mode only. | Offloads 100% of user traffic to overlapping neighboring antennas. |

### Inter-Sector Traffic Offloading (Handover)
Cell towers have multiple directional antennas (sectors), usually pointing in 3 directions (e.g., 0°, 120°, 240°). Their coverage footprints physically overlap. When one sector enters **Deep Sleep**, users under its coverage are transferred (via 3GPP handover) to overlapping co-sited or adjacent sectors. If the neighbor has enough "headroom" (spare capacity), the users notice zero degradation.

---

## 📊 3. The Dataset & Physical Topology

The project simulates realistic 5G cellular conditions using two rich datasets located in [`data/`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/data):

### 1. Cellular BS Topology (`cellular_bs_topology.csv`)
Contains physical engineering specifications for 84 cell sectors across multiple tower sites:
* **Coordinates**: `distanceX`, `distanceY` in meters.
* **Antenna Specifications**: `Azimuth` (heading in degrees), `AntennaHeight` (meters), `GroundHeight`, `HBeamwidth` (horizontal beamwidth, ~63°).
* **Radio Parameters**: `Band` (e.g., 2.1 GHz / 3.5 GHz), `dlBandwidth`, `PCI` (Physical Cell ID), `DuplexMode`.
* **Topology Graph**: Used by [`src/env/topology_graph.py`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/src/env/topology_graph.py) to calculate exact angular overlaps and inter-site neighbor distances for traffic offloading.

### 2. Hourly Traffic KPIs (`cellular_bs_traffic_kpi_train.csv` & `_test.csv`)
Split into **Training (Days 1–25)** and **Unseen Testing (Days 25–31)**:
* `ThpVolDl` / `ThpVolUl`: Downlink and uplink throughput volumes (MB).
* `RRC.ConnMax` / `RRC.ConnEstabAtt`: Active Radio Resource Control connected users (connected smartphones).
* `CARR.WBCQIDist.Bin0` to `Bin15`: Wideband Channel Quality Indicator (CQI) histogram bins (signal-to-interference radio quality).
* `MM.HoExeIntraFreqSuccOut` & `MM.HoExeInterFreq...`: Inter-cell handover execution statistics.

---

## 🧠 4. Reinforcement Learning Explained (For Non-RL Specialists)

If you are new to Reinforcement Learning (RL), think of it not as pattern recognition (like supervised learning), but as **learning through trial, error, and incentives**:

```
                       +-----------------------------+
                       |          RL Agent           |
                       |       (AI Decision Maker)   |
                       +-----------------------------+
                          ▲                       │
           Observation /  │                       │ Action
             State (s)    │                       │  (a)
                          │                       ▼
                       +-----------------------------+
                       |    Cellular Environment     |
                       |      (Base Station Sim)     |
                       +-----------------------------+
                                      │
                               Reward | (r)
                                      ▼
```

1. **Agent**: The AI brain deciding whether to sleep or stay active.
2. **Environment**: The simulated cell tower with fluctuating user traffic.
3. **State ($s_t$)**: What the tower looks like right now (current traffic, active users, time of day, neighbor capacity).
4. **Action ($a_t$)**: The choice made by the agent (*Active*, *Shallow Sleep*, or *Deep Sleep*).
5. **Reward ($r_t$)**: A mathematical score giving positive points for saving electricity, and severe penalties for dropping calls or violating customer SLAs.

Over thousands of simulated hours, the agent learns a **Policy ($\pi$)**—a strategy that maximizes accumulated rewards over time.

---

## ⚙️ 5. MDP Formulation: State, Action, and Reward Shaping

This problem is formalized as a **Markov Decision Process (MDP)** in [`src/env/base_station_env.py`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/src/env/base_station_env.py):

### Observation Space (7 Continuous Features)
All normalized between `[0.0, 1.0]` (or `[-1.0, 1.0]` for cyclic terms):
1. **$s_0$ (Normalized DL Volume)**: Downlink traffic demand ratio.
2. **$s_1$ (Normalized UL Volume)**: Uplink traffic demand ratio.
3. **$s_2$ (Normalized Active RRC Users)**: Number of active mobile connections.
4. **$s_3$ (Weighted Channel Quality - CQI)**: Aggregated 16-bin radio signal quality.
5. **$s_4$ (Cyclic Hour $\sin$)**: $\sin(2\pi \cdot \text{hour}/24)$ to model seamless daily cycles.
6. **$s_5$ (Cyclic Hour $\cos$)**: $\cos(2\pi \cdot \text{hour}/24)$ to prevent midnight boundary jumps.
7. **$s_6$ (Neighbor Headroom Ratio)**: Spare capacity available in neighboring sectors to absorb handovers.

### Action Space (3 Discrete Choices)
* `0`: **Active** (1000 W)
* `1`: **Shallow Sleep** (500 W)
* `2`: **Deep Sleep** (100 W)

### Reward Function
The reward formula balances energy conservation with telecommunications service reliability:

$$\text{Reward} = \underbrace{2.0 \times \left(\frac{P_{\text{saved}}}{1000}\right)}_{\text{Energy Conservation Incentive}} - \underbrace{2.5 \times \text{QoS Penalty}}_{\text{Throughput Deficit}} - \underbrace{25.0 \times \left(\frac{\text{Dropped Users}}{\text{Demand Users}}\right)}_{\text{Strict SLA Call Drop Penalty}}$$

* **Why this works**: Saving 900 W in Deep Sleep gives $+1.8$ reward. But if the sector drops even 10% of users because neighbors cannot absorb them, the penalty is $-2.5$, making reckless sleep unprofitable for the agent.

---

## 🔬 6. Why PPO? (Proximal Policy Optimization)

We chose **PPO** (Schulman et al.) via [Stable-Baselines3](https://stable-baselines3.readthedocs.io/):

1. **Stability via Clipped Objective**: In cellular networks, an erratic policy shift can drop hundreds of calls simultaneously. Standard policy gradients (like REINFORCE or standard Actor-Critic) suffer from destructive updates. PPO constrains policy updates within a clipping window $[1-\epsilon, 1+\epsilon]$ (where $\epsilon=0.2$), guaranteeing smooth, monotonic policy improvements.
2. **Sample Efficiency on Continuous States**: PPO excels at tabular/continuous time-series inputs by utilizing an Actor-Critic multi-layer perceptron (MLP) architecture.
3. **Entropy Regularization**: Encourages the agent to safely explore different sleep states during low traffic hours rather than getting stuck in the safe-but-wasteful "Always-On" local minimum.

---

## 🔄 7. How the Training Pipeline Works

The training workflow executed in [`src/models/train_ppo.py`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/src/models/train_ppo.py) proceeds through these stages:

```
[ cellular_bs_traffic_kpi_train.csv ]
                 │
                 ▼
     [ BaseStationEnergyEnv ] <─── [ CellularTopologyGraph ]
                 │
                 ▼
        [ PPO Agent (MLP) ]
         - 2048-step rollouts
         - GAE (gamma=0.99, lambda=0.95)
         - 10 training epochs per batch
                 │
                 ▼
   [ models/ppo_bs_energy_agent.zip ] Checkpoint
```

1. **Environment Instantiation**: Reads the target cell's 25-day training time-series and calculates 99th percentile normalization constants.
2. **Rollout Collection**: Collects trajectories of observations, actions, rewards, and neighbor offload results.
3. **Advantage Estimation**: Generalized Advantage Estimation (GAE) computes whether actions yielded better energy-SLA tradeoffs than average.
4. **Policy & Value Optimization**: Updates policy and value networks using Adam optimizer (`lr=3e-4`).
5. **Checkpoint Persistence**: Saves the trained agent into [`models/ppo_bs_energy_agent.zip`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/models/ppo_bs_energy_agent.zip).

---

## 📈 8. Benchmark Comparisons & Financial Impact

The trained PPO agent is benchmarked on **unseen test data (Days 25–31)** against 3 industry standards:
1. **Always-On Baseline**: Traditional cell operation (100% active).
2. **Static Night Timer**: Sleeps strictly between 01:00 and 06:00.
3. **Dynamic Threshold Rule**: Sleeps when instantaneous downlink volume drops below fixed 15%/40% thresholds.

### Test Set Benchmark Results
*(Evaluated across 148 test hours on unseen data)*

| Metric | Always-On Baseline | Static Night Timer | Dynamic Threshold Rule | 🤖 RL Agent (PPO) |
|---|---|---|---|---|
| **Test Set Energy (kWh)** | 148.0 kWh | 115.6 kWh | 99.4 kWh | **58.4 kWh** |
| **Energy Reduction (%)** | 0.0% | 21.89% | 32.84% | **60.54%** |
| **Test Period OPEX ($)** | $26.64 | $20.81 | $17.89 | **$10.51** |
| **Annualized OPEX / Cell ($)** | ~$1,389.01 | ~$1,085.03 | ~$932.78 | **~$547.99** |
| **Annual Savings / 3-Sector Site ($)** | $0 | ~$911.93 | ~$1,368.68 | **~$2,523.05** |
| **SLA Compliance Rate (%)** | 100.0% | 99.32% | 100.0% | **98.65%** |
| **Total Dropped Connections** | 0 | 1 | 0 | **0** |
| **Test Carbon Footprint (kg CO2)** | 70.30 kg | 54.91 kg | 47.22 kg | **27.74 kg** |

*Assumptions: $0.18/kWh commercial electricity tariff; 0.475 kg CO2/kWh grid carbon intensity factor.*

---

## 📁 9. Project Architecture & Directory Layout

```
telco-bs-energy-saving/
├── data/
│   ├── cellular_bs_topology.csv            # 84 base station sector coordinates, azimuths & heights
│   ├── cellular_bs_traffic_kpi_train.csv   # 25-day hourly KPI training dataset
│   └── cellular_bs_traffic_kpi_test.csv    # 6-day unseen hourly KPI test dataset
├── frontend/
│   └── app.py                              # Interactive Streamlit dashboard with Plotly visuals
├── models/
│   └── ppo_bs_energy_agent.zip             # Trained Stable-Baselines3 PPO checkpoint
├── src/
│   ├── env/
│   │   ├── base_station_env.py             # Custom Gymnasium BaseStationEnergyEnv simulator
│   │   └── topology_graph.py               # Spatial antenna geometry & handover overlap weights
│   ├── models/
│   │   ├── baselines.py                    # Always-On, Static Timer, & Dynamic Threshold policies
│   │   ├── evaluate.py                     # Benchmark evaluation engine producing metrics table
│   │   └── train_ppo.py                    # PPO agent training pipeline
│   └── utils/
│       └── metrics.py                      # Power consumption, OPEX, CO2 & SLA calculation rules
├── pyproject.toml                          # Project dependencies & uv configuration
├── run_app.bat                             # One-click Windows launch script
└── README.md                               # End-to-end documentation
```

---

## 🚀 10. Quick-Start Guide (Installation & Execution)

### 1. Prerequisites
Install **[uv](https://docs.astral.sh/uv/)** (recommended fast Python packaging tool) or standard Python 3.10+.

### 2. Environment Setup
Clone the repository and install all dependencies into an isolated virtual environment:

```bash
# Automatically creates .venv and installs all dependencies
uv sync
```

### 3. Launch the Interactive Dashboard

> [!IMPORTANT]
> **Windows Path Compatibility Note:**
> Always run Streamlit using `uv run python -m streamlit ...` rather than `uv run streamlit ...`. This bypasses Windows trampoline executable path canonicalization issues when parent directories contain spaces.

Run the Streamlit web application:

```bash
uv run python -m streamlit run frontend/app.py
```

*(Alternatively on Windows, double-click [`run_app.bat`](file:///c:/Users/Santiago/Documents/PROGRAMACION/PORTFOLIO/Reinforcement%20Learning/telco-bs-energy-saving/run_app.bat))*

Once launched, open your browser at `http://localhost:8501` to explore:
* **Live Simulation & Telemetry**: Toggle between policies, adjust simulation steps, and observe real-time power vs. SLA curves.
* **Comparative Benchmark & Radar**: Compare energy savings, OPEX, and compliance radar across all 4 policies.
* **Antenna Topology**: Interactive polar radiation diagrams showing antenna sector azimuths and coverage overlap.
* **System Architecture**: Detailed problem formulation and telecom business case.

---

### 4. Retrain the RL Agent (Optional)
To train the PPO model from scratch on any cell sector:

```bash
uv run python src/models/train_ppo.py --timesteps 50000 --cell Cell_1
```

### 5. Run Benchmark Evaluation
To re-run the comparative evaluation across unseen test data and generate benchmark metrics:

```bash
uv run python src/models/evaluate.py
```

---

## 👨‍💻 Author & Contact
Developed as part of the **Telecom AI & Applied Reinforcement Learning Engineering Portfolio**.
* Built with: Gymnasium, Stable-Baselines3, PyTorch, Streamlit, Plotly, and UV.
