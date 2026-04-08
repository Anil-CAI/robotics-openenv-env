# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Robotics Env Environment Implementation.

A simple test environment that echoes back messages sent to it.
Perfect for testing HTTP server infrastructure.
"""

import random
from uuid import uuid4
from typing import List, Tuple

from robotics_env.models import Observation, Action


class RoboticsEnvironment:
    """
    A simple echo environment that echoes back messages.

    This environment is designed for testing the HTTP server infrastructure.
    It maintains minimal state and simply echoes back whatever message it receives.

    Example:
        >>> env = RoboticsEnvironment()
        >>> obs = env.reset()
        >>> print(obs.echoed_message)  # "Robotics Env environment ready!"
        >>>
        >>> obs = env.step(RoboticsAction(message="Hello"))
        >>> print(obs.echoed_message)  # "Hello"
        >>> print(obs.message_length)  # 5
    """

    # Enable concurrent WebSocket sessions.
    # Set to True if your environment isolates state between instances.
    # When True, multiple WebSocket clients can connect simultaneously, each
    # getting their own environment instance (when using factory mode in app.py).
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the robotics_env environment."""
        self._reset_count = 0
        self.grid_size = 6
        self.position = (0, 0)
        self.goal = (5, 5)
        self.obstacles = []
        self.object_position = None
        self.has_object = False
        self.max_steps = 30
        self.current_step = 0
        self.collisions = 0

    def state(self):
        """Required by OpenEnv."""
        return self._get_obs()

    def _get_obs(self) -> Observation:
        """Helper to create an Observation object from current state."""
        score = 0.0
        done = False

        if hasattr(self, "position") and hasattr(self, "goal"):
             if tuple(self.position) == tuple(self.goal):
                 score += 1.0
                 done = True
             if hasattr(self, "collisions"):
                 score -= self.collisions * 0.1
             if hasattr(self, "current_step") and hasattr(self, "max_steps"):
                 score -= (self.current_step / self.max_steps) * 0.5
                 if self.current_step >= self.max_steps:
                     done = True

        return Observation(
            position=list(self.position),
            goal=list(self.goal),
            obstacles=[list(o) for o in self.obstacles],
            grid_size=self.grid_size,
            score=score,
            reward=score,
            done=done
        )

    def reset(self, difficulty="medium", goal: tuple = None) -> Observation:
        """
        Reset the environment with a specific difficulty.
        Difficulty levels: easy (0 obstacles), medium (3 obstacles), hard (6 obstacles).
        """
        self._reset_count += 1
        self.grid_size = 6
        self.position = (0, 0)

        # Difficulty logic
        if difficulty == "easy":
            num_obstacles = 0
        elif difficulty == "medium":
            num_obstacles = 3
        elif difficulty == "hard":
            num_obstacles = 6
        else:
            num_obstacles = 3

        # Generate custom or random goal
        if goal:
            self.goal = goal
        else:
            while True:
                self.goal = (random.randint(0, 5), random.randint(0, 5))
                if self.goal != self.position:
                    break

        # Generate obstacles
        self.obstacles = []
        while len(self.obstacles) < num_obstacles:
            obs = (random.randint(0, 5), random.randint(0, 5))
            if obs != self.position and obs != self.goal and obs not in self.obstacles:
                self.obstacles.append(obs)

        # Task variables
        self.current_step = 0
        self.collisions = 0
        
        self.render()
        return self._get_obs()

    def step(self, action: Action) -> Observation:
        """
        Execute a step in the environment with movement and reward logic.
        """
        if not hasattr(self, "position"):
            self.reset()
        self.current_step += 1
        x, y = self.position
        new_x, new_y = x, y

        # Movement logic
        if action.action == "up":
            new_y -= 1
        elif action.action == "down":
            new_y += 1
        elif action.action == "left":
            new_x -= 1
        elif action.action == "right":
            new_x += 1

        reward = -0.01  # step penalty

        # Check bounds
        if not (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size):
            new_x, new_y = x, y
            reward -= 0.3
            self.collisions += 1

        # Check obstacle
        elif (new_x, new_y) in self.obstacles:
            new_x, new_y = x, y
            reward -= 0.3
            self.collisions += 1

        else:
            # Distance reward
            old_dist = abs(x - self.goal[0]) + abs(y - self.goal[1])
            new_dist = abs(new_x - self.goal[0]) + abs(new_y - self.goal[1])
            if new_dist < old_dist:
                reward += 0.1

        self.position = (new_x, new_y)

        done = False

        # Check goal
        print("CHECK:", self.position, self.goal)
        if tuple(self.position) == tuple(self.goal):
            reward += 1.0
            done = True

        if self.current_step >= self.max_steps:
            done = True

        self.render()

        obs = self._get_obs()
        obs.reward = reward
        obs.done = done

        return obs

    def render(self):
        """Render the environment grid to the console."""
        grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Place obstacles
        for (x, y) in self.obstacles:
            grid[y][x] = "X"

        # Place goal
        gx, gy = self.goal
        grid[gy][gx] = "G"

        # Place robot
        rx, ry = self.position
        grid[ry][rx] = "R"

        print(f"\nStep: {self.current_step}/{self.max_steps}")
        print(f"Collisions: {self.collisions}")
        print("GRID:")
        for row in grid:
            print(" ".join(row))
        print()
