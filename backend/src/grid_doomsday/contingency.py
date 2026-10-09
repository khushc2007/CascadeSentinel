from __future__ import annotations
from itertools import combinations
from math import comb
from typing import Iterable, Iterator

def enumerate_outages(branch_ids: Iterable[int], k: int) -> Iterator[tuple[int, ...]]:
    ids = tuple(sorted(set(branch_ids)))
    if k < 0 or k > len(ids):
        raise ValueError(f"k must be between 0 and {len(ids)}")
    yield from combinations(ids, k)

def count_outages(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        raise ValueError("require 0 <= k <= n")
    return comb(n, k)

def rank_combination(values: tuple[int, ...], universe: tuple[int, ...]) -> int:
    positions = {v: i for i, v in enumerate(universe)}; rank = 0; previous = -1
    for i, value in enumerate(values):
        position = positions[value]
        for candidate in range(previous + 1, position): rank += comb(len(universe) - candidate - 1, len(values) - i - 1)
        previous = position
    return rank

def unrank_combination(rank: int, universe: tuple[int, ...], k: int) -> tuple[int, ...]:
    result=[]; start=0
    for remaining in range(k, 0, -1):
        for position in range(start, len(universe)):
            block=comb(len(universe)-position-1, remaining-1)
            if rank < block: result.append(universe[position]); start=position+1; break
            rank -= block
    return tuple(result)
