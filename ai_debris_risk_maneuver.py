#!/usr/bin/env python3
"""Continuation module: score space-debris risk and recommend a safe maneuver."""

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class ObjectTrack:
    name: str
    distance_km: float
    relative_speed_kms: float
    uncertainty_km: float


def collision_risk(track: ObjectTrack, horizon_s: int = 60) -> float:
    """Transparent proxy risk score for an educational orbital screen."""
    closing_distance = max(0.0, track.distance_km - abs(track.relative_speed_kms) * horizon_s)
    proximity = exp(-closing_distance / 4.0)
    uncertainty = min(1.0, track.uncertainty_km / 10.0)
    speed_factor = min(1.0, abs(track.relative_speed_kms) / 8.0)
    return min(1.0, 0.65 * proximity + 0.20 * uncertainty + 0.15 * speed_factor)


def recommend_maneuver(risks: dict[str, float]) -> str:
    peak = max(risks.values(), default=0.0)
    if peak >= 0.70:
        return "EMERGENCY_AVOIDANCE: raise_or_lower_orbit_and_request_review"
    if peak >= 0.35:
        return "CAUTION: schedule_small_plane_change"
    return "NOMINAL: maintain_orbit_and_monitor"


def assess(tracks: list[ObjectTrack]) -> dict[str, object]:
    risks = {track.name: round(collision_risk(track), 3) for track in tracks}
    peak = max(risks.values(), default=0.0)
    return {
        "object_risk": risks,
        "peak_risk": peak,
        "status": "REVIEW_REQUIRED" if peak >= 0.35 else "SAFE_TO_MONITOR",
        "maneuver": recommend_maneuver(risks),
    }


if __name__ == "__main__":
    tracks = [
        ObjectTrack("DEBRIS-A", distance_km=7.0, relative_speed_kms=0.08, uncertainty_km=2.0),
        ObjectTrack("DEBRIS-B", distance_km=2.5, relative_speed_kms=0.04, uncertainty_km=5.0),
    ]
    print(assess(tracks))
