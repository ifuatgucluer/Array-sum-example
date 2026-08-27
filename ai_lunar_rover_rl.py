#!/usr/bin/env python3
"""Q-learning rover that learns a short, crater-free route to a lunar base."""

import random
from collections import defaultdict

ACTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
CRATERS = {(1, 1), (2, 3), (3, 1)}
START, BASE = (0, 0), (4, 4)


def step(position, action):
    target = (position[0] + action[0], position[1] + action[1])
    if not (0 <= target[0] < 5 and 0 <= target[1] < 5) or target in CRATERS:
        return position, -4, False
    if target == BASE:
        return target, 15, True
    return target, -1, False


def train(episodes=900, alpha=0.2, gamma=0.9):
    q = defaultdict(float)
    for episode in range(episodes):
        state = START
        epsilon = max(0.03, 1 - episode / episodes)
        for _ in range(40):
            explore = random.random() < epsilon
            action = random.choice(ACTIONS) if explore else max(
                ACTIONS, key=lambda move: q[(state, move)]
            )
            next_state, reward, done = step(state, action)
            best_future = max(q[(next_state, move)] for move in ACTIONS)
            q[(state, action)] += alpha * (
                reward + gamma * best_future - q[(state, action)]
            )
            state = next_state
            if done:
                break
    return q


def evaluate(q, missions=30):
    successes, steps = 0, 0
    for _ in range(missions):
        state = START
        for attempt in range(40):
            action = max(ACTIONS, key=lambda move: q[(state, move)])
            state, _, done = step(state, action)
            if done:
                successes += state == BASE
                steps += attempt + 1
                break
    return successes / missions, steps / missions


if __name__ == "__main__":
    random.seed(31)
    q_table = train()
    success, average_steps = evaluate(q_table)
    first_move = max(ACTIONS, key=lambda move: q_table[(START, move)])
    print(f"Lunar base success rate: {success:.0%}")
    print(f"Average route length: {average_steps:.1f} steps")
    print(f"Learned first move: {first_move}")
