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


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
