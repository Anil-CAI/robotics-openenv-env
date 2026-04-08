---
title: Robotics OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Robotics Navigation Environment (OpenEnv)

## Overview
This project simulates a real-world robotics navigation task where an agent must reach a goal while avoiding obstacles. It is designed to be compatible with the OpenEnv standard for AI environment development.

## Real-World Applications
This environment simulates real-world robotic navigation problems such as warehouse automation, autonomous delivery robots, and path planning in dynamic environments. It can be used to train and evaluate AI agents for obstacle avoidance and efficient route optimization tasks.

## Features
- **OpenEnv Compliant API**: Supports `step`, `reset`, and `state` endpoints.
- **Difficulty Levels**: 
    - **Easy**: 0 obstacles.
    - **Medium**: 3 obstacles.
    - **Hard**: 6 obstacles.
- **Reward-based Learning System**: Dense rewards for distance and sparse rewards for goal completion.
- **Baseline Agent**: `inference.py` provides an A* or heuristic navigation example.
- **Deterministic Graders**: `grader.py` evaluates performance based on task difficulty.

## Tasks
- **Easy**: Reach goal without obstacles.
- **Medium**: Reach goal with moderate obstacles.
- **Hard**: Reach goal with dense obstacles and safety penalties.

## Reward System
- `+1.0`: Reaching the goal.
- `+0.1`: Moving closer to the goal.
- `-0.01`: Per step penalty.
- `-0.3`: For collisions with obstacles or boundaries.

## Running Locally

### 1. Start the Server
From the project root:
```bash
python3 -m server.app
```

### 2. Run the Baseline Agent
```bash
python3 inference.py
```

## API Endpoints
- `POST /reset`: Reset environment with a specific difficulty.
- `POST /step`: Execute an action (`up`, `down`, `left`, `right`).
- `GET /state`: Retrieve current environment state.

## Requirements
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- Requests

## Baseline Performance Results
- **Easy**: ~1.0
- **Medium**: ~0.8–0.9
- **Hard**: ~0.6–0.8
