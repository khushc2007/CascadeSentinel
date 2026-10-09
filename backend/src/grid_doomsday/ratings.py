from __future__ import annotations

from dataclasses import replace

from .models import Grid


def apply_ratings(grid: Grid, base_flows: dict[int, float], headroom: float = 0.2, floor_fraction: float = 0.05) -> Grid:
    floor = max((abs(value) for value in base_flows.values()), default=1.0) * floor_fraction
    branches = tuple(replace(branch, rating=max((1 + headroom) * abs(base_flows.get(branch.id, 0.0)), floor)) for branch in grid.branches)
    return replace(grid, branches=branches, metadata={**grid.metadata, "synthetic_ratings": True, "headroom": headroom, "rating_floor": floor})
