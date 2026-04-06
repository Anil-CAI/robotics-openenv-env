import argparse
import uvicorn
from fastapi import FastAPI
from typing import Optional

from robotics_env.server.robotics_env_environment import RoboticsEnvironment
from robotics_env.models import Action

app = FastAPI()
env = RoboticsEnvironment()

@app.post("/reset")
def reset(data: dict = {}):
    difficulty = data.get("difficulty", "medium")
    goal = data.get("goal")
    obs = env.reset(difficulty=difficulty, goal=tuple(goal) if goal else None)
    
    return {
        "observation": obs.model_dump(),
        "reward": obs.reward,
        "done": obs.done
    }

@app.post("/step")
def step(action: Action):
    # Pass the full Action model as expected by the environment
    obs = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": obs.reward,
        "done": obs.done
    }

@app.get("/state")
def state():
    obs = env.state()
    return obs.model_dump()

def main(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(port=args.port)
