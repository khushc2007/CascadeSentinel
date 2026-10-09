from __future__ import annotations

import numpy as np

from .connectivity import connected_components
from .models import Grid, OperatingPoint


def solve_dc(grid: Grid, injections: dict[int, float], active_branch_ids: tuple[int, ...] | None = None) -> OperatingPoint:
    active = set(grid.candidate_branch_ids if active_branch_ids is None else active_branch_ids)
    buses = [bus.id for bus in grid.buses]; index = {bus: i for i, bus in enumerate(buses)}
    flows: dict[int, float] = {}
    for island in connected_components(grid, active):
        island_injection = sum(injections.get(bus, 0.0) for bus in island)
        if abs(island_injection) > 1e-7:
            return OperatingPoint(injections, {}, False, {"reason": "unbalanced_island", "island": list(island), "net_injection": island_injection})
        if len(island) < 2:
            continue
        slack_candidates = [bus.id for bus in grid.buses if bus.id in island and bus.bus_type.value == "slack"]
        slack = slack_candidates[0] if slack_candidates else island[0]
        unknown = [bus for bus in island if bus != slack]
        matrix = np.zeros((len(unknown), len(unknown))); rhs = np.array([injections.get(bus, 0.0) for bus in unknown], dtype=float)
        for row, bus in enumerate(unknown):
            for branch in grid.branches:
                if branch.id not in active or branch.reactance == 0 or bus not in (branch.from_bus, branch.to_bus):
                    continue
                other = branch.to_bus if branch.from_bus == bus else branch.from_bus
                b = 1.0 / branch.reactance
                matrix[row, row] += b
                if other in unknown: matrix[row, unknown.index(other)] -= b
        try: angles = np.linalg.solve(matrix, rhs)
        except np.linalg.LinAlgError: return OperatingPoint(injections, {}, False, {"reason": "singular_island"})
        theta = {slack: 0.0, **dict(zip(unknown, angles))}
        for branch in grid.branches:
            if branch.id in active and branch.from_bus in theta and branch.to_bus in theta:
                flows[branch.id] = (theta[branch.from_bus] - theta[branch.to_bus]) / branch.reactance
    return OperatingPoint(injections, flows, True, {"active_branches": sorted(active)})
