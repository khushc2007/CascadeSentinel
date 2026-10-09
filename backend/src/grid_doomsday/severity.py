from __future__ import annotations

from .models import CascadeResult


def severity(result: CascadeResult) -> float: return result.s

def ranking_key(result: CascadeResult) -> tuple[float, tuple[int, ...]]: return (-result.s, result.outage_set)
