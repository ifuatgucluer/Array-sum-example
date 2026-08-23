#!/usr/bin/env python3
"""Generative Engineering AI: compact topology optimization prototype.

This SIMP-inspired model prunes low-value material while preserving a
load path. It is a research prototype, not a certified design tool.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class TopologyConfig:
    rows: int = 18
    cols: int = 28
    volume_fraction: float = 0.42
    iterations: int = 35

class GenerativeTopologyOptimizer:
    def __init__(self, config: TopologyConfig | None = None):
        self.cfg = config or TopologyConfig()
        self.density = np.full((self.cfg.rows, self.cfg.cols), self.cfg.volume_fraction)
        self.density[:, 0] = 1.0
        mid = self.cfg.rows // 2
        self.density[mid - 1:mid + 1, -1] = 1.0

    def compliance_proxy(self) -> float:
        dx = np.diff(self.density, axis=1)
        dy = np.diff(self.density, axis=0)
        stiffness = max(float(self.density.mean()) ** 3, 1e-6)
        return float((1 + np.mean(dx * dx) + np.mean(dy * dy)) / stiffness)

    def sensitivity(self) -> np.ndarray:
        y, x = np.indices(self.density.shape)
        center = (self.cfg.rows - 1) / 2
        load_path = 1 / (1 + np.abs(y - center))
        distance = x / max(self.cfg.cols - 1, 1)
        return load_path * (0.55 + 0.45 * distance) * self.density ** 2

    def filter_field(self, field: np.ndarray) -> np.ndarray:
        result = np.zeros_like(field)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                result += np.roll(np.roll(field, dr, axis=0), dc, axis=1)
        return result / 9

    def optimize(self) -> tuple[np.ndarray, list[float]]:
        history = []
        for _ in range(self.cfg.iterations):
            score = self.filter_field(self.sensitivity())
            threshold = np.quantile(score[:, 1:], 1 - self.cfg.volume_fraction)
            self.density = np.where(score >= threshold, 1.0, 0.05)
            self.density[:, 0] = 1.0
            mid = self.cfg.rows // 2
            self.density[mid - 1:mid + 1, -1] = 1.0
            history.append(self.compliance_proxy())
        return self.density, history

    def ascii_design(self) -> str:
        return "\n".join("".join("##" if c > 0.5 else ".." for c in row) for row in self.density)

if __name__ == "__main__":
    optimizer = GenerativeTopologyOptimizer()
    _, history = optimizer.optimize()
    print("--- Generative Topology Optimization ---")
    print(f"Iterations: {len(history)} | Final compliance proxy: {history[-1]:.4f}")
    print(optimizer.ascii_design())
    print("Prototype complete: validate with certified FEA before manufacture.")
