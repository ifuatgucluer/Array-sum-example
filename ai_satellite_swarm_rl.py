#!/usr/bin/env python3
"""Tiny multi-agent RL demo: satellites learn to keep formation safely."""

import random
from collections import defaultdict

ACTIONS = (-1, 0, 1)  # move left, hold, move right
TARGETS = (-1, 0, 1)


def step(positions, action):
    next_positions = tuple(p + action[i] for i, p in enumerate(positions))
    collision = len(set(next_positions)) < len(next_positions)
    spread = max(next_positions) - min(next_positions)
    reward = -sum(abs(next_positions[i] - TARGETS[i]) for i in range(3))
    reward -= 8 if collision else 0
    return next_positions, reward, spread <= 2


def train(episodes=700, alpha=0.25, gamma=0.9):
    q = defaultdict(float)
    for episode in range(episodes):
        state = (-3, 0, 3)
        epsilon = max(0.04, 1 - episode / episodes)
        for _ in range(25):
            joint = tuple(random.choice(ACTIONS) if random.random() < epsilon else max(
                ACTIONS, key=lambda a: q[(state, i, a)])
                for i in range(3))
            next_state, reward, stable = step(state, joint)
            for i, action in enumerate(joint):
                future = max(q[(next_state, i, a)] for a in ACTIONS)
                q[(state, i, action)] += alpha * (
                    reward + gamma * future - q[(state, i, action)]
                )
            state = next_state
            if stable:
                break
    return q


def evaluate(q, missions=30):
    successes = 0
    for _ in range(missions):
        state = (-3, 0, 3)
        for _ in range(25):
            joint = tuple(max(ACTIONS, key=lambda a: q[(state, i, a)]) for i in range(3))
            state, _, stable = step(state, joint)
            if stable:
                successes += 1
                break
    return successes / missions


if __name__ == "__main__":
    random.seed(11)
    q_table = train()
    print(f"Formation success rate: {evaluate(q_table):.0%}")
    print("Learned fleet action:", tuple(
        max(ACTIONS, key=lambda a: q_table[((-3, 0, 3), i, a)]) for i in range(3)
    ))
