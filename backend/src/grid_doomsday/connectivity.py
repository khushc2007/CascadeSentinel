from __future__ import annotations

from collections import deque
from typing import Iterable

from .models import Branch, Grid


def connected_components(grid: Grid, active_branch_ids: Iterable[int] | None = None) -> tuple[tuple[int, ...], ...]:
    active = set(grid.candidate_branch_ids if active_branch_ids is None else active_branch_ids)
    adjacency: dict[int, list[int]] = {bus.id: [] for bus in grid.buses}
    for branch in grid.branches:
        if branch.id in active and branch.status:
            adjacency[branch.from_bus].append(branch.to_bus)
            adjacency[branch.to_bus].append(branch.from_bus)
    unseen = set(adjacency)
    components: list[tuple[int, ...]] = []
    while unseen:
        root = min(unseen)
        queue = deque([root]); unseen.remove(root); component = []
        while queue:
            node = queue.popleft(); component.append(node)
            for neighbor in adjacency[node]:
                if neighbor in unseen:
                    unseen.remove(neighbor); queue.append(neighbor)
        components.append(tuple(sorted(component)))
    return tuple(sorted(components, key=lambda item: item[0]))


def active_branches(grid: Grid, outages: Iterable[int]) -> tuple[int, ...]:
    lost = set(outages)
    return tuple(branch.id for branch in grid.branches if branch.status and branch.id not in lost)


def branches_in_islands(grid: Grid, islands: tuple[tuple[int, ...], ...]) -> dict[int, int]:
    lookup = {bus: index for index, island in enumerate(islands) for bus in island}
    return {branch.id: lookup.get(branch.from_bus, -1) for branch in grid.branches}
