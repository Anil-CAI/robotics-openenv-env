import requests
import os
import time
import random

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

visited = set()

def get_action(position, goal, obstacles, grid_size):
    global visited

    x, y = position
    gx, gy = goal

    # 🎯 DIRECT GOAL CHECK (CRITICAL)
    if position == goal:
        return None

    visited.add(position)

    # All possible moves
    moves = {
        "up": (x, y - 1),
        "down": (x, y + 1),
        "left": (x - 1, y),
        "right": (x + 1, y),
    }

    valid_moves = []

    for action, (nx, ny) in moves.items():
        # Check bounds
        if nx < 0 or ny < 0 or nx >= grid_size or ny >= grid_size:
            continue

        # Check obstacles
        if (nx, ny) in obstacles:
            continue
        
        # 🎯 IF THIS MOVE REACHES GOAL → PRIORITY
        if (nx, ny) == goal:
            return action

        # 🚫 avoid visited (KEY FIX)
        if (nx, ny) in visited:
            continue

        # Score based on distance to goal
        distance = abs(nx - gx) + abs(ny - gy)

        valid_moves.append((distance, action))

    # If no valid moves → random fallback
    if not valid_moves:
        return random.choice(list(moves.keys()))

    # Sort → choose best move
    valid_moves.sort()
    return valid_moves[0][1]


def send_step(action):
    """Send a step to the server and return the JSON response."""
    res = requests.post(
        f"{BASE_URL}/step",
        json={"action": action}
    )
    return res.json()


# Detection logic
AUTO_MODE = os.getenv("AUTO_MODE", "1") == "1"

if AUTO_MODE:
    difficulty = "medium"
    mode = "random"
else:
    print("Select difficulty:")
    print("1. Easy\n2. Medium\n3. Hard")
    choice = input("Enter choice: ")

    difficulty = {"1": "easy", "2": "medium", "3": "hard"}.get(choice, "medium")

    print("Choose mode:")
    print("1. Random Goal\n2. Manual Goal")
    mode_choice = input("Enter choice: ")

    mode = "manual" if mode_choice == "2" else "random"

print(f"⚙️ Mode: {difficulty.upper()} | Goal Mode: {mode.upper()}")

# Reset environment
manual_goal = None
if mode == "manual":
    try:
        x = int(input("Enter goal X (0-5): "))
        y = int(input("Enter goal Y (0-5): "))

        if not (0 <= x <= 5 and 0 <= y <= 5):
             print("❌ Invalid goal! Please enter values between 0 and 5.")
             x = int(input("Enter goal X (0-5): "))
             y = int(input("Enter goal Y (0-5): "))

             if not (0 <= x <= 5 and 0 <= y <= 5):
                 print("⚠️ Still invalid. Switching to random goal.")
                 manual_goal = None
             else:
                 manual_goal = [x, y]
        else:
            manual_goal = [x, y]
    except ValueError:
        print("Invalid input, using random goal.")

# Reset call with difficulty and optional goal
res = requests.post(
    f"{BASE_URL}/reset",
    json={
        "difficulty": difficulty,
        "goal": manual_goal
    }
)

data = res.json()
obs = data["observation"]

# 🎯 Check if already at goal (Double Safety)
if obs["position"] == obs["goal"]:
    print("🎯 Already at goal. No movement needed.")
    done = True
else:
    done = False

print("Starting Demo...\n")
print("🎯 Goal:", obs["goal"])
print("🤖 Start:", obs["position"])
print("-" * 20)

visited = set()
steps = 0
max_steps = 30

while not done:
    position = tuple(obs["position"])
    
    goal = obs["goal"]
    obstacles = [tuple(o) for o in obs["obstacles"]]
    grid_size = obs["grid_size"]

    action = get_action(position, goal, obstacles, grid_size)

    if action is None:
        break

    print(f"Action: {action}")
    time.sleep(0.5)

    # 🔥 SEND STEP & CHECK DONE IMMEDIATELY
    data = send_step(action)
    steps += 1
    
    obs = data["observation"]
    done = data["done"]
    score = obs.get("score", 0.0)

    print(f"Action: {action} | Score: {score:.2f}")

    if done:
        if tuple(obs["position"]) == tuple(obs["goal"]):
            print("\n🎯 Goal reached — stopping.")
        else:
            print("⚠️ Goal unreachable within step limit.")
        break

    if steps >= max_steps:
        print("⚠️ Goal unreachable within step limit.")
        break

from grader import grade_easy, grade_medium, grade_hard

if difficulty == "easy":
    final_score = grade_easy(done)
elif difficulty == "medium":
    final_score = grade_medium(done, steps)
else:
    final_score = grade_hard(done, steps, 0)  # collisions optional

print(f"\n🏁 Grader Score: {final_score:.2f}")
print("\nGoal reached or episode ended.")
print(f"Final Score: {obs.get('score', 0.0):.2f}")
