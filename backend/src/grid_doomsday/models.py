from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BusType(str, Enum):
    SLACK = "slack"
    PV = "pv"
    PQ = "pq"


class CascadeStatus(str, Enum):
    STABLE = "stable"
    EXHAUSTED = "exhausted"
    TOTAL_LOSS = "total_loss"
    AC_INFEASIBLE = "ac_infeasible"


@dataclass(frozen=True)
class Bus:
    id: int
    p_load: float = 0.0
    q_load: float = 0.0
    bus_type: BusType = BusType.PQ
    v_min: float = 0.9
    v_max: float = 1.1


@dataclass(frozen=True)
class Branch:
    id: int
    from_bus: int
    to_bus: int
    reactance: float
    resistance: float = 0.0
    susceptance: float = 0.0
    rating: float = 1.0
    status: bool = True
    transformer: bool = False


@dataclass(frozen=True)
class Generator:
    id: int
    bus: int
    p_min: float
    p_max: float
    p_dispatch: float
    q_min: float = -1e9
    q_max: float = 1e9


@dataclass
class Grid:
    buses: tuple[Bus, ...]
    branches: tuple[Branch, ...]
    generators: tuple[Generator, ...] = ()
    base_mva: float = 100.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def load_total(self) -> float:
        return sum(bus.p_load for bus in self.buses)

    @property
    def candidate_branch_ids(self) -> tuple[int, ...]:
        return tuple(branch.id for branch in self.branches if branch.status)


@dataclass(frozen=True)
class OperatingPoint:
    injections: dict[int, float]
    branch_flows: dict[int, float]
    converged: bool = True
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class CascadeRound:
    index: int
    active_branches: tuple[int, ...]
    islands: tuple[tuple[int, ...], ...]
    trips: tuple[int, ...]
    served_load: float
    branch_flows: dict[int, float]
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class CascadeResult:
    outage_set: tuple[int, ...]
    status: CascadeStatus
    s: float
    s0: float
    c: float
    a: float
    rounds: tuple[CascadeRound, ...]
    total_trips: int
    max_islands: int
    generation_lost: float = 0.0
    flags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "outage_set": list(self.outage_set), "status": self.status.value,
            "s": self.s, "s0": self.s0, "c": self.c, "a": self.a,
            "total_trips": self.total_trips, "max_islands": self.max_islands,
            "generation_lost": self.generation_lost, "flags": list(self.flags),
            "rounds": [{"index": r.index, "active_branches": list(r.active_branches),
                        "islands": [list(i) for i in r.islands], "trips": list(r.trips),
                        "served_load": r.served_load, "branch_flows": r.branch_flows,
                        "diagnostics": r.diagnostics} for r in self.rounds],
        }
