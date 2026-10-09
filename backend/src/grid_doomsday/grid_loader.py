from __future__ import annotations

from .models import Branch, Bus, BusType, Generator, Grid


def toy_grid() -> Grid:
    """Small deterministic 5-bus ring used for smoke tests and demos."""
    buses = tuple(Bus(i, p_load=(0.0 if i == 0 else 20.0), bus_type=BusType.SLACK if i == 0 else BusType.PQ) for i in range(5))
    branches = tuple(Branch(i, i, (i + 1) % 5, reactance=0.1, rating=35.0) for i in range(5))
    generators = (Generator(0, 0, 0.0, 120.0, 80.0),)
    return Grid(buses, branches, generators, metadata={"source": "built-in toy", "case": "ring5"})


def load_case(name: str = "toy") -> Grid:
    normalized = name.lower().replace("ieee-", "").replace("ieee", "")
    if normalized in {"toy", "ring5", "5"}:
        return toy_grid()
    raise ValueError(f"Case {name!r} is not bundled. Install pandapower and add a case adapter for IEEE datasets.")
