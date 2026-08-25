#!/usr/bin/env python3
"""Simple AI-inspired scheduler for reducing building energy use."""

def schedule_battery(demand_kw, solar_kw, battery_kwh=6, max_power_kw=2):
    """Use solar first, then battery during peak demand periods."""
    charge = 0.0
    grid = []
    for demand, solar in zip(demand_kw, solar_kw):
        surplus = max(solar - demand, 0)
        charge = min(battery_kwh, charge + surplus)
        deficit = max(demand - solar, 0)
        discharge = min(charge, deficit, max_power_kw)
        charge -= discharge
        grid.append(round(deficit - discharge, 2))
    return grid, round(charge, 2)

if __name__ == "__main__":
    demand = [4, 5, 7, 8, 6, 3]
    solar = [0, 2, 5, 6, 3, 0]
    grid, remaining = schedule_battery(demand, solar)
    print("Grid draw (kW):", grid)
    print("Battery remaining (kWh):", remaining)
    print("Peak after schedule (kW):", max(grid))
