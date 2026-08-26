#!/usr/bin/env python3
"""Original mini game: an AI captain chooses attack, shield, or evade."""

def ai_turn(player, enemy):
    """Choose a safe action from energy, shields, and distance."""
    if player["energy"] < 3:
        return "shield"
    if enemy["hull"] <= 3 and player["distance"] <= 5:
        return "attack"
    return "evade" if enemy["weapon"] > player["shield"] else "attack"


def resolve(player, enemy):
    action = ai_turn(player, enemy)
    if action == "attack":
        enemy["hull"] -= 3
        player["energy"] -= 3
    elif action == "shield":
        player["shield"] += 2
        player["energy"] += 2
    else:
        player["distance"] += 3
        player["energy"] -= 1
    return action


if __name__ == "__main__":
    player = {"energy": 6, "shield": 4, "distance": 4}
    enemy = {"hull": 3, "weapon": 5}
    action = resolve(player, enemy)
    print(f"AI captain action: {action}")
    print(f"Enemy hull: {enemy['hull']} | Player energy: {player['energy']}")
