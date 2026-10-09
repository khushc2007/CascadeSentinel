from __future__ import annotations
from .models import Grid, OperatingPoint

def solve_ac(grid: Grid, injections: dict[int,float], active_branch_ids=None) -> OperatingPoint:
    """AC verification boundary. Requires an explicit pandapower adapter; never silently falls back to DC."""
    raise NotImplementedError('AC solver is pending the pandapower case adapter and validation fixtures')
