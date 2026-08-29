#!/usr/bin/env python3
"""Small AI-inspired scheduler for delayed interstellar mission messages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionMessage:
    name: str
    priority: int
    delay_minutes: float
    energy_cost: float


def utility(message: MissionMessage, available_energy: float) -> float:
    urgency = 1 / message.priority
    delay_penalty = 1 / (1 + message.delay_minutes / 60)
    energy_fit = min(1.0, available_energy / max(message.energy_cost, 1))
    return 0.55 * urgency + 0.30 * delay_penalty + 0.15 * energy_fit


def schedule(messages: list[MissionMessage], energy_budget: float) -> list[str]:
    ranked = sorted(messages, key=lambda m: utility(m, energy_budget), reverse=True)
    sent, remaining = [], energy_budget
    for message in ranked:
        if message.energy_cost <= remaining:
            sent.append(message.name)
            remaining -= message.energy_cost
    return sent


if __name__ == "__main__":
    queue = [
        MissionMessage("life_support_alert", 1, 42, 8),
        MissionMessage("science_packet", 3, 18, 5),
        MissionMessage("crew_video", 5, 90, 4),
    ]
    print("Transmission order:", schedule(queue, energy_budget=13))
