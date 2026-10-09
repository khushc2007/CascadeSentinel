from __future__ import annotations

from .connectivity import active_branches, connected_components
from .dc_power_flow import solve_dc
from .island_balancing import balance_islands
from .models import CascadeResult, CascadeRound, CascadeStatus, Grid


def run_cascade(grid: Grid, outages: tuple[int, ...], *, trip_multiplier: float = 1.0, max_rounds: int = 30) -> CascadeResult:
    known = {branch.id for branch in grid.branches}
    outage_set = tuple(sorted(outages))
    if len(set(outage_set)) != len(outage_set):
        raise ValueError("outages must not contain duplicates")
    if any(branch_id not in known for branch_id in outage_set):
        raise ValueError("outage contains an unknown branch id")
    if trip_multiplier <= 0 or max_rounds < 0:
        raise ValueError("trip_multiplier must be positive and max_rounds non-negative")
    active = active_branches(grid, outage_set); rounds = []; flags = []
    injections, served, generation_lost, balance_diag = balance_islands(grid, active)
    s0 = 1.0 - served / grid.load_total if grid.load_total else 0.0
    status = CascadeStatus.STABLE
    for round_index in range(max_rounds + 1):
        islands = connected_components(grid, active)
        solution = solve_dc(grid, injections, active)
        if not solution.converged:
            flags.append("dc_nonconvergence"); status = CascadeStatus.EXHAUSTED; break
        overloaded = tuple(sorted(branch.id for branch in grid.branches if branch.id in solution.branch_flows and abs(solution.branch_flows[branch.id]) > trip_multiplier * branch.rating + 1e-9))
        trips = overloaded if round_index < max_rounds else ()
        rounds.append(CascadeRound(round_index, tuple(active), islands, trips, served, solution.branch_flows, balance_diag))
        if not trips: status = CascadeStatus.STABLE; break
        active = tuple(branch_id for branch_id in active if branch_id not in trips)
        injections, served, generation_lost, balance_diag = balance_islands(grid, active)
        if served <= 1e-12:
            status = CascadeStatus.TOTAL_LOSS; break
    else:
        status = CascadeStatus.EXHAUSTED; flags.append("max_rounds")
    s = 1.0 - served / grid.load_total if grid.load_total else 0.0
    return CascadeResult(tuple(sorted(outages)), status, s, s0, max(0.0, s - s0), s / max(s0, 0.01), tuple(rounds), sum(len(r.trips) for r in rounds), max((len(r.islands) for r in rounds), default=0), generation_lost, tuple(flags))
