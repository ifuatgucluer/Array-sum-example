#!/usr/bin/env python3
"""Mini game: balance demand, solar power, battery, and city happiness."""

def play_turn(demand, solar, battery, action):
    """Return the next battery level, grid use, and game score."""
    if action == "save":
        battery = min(10, battery + max(solar - demand, 0))
    elif action == "boost":
        battery = max(0, battery - min(3, battery))
        demand += 2  # extra comfort for the city

    grid = max(0, demand - solar - max(0, battery - 5))
    score = 100 - grid * 8 - abs(demand - solar) * 2
    return battery, grid, round(max(score, 0), 1)

if __name__ == "__main__":
    battery = 6
    total = 0
    for turn, (demand, solar, action) in enumerate(
        [(5, 2, "save"), (7, 6, "save"), (8, 3, "boost")], 1
    ):
        battery, grid, score = play_turn(demand, solar, battery, action)
        total += score
        print(f"Turn {turn}: action={action}, grid={grid} kW, score={score}")
    print(f"AI energy captain total score: {round(total, 1)}")
