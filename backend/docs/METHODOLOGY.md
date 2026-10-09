# Methodology

The proposed study evaluates exactly-k transmission outages under a deterministic quasi-steady-state cascade model. A case is validated, a base case is solved, outage combinations are generated without replacement, and each candidate is replayed using the same ordering, thresholds, balancing policy, and stopping rule.

The planned DC approximation solves `B_red theta = P_gen - P_load`; each in-service branch uses `F_ij = b_ij(theta_i-theta_j)`. Islanding is detected from graph connectivity. Each island is balanced according to the V2 policy before the next flow solve. Overloads are compared with the configured rating and persistence rule.

Severity is reported as a vector and scalar, including served-load loss, overload exposure, islanding/blackout impact, and cascade extent. The score must disclose normalization, weights, and thresholds. AC verification, case-specific validation, sensitivity analysis, and all published conclusions remain future work.

The comparison baseline is exhaustive enumeration, followed by deterministic classical ranking. Quantum methods are compared only through explicit oracle formulations, emulation, or analytical resource estimates until circuits are independently audited and hardware evidence is available.
