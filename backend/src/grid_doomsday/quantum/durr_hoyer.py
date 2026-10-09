from __future__ import annotations
import random

def classical_maximum_scan(values: list[float], seed: int=0) -> tuple[int,float,int]:
    """Deterministic classical baseline; this is not a quantum Durr-Hoyer implementation."""
    if not values: raise ValueError('values must not be empty')
    rng=random.Random(seed); index=rng.randrange(len(values)); threshold=values[index]; calls=1
    for candidate,value in enumerate(values):
        calls+=1
        if value>threshold: index,threshold=candidate,value
    return index,threshold,calls
