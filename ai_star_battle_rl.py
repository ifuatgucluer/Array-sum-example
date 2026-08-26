#!/usr/bin/env python3
"""Compact reinforcement-learning star battle using tabular Q-learning."""

import random
from collections import defaultdict

ACTIONS = ("attack", "shield", "evade")


def step(state, action):
    energy, hull, distance, shield = state
    reward = -2

    if action == "attack" and energy >= 1 and distance <= 5:
        hull -= 3
        energy -= 1
        reward = 30 if hull <= 0 else 8
    elif action == "shield":
        shield = min(6, shield + 2)
        energy = min(6, energy + 1)
        reward = -1
    elif action == "evade":
        distance = min(9, distance + 3)
        energy = max(0, energy - 1)
        reward = -2

    if hull > 0 and distance <= 5:
        damage = 2 if shield < 5 else 0
        shield = max(0, shield - 2)
        energy = max(0, energy - damage)
        reward -= damage * 2

    done = hull <= 0
    return (energy, hull, distance, shield), reward, done


def choose(q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    return max(ACTIONS, key=lambda action: q[(state, action)])


def train(episodes=800, alpha=0.2, gamma=0.9):
    q = defaultdict(float)
    for episode in range(episodes):
        state = (6, 6, 4, 4)
        epsilon = max(0.03, 1.0 - episode / episodes)
        for _ in range(30):
            action = choose(q, state, epsilon)
            next_state, reward, done = step(state, action)
            future = max(q[(next_state, a)] for a in ACTIONS)
            q[(state, action)] += alpha * (reward + gamma * future - q[(state, action)])
            state = next_state
            if done:
                break
    return q


def evaluate(q, games=50):
    wins = 0
    for _ in range(games):
        state = (6, 6, 4, 4)
        for _ in range(30):
            action = choose(q, state, 0.0)
            state, _, done = step(state, action)
            if done:
                wins += state[1] <= 0
                break
    return wins / games


if __name__ == "__main__":
    random.seed(7)
    q_table = train()
    print(f"Greedy win rate after learning: {evaluate(q_table):.0%}")
    print("Learned opening move:", choose(q_table, (6, 6, 4, 4), 0.0))
