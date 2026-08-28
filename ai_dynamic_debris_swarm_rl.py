#!/usr/bin/env python3
"""Tabular RL demo: a satellite swarm avoids moving debris and orbit drift."""

import random
from collections import defaultdict

ACTIONS = (-1, 0, 1)
START = (-3, 0, 3)
TARGET = (-1, 0, 1)


def debris_at(t):
    return ((t * 2 - 2) % 7) - 3


def step(state, joint_action, t):
    drift = 1 if t % 4 == 3 else 0
    next_state = tuple(state[i] + joint_action[i] + drift for i in range(3))
    debris = debris_at(t)
    collision = any(position == debris for position in next_state)
    spread = max(next_state) - min(next_state)
    error = sum(abs(next_state[i] - TARGET[i]) for i in range(3))
    reward = -error - 2 * drift - (14 if collision else 0)
    safe = not collision and spread <= 3
    done = collision or (safe and error == 0) or t >= 19
    if safe and error == 0:
        reward += 18
    return next_state, reward, done, collision


def train(episodes=1500, alpha=0.2, gamma=0.9):
    q = defaultdict(float)
    for episode in range(episodes):
        state, t = START, 0
        epsilon = max(0.03, 1 - episode / episodes)
        for _ in range(20):
            joint = tuple(
                random.choice(ACTIONS) if random.random() < epsilon else max(
                    ACTIONS, key=lambda action: q[(state, t, i, action)]
                )
                for i in range(3)
            )
            next_state, reward, done, _ = step(state, joint, t)
            for i, action in enumerate(joint):
                future = max(q[(next_state, t + 1, i, a)] for a in ACTIONS)
                q[(state, t, i, action)] += alpha * (
                    reward + gamma * future - q[(state, t, i, action)]
                )
            state, t = next_state, t + 1
            if done:
                break
    return q


def evaluate(q, missions=40):
    successes, collisions = 0, 0
    for _ in range(missions):
        state, t = START, 0
        for _ in range(20):
            joint = tuple(max(ACTIONS, key=lambda a: q[(state, t, i, a)]) for i in range(3))
            state, _, done, hit = step(state, joint, t)
            collisions += hit
            t += 1
            if done:
                successes += int(not hit and max(state) - min(state) <= 3)
                break
    return successes / missions, collisions


if __name__ == "__main__":
    random.seed(23)
    q_table = train()
    success, collisions = evaluate(q_table)
    opening = tuple(max(ACTIONS, key=lambda a: q_table[(START, 0, i, a)]) for i in range(3))
    print(f"Dynamic-mission success rate: {success:.0%}")
    print(f"Collisions during evaluation: {collisions}")
    print(f"Learned opening action: {opening}")
