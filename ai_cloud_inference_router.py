#!/usr/bin/env python3
"""Cloud AI: choose the best inference model for each request."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Model:
    name: str
    quality: float
    latency_ms: int
    cost_per_1k: float

MODELS = (
    Model("edge-small", 0.78, 35, 0.02),
    Model("cloud-balanced", 0.90, 180, 0.08),
    Model("cloud-reasoning", 0.97, 650, 0.22),
)

def route_ai_request(complexity: float, max_latency_ms: int) -> Model:
    """Route to the highest-quality model that satisfies the cloud SLA."""
    candidates = [m for m in MODELS if m.latency_ms <= max_latency_ms]
    if not candidates:
        return MODELS[0]
    target = min(0.78 + complexity * 0.20, 0.97)
    return min(candidates, key=lambda m: (abs(m.quality - target), m.cost_per_1k))

if __name__ == "__main__":
    for complexity, sla in [(0.2, 80), (0.6, 250), (1.0, 900)]:
        model = route_ai_request(complexity, sla)
        print(f"complexity={complexity:.1f}, SLA={sla}ms -> {model.name}")
