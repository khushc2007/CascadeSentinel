from __future__ import annotations
import math

def grover_probability(space_size: int, marked: int, iterations: int) -> float:
    if not marked or not space_size: return 0.0
    theta=math.asin(math.sqrt(marked/space_size)); return math.sin((2*iterations+1)*theta)**2

def optimal_iterations(space_size:int,marked:int=1)->int:
    return max(0,round(math.pi/4*math.sqrt(space_size/marked)-0.5))
