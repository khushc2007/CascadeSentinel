from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Callable, Iterable
from .contingency import enumerate_outages
from .models import CascadeResult

@dataclass
class SearchResult:
    best: CascadeResult | None
    evaluations: int
    candidates: list[CascadeResult]

def exhaustive(branch_ids: Iterable[int], k: int, oracle: Callable[[tuple[int,...]], CascadeResult]) -> SearchResult:
    results=[oracle(x) for x in enumerate_outages(branch_ids,k)]
    return SearchResult(max(results, key=lambda r:r.s, default=None),len(results),results)

def random_sample(branch_ids: Iterable[int], k: int, oracle, samples: int, seed: int=0) -> SearchResult:
    if samples < 0:
        raise ValueError("samples must be non-negative")
    rng = random.Random(seed); ids = tuple(sorted(set(branch_ids)))
    if k < 0 or k > len(ids):
        raise ValueError("k is outside the available branch range")
    candidates = list(enumerate_outages(ids, k))
    rng.shuffle(candidates)
    results = [oracle(outage) for outage in candidates[:min(samples, len(candidates))]]
    return SearchResult(max(results, key=lambda r: r.s, default=None), len(results), results)

def threshold(branch_ids, k, oracle, tau: float) -> SearchResult:
    for index, outage in enumerate(enumerate_outages(branch_ids,k),1):
        result=oracle(outage)
        if result.s >= tau: return SearchResult(result,index,[result])
    return SearchResult(None,index if 'index' in locals() else 0,[])

def top_t(branch_ids, k, oracle, top: int) -> SearchResult:
    result=exhaustive(branch_ids,k,oracle); return SearchResult(result.best,result.evaluations,sorted(result.candidates,key=lambda r:r.s,reverse=True)[:top])
