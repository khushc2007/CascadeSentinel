from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
@dataclass(frozen=True)
class CrossoverEstimate:
    candidates:int; oracle_cost:float; quantum_clock:float; classical_time:float; quantum_time:float
    @property
    def quantum_wins(self)->bool:return self.quantum_time<self.classical_time

def estimate(candidates:int, oracle_cost:float=1.0, quantum_clock:float=1.0, classical_time_per_eval:float=1.0, parallelism:int=1)->CrossoverEstimate:
    classical=candidates*classical_time_per_eval/max(1,parallelism); quantum=sqrt(candidates)*oracle_cost/quantum_clock
    return CrossoverEstimate(candidates,oracle_cost,quantum_clock,classical,quantum)
