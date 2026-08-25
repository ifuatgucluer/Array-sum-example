#!/usr/bin/env python3
"""Human-in-the-loop digital twin lab: predict, explain, and ask before acting."""
from dataclasses import dataclass
from statistics import mean, pstdev

@dataclass
class TwinDecision:
    prediction: float
    uncertainty: float
    explanation: str
    action: str

def learn_linear_trend(values):
    x = list(range(len(values)))
    x_bar, y_bar = mean(x), mean(values)
    slope = sum((i - x_bar) * (y - y_bar) for i, y in zip(x, values))
    slope /= sum((i - x_bar) ** 2 for i in x) or 1
    intercept = y_bar - slope * x_bar
    residuals = [y - (intercept + slope * i) for i, y in zip(x, values)]
    return intercept, slope, pstdev(residuals) or 0.1

def inspect_twin(sensor_values, alert_limit=1.0):
    intercept, slope, noise = learn_linear_trend(sensor_values)
    prediction = intercept + slope * len(sensor_values)
    explanation = f"trend={slope:+.2f}/step, noise={noise:.2f}"
    risk = abs(slope) * 3 + noise
    action = "HUMAN REVIEW" if risk > alert_limit else "MONITOR"
    return TwinDecision(round(prediction, 2), round(risk, 2), explanation, action)

if __name__ == "__main__":
    demo_temperature = [21.0, 21.2, 21.4, 21.7, 22.0, 22.3]
    decision = inspect_twin(demo_temperature)
    print(decision)
    print("No automatic intervention: a human engineer remains in the loop.")
