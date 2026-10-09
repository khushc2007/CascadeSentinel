from __future__ import annotations

from .dc_power_flow import solve_dc
from .models import Grid


def base_injections(grid: Grid) -> dict[int, float]:
    injections = {bus.id: -bus.p_load for bus in grid.buses}
    for generator in grid.generators: injections[generator.bus] = injections.get(generator.bus, 0.0) + generator.p_dispatch
    return injections


def solve_base_case(grid: Grid):
    return solve_dc(grid, base_injections(grid))
