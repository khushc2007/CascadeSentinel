from __future__ import annotations

from .connectivity import connected_components
from .models import Grid


def balance_islands(grid: Grid, active_branch_ids: tuple[int, ...]) -> tuple[dict[int, float], float, float, dict[str, object]]:
    """Redispatch each island and curtail load while preserving zero net injection."""
    injections = {bus.id: 0.0 for bus in grid.buses}
    served = 0.0
    curtailed = 0.0
    diagnostics: dict[str, object] = {"islands": []}
    for island in connected_components(grid, active_branch_ids):
        island_buses = [bus for bus in grid.buses if bus.id in island]
        load = sum(bus.p_load for bus in island_buses)
        generators = [g for g in grid.generators if g.bus in island]
        lower = sum(g.p_min for g in generators)
        upper = sum(g.p_max for g in generators)
        target = min(max(load, lower), upper) if generators else 0.0
        served_island = min(load, target)
        curtailed += load - served_island
        served += served_island
        remaining = target
        dispatch: dict[int, float] = {}
        for generator in sorted(generators, key=lambda g: g.id):
            value = min(generator.p_max, max(generator.p_min, remaining))
            dispatch[generator.id] = value
            remaining -= value
        for bus in island_buses:
            injections[bus.id] -= bus.p_load * (served_island / load if load else 0.0)
        for generator in generators:
            injections[generator.bus] += dispatch.get(generator.id, 0.0)
        diagnostics["islands"].append({"buses": list(island), "load": load, "served": served_island,
            "curtailed": load - served_island, "generation_minimum": lower, "generation_capacity": upper,
            "dispatch": dispatch})
    return injections, served, curtailed, diagnostics
