#!/usr/bin/env python3
"""Q-learning agent that learns fuel-aware orbital correction."""

import random
from collections import defaultdict

ACTIONS = ("coast", "correct", "brake")


def step(state, action):
    altitude, fuel = state
    if action == "correct":
        altitude = min(10, altitude + 2)
        fuel -= 2
        reward = 3 if altitude >= 7 else -1
    elif action == "brake":
        altitude = max(0, altitude - 1)
        fuel -= 1
        reward = 1
    else:
        altitude = max(0, altitude - 2)
        reward = -1
    done = altitude >= 7 or fuel <= 0
    if altitude >= 7:
        reward += 10
    return (altitude, fuel), reward, done


def train(episodes=700, alpha=0.2, gamma=0.9):
    q = defaultdict(float)
    for episode in range(episodes):
        state = (3, 8)
        epsilon = max(0.03, 1 - episode / episodes)
        for _ in range(20):
            action = random.choice(ACTIONS) if random.random() < epsilon else max(
                ACTIONS, key=lambda a: q[(state, a)]
            )
            next_state, reward, done = step(state, action)
            future = max(q[(next_state, a)] for a in ACTIONS)
            q[(state, action)] += alpha * (reward + gamma * future - q[(state, action)])
            state = next_state
            if done:
                break
    return q


def evaluate(q, missions=30):
    successes = 0
    fuel_left = 0
    for _ in range(missions):
        state = (3, 8)
        for _ in range(20):
            action = max(ACTIONS, key=lambda a: q[(state, a)])
            state, _, done = step(state, action)
            if done:
                successes += state[0] >= 7
                fuel_left += state[1]
                break
    return successes / missions, fuel_left / missions


if __name__ == "__main__":
    random.seed(21)
    q_table = train()
    success, average_fuel = evaluate(q_table)
    opening = max(ACTIONS, key=lambda a: q_table[((3, 8), a)])
    print(f"Orbit success rate: {success:.0%}")
    print(f"Average fuel remaining: {average_fuel:.1f}")
    print(f"Learned opening action: {opening}")
