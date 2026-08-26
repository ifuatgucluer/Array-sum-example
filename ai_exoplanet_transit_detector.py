#!/usr/bin/env python3
"""Tiny explainable baseline for spotting exoplanet transit candidates."""

from statistics import mean


def detect_transit(flux, threshold=0.985):
    """Return candidate indices where brightness falls below the threshold."""
    baseline = mean(flux)
    candidates = [i for i, value in enumerate(flux) if value / baseline < threshold]
    return candidates


if __name__ == "__main__":
    # A compact light-curve example: repeated dips may indicate a transit.
    light_curve = [1.000, 0.999, 0.998, 0.970, 0.999, 1.001, 0.997, 0.969, 1.000]
    hits = detect_transit(light_curve)
    print(f"Transit candidates: {hits}")
    print("Interpretation: repeated brightness dips deserve astronomical review.")
