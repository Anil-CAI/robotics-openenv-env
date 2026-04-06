from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    position: List[int]
    goal: List[int]
    obstacles: List[List[int]]
    grid_size: int
    score: Optional[float] = 0.0
    reward: float = 0.0
    done: bool = False

class Action(BaseModel):
    action: str  # "up", "down", "left", "right"

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
