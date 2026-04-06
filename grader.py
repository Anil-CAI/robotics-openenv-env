def grade_easy(done):
    """Reach goal without any obstacles."""
    return 1.0 if done else 0.0


def grade_medium(done, steps):
    """Reach goal with moderate obstacles. Penalty for excessive steps."""
    if not done:
        return 0.0
    # Higher score for fewer steps (max 30 steps)
    return max(0.0, 1.0 - (steps / 30.0))


def grade_hard(done, steps, collisions):
    """Reach goal with dense obstacles. Heavy penalties for collisions and steps."""
    if not done:
        return 0.0
    # Penalty calculation: efficiency (steps) and safety (collisions)
    penalty = (steps / 30.0) + (collisions * 0.2)
    return max(0.0, 1.0 - penalty)
