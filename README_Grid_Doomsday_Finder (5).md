# Grid Doomsday Finder

**Constrained quantum-search benchmark for high-severity exactly-\(k\) transmission-branch outages under a deterministic quasi-steady-state cascade model**

**Event:** Q-Hack India 2026 — National Quantum Hackathon, Quantum Week 2026  
**Track:** Track 04 — Open Quantum Innovation  
**Specification:** `Grid_Doomsday_Finder_Solution_Design_V2.pdf`  
**Specification status:** V2 is authoritative and supersedes V1.

> **Important status notice:** This README describes the project design and the intended software architecture. A file existing in the repository does not mean its feature is implemented, tested, or scientifically validated. Replace every status marker below with evidence from the actual repository and experiment outputs. Do not invent results, benchmark values, or quantum advantage.

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Project objective](#2-project-objective)
3. [Problem statement](#3-problem-statement)
4. [Scope and non-goals](#4-scope-and-non-goals)
5. [Mathematical formulation](#5-mathematical-formulation)
6. [Severity metrics](#6-severity-metrics)
7. [System overview](#7-system-overview)
8. [Repository architecture](#8-repository-architecture)
9. [Grid digital twin and data provenance](#9-grid-digital-twin-and-data-provenance)
10. [Cascade simulation methodology](#10-cascade-simulation-methodology)
11. [DC and AC model fidelity](#11-dc-and-ac-model-fidelity)
12. [Classical search and baselines](#12-classical-search-and-baselines)
13. [Quantum search formulation](#13-quantum-search-formulation)
14. [Three-tier quantum evidence model](#14-three-tier-quantum-evidence-model)
15. [QAOA comparison](#15-qaoa-comparison)
16. [Resource estimation and crossover analysis](#16-resource-estimation-and-crossover-analysis)
17. [Experiment plan E0–E16](#17-experiment-plan-e0e16)
18. [Verification and testing](#18-verification-and-testing)
19. [API and frontend integration](#19-api-and-frontend-integration)
20. [Installation and development setup](#20-installation-and-development-setup)
21. [Running the project](#21-running-the-project)
22. [Configuration and reproducibility](#22-configuration-and-reproducibility)
23. [Results, artifacts, and reporting](#23-results-artifacts-and-reporting)
24. [Evidence labels](#24-evidence-labels)
25. [Claims policy](#25-claims-policy)
26. [Limitations and threats to validity](#26-limitations-and-threats-to-validity)
27. [Security and responsible use](#27-security-and-responsible-use)
28. [Development roadmap](#28-development-roadmap)
29. [Contribution workflow](#29-contribution-workflow)
30. [Troubleshooting](#30-troubleshooting)
31. [Glossary](#31-glossary)
32. [References and source of truth](#32-references-and-source-of-truth)
33. [Current implementation status](#33-current-implementation-status)

---

## 1. Executive summary

Grid Doomsday Finder is a research and demonstration project for identifying high-severity sets of simultaneous transmission-branch outages under a stated deterministic quasi-steady-state cascading model. It frames the task as a cardinality-constrained search problem and compares a classical evaluation pipeline with quantum-search formulations, including Grover-style amplitude amplification, BBHT-style search, Dürr–Høyer maximum finding, and a separate QAOA surrogate experiment.

The principal reference systems in the V2 design are IEEE 14-bus, IEEE 30-bus, and IEEE 118-bus networks. The IEEE 118-bus case has 118 buses and 186 branches. For exactly three initiating branch outages, the candidate space contains

\[
\binom{186}{3}=1{,}055{,}240
\]

sets. Larger outage cardinalities grow rapidly, making the cost of repeatedly evaluating a cascade central to the study.

The planned pipeline contains:

- a versioned grid representation and base operating point;
- explicit, documented branch-rating assumptions;
- a deterministic DC quasi-steady-state cascade model for screening and search;
- a higher-fidelity AC model for static verification;
- severity measurements that separate immediate load loss from cascade-induced loss;
- classical exhaustive and structure-exploiting search baselines;
- cardinality-constrained quantum-search circuits on small instances;
- exact classical emulation of idealized search dynamics at larger search-space sizes;
- a toy reversible micro-oracle to calibrate component-level resource estimates;
- a resource and crossover model;
- reproducible experiment scripts and generated result artifacts; and
- an existing web dashboard intended to display project information and results.

**This is not a real-world blackout prediction system.** The model does not include electromagnetic transients, detailed protection timing, operator actions, or utility-specific operational data. Branch ratings may be synthetic and must be labelled as such. Quantum query complexity is not the same as wall-clock speedup, and no quantum advantage should be claimed unless supported by a fair measured comparison.

### Status of this repository

This README is intended to be the full project guide. The repository may initially contain only the frontend and minimal backend scaffolding. The current status must be determined by inspecting the actual source files, running the tests, and checking generated artifacts. Do not treat the architecture described here as proof that the corresponding modules already exist or work.

---

## 2. Project objective

The project investigates the following question:

> Given a transmission network, a documented base operating point, a fixed cascade policy, and an outage cardinality \(k\), which exactly-\(k\) simultaneous initiating branch outages produce the greatest unserved load at the end of the modelled cascade, and what are the costs and limitations of finding those sets with classical and quantum-inspired search approaches?

The work has several objectives:

1. Define the exactly-\(k\) outage-search problem and its metrics unambiguously.
2. Establish a reproducible grid and cascade model.
3. Validate the model on small, hand-checkable cases before trusting larger results.
4. Compare DC screening against AC static verification.
5. Evaluate classical methods under transparent budgets.
6. Construct and test quantum-search circuits on tractable toy cases.
7. Separate circuit demonstrations from exact classical emulation and theoretical fault-tolerant resource estimates.
8. Estimate when query reductions could—or could not—translate into wall-clock advantages.
9. Present results in a web demonstration without conflating illustrative UI values with scientific measurements.

The project should measure these dependencies rather than assume that quantum search will outperform classical methods.

---

## 3. Problem statement

Let a network contain \(L\) candidate transmission branches. A candidate outage is a set of exactly \(k\) distinct branch indices. Each candidate is evaluated by applying the initial outages to the base network and running the specified cascade model until termination.

The main optimization target is the fraction of base load unserved when the cascade terminates. The objective is evaluated under a particular grid, rating configuration, operating point, cascade policy, solver fidelity, and software version. Changing any of these can change the ranking.

The term **high-severity outage set** refers only to an outage set that scores highly under the defined model and configuration. It does not mean that the set will necessarily cause a real-world blackout.

### Reference scale

The V2 design includes the following benchmark scale:

| Grid | Buses | Branches \(L\) | Example search-space fact |
|---|---:|---:|---|
| IEEE 14-bus | 14 | 20 | \(\binom{20}{3}=1{,}140\) |
| IEEE 30-bus | 30 | 41 | \(\binom{41}{3}=10{,}660\) |
| IEEE 118-bus | 118 | 186 | \(\binom{186}{3}=1{,}055{,}240\) |

These counts describe candidate combinations, not measured runtime. Runtime must be measured using the actual implementation and environment.

The V2 document also discusses a Polish 2383-bus system as a resource-model proxy. It must not be represented as a validated benchmark in this repository unless the data source, branch count, conversion, and actual experiment are documented.

---

## 4. Scope and non-goals

### In scope

- Benchmark grid loading and validation.
- Explicit base operating-point and branch-rating configuration.
- Exactly-\(k\) outage-set generation and indexing.
- DC power-flow screening.
- A deterministic quasi-steady-state overload cascade.
- Island detection and documented generation/load balancing.
- Severity metrics \(S\), \(S_0\), and \(C\), with \(A\) as a diagnostic.
- AC static verification where supported.
- Classical baselines and fair search-budget accounting.
- Toy quantum circuits and exact small-instance verification.
- Exact classical emulation of idealized quantum-search dynamics where specified.
- A reversible micro-oracle for resource calibration at toy scale.
- Analytical fault-tolerant resource and crossover estimates.
- QAOA on a clearly defined surrogate objective.
- Reproducible experiments, tests, and result artifacts.
- A frontend that presents results with explicit evidence labels.

### Out of scope

- Real-time control of transmission equipment.
- Switching instructions to a utility network.
- A validated operational blackout prediction service.
- Electromagnetic transient simulation.
- Detailed relay/protection timing and coordination.
- Human operator response and emergency-control modeling.
- Claiming that a simulator run is execution on quantum hardware.
- Claiming practical quantum advantage solely from asymptotic query complexity.
- Treating synthetic ratings as actual utility ratings.

---

## 5. Mathematical formulation

Let \(L\) be the number of candidate branches and \(k\) the required number of simultaneous initiating outages. The feasible set is

\[
\Omega_k=\{x\in\{0,1\}^{L}:|x|=k\}
\]

where each bit indicates whether a branch is part of the initiating outage set. The cardinality constraint requires exactly \(k\) selected branches.

The number of feasible candidates is

\[
N=|\Omega_k|=\binom{L}{k}.
\]

For a candidate \(x\), let \(S(x)\) be the final unserved-load fraction produced by the selected cascade model. The objective is

\[
x^\star\in\operatorname*{arg\,max}_{x\in\Omega_k} S(x).
\]

If several candidates share the same maximum severity, the implementation must document how ties are handled. A ranking output should preserve ties or state its deterministic tie-breaking rule.

### Important modeling details

- The outage cardinality is exactly \(k\), not “up to \(k\).”
- Branch indices must map consistently to the selected grid's branch records.
- Invalid, duplicate, or out-of-range branch indices must be rejected.
- The same grid hash, rating configuration, base operating point, cascade settings, and fidelity must be used when comparing search methods.
- If AC evaluation fails to converge, the result must be recorded with an explicit status. It must not silently be treated as a zero-severity case.
- Search outputs should state whether the returned result is the best candidate found within a budget or a certified maximum over the entire candidate space.

---

## 6. Severity metrics

The V2 definitions are authoritative.

### 6.1 Final unserved-load fraction: \(S\)

\(S\) is the fraction of base load unserved at cascade termination. It is the primary severity objective.

### 6.2 Initial unserved-load fraction: \(S_0\)

\(S_0\) is the fraction of base load unserved immediately after the initial outage set and island balancing, before overload-driven cascade trips. It measures loss associated with the initial contingency and immediate islanding/balancing outcome.

### 6.3 Cascade-induced loss: \(C\)

\[
C=S-S_0.
\]

\(C\) measures the incremental unserved-load fraction attributable to the subsequent cascade relative to the initial post-outage state. Numerical tolerance and handling of small negative values caused by solver or balancing details must be explicitly documented; do not silently alter the metric's definition.

### 6.4 Diagnostic amplification ratio: \(A\)

\[
A=\frac{S}{\max(S_0,\varepsilon)}
\]

where \(\varepsilon\) is a small positive floor used to avoid division by zero. \(A\) is diagnostic only. It is **not** the primary optimization objective.

### 6.5 Additional result fields

Where available, a cascade result should record:

- final severity \(S\);
- initial severity \(S_0\);
- cascade-induced loss \(C\);
- diagnostic ratio \(A\);
- cascade rounds;
- tripped branches by round;
- islands and balancing outcomes;
- solver and termination status;
- AC convergence status and any documented uncertainty interval;
- model fidelity (`dc` or `ac`);
- flags for exceptional conditions; and
- the grid/configuration/code hashes needed to reproduce the result.

Do not invent values for these fields when the simulation has not run.

---

## 7. System overview

The intended architecture separates the power-system model from the search algorithms and from the resource model.

1. **Grid twin:** loads a network and its base operating point, validates topology and parameters, and records data provenance.
2. **Cascade engine:** applies initiating outages, identifies islands, balances generation and load, solves flows, trips overloaded branches, and repeats according to the documented rules.
3. **Severity layer:** computes \(S\), \(S_0\), \(C\), and diagnostic \(A\).
4. **Oracle interface:** exposes a consistent severity and high-severity predicate to search algorithms. It may be backed by live evaluation or a cached truth table.
5. **Classical search:** enumerates or searches candidates using documented baselines.
6. **Quantum search:** implements toy circuits and reduced-space search dynamics under the chosen cardinality encoding.
7. **Resource model:** consumes measured calibration data and explicit parameters to estimate logical/physical resource requirements and crossover conditions.
8. **Experiments:** runs configured experiments, stores machine-readable outputs, and produces figures/tables from recorded results.
9. **API and frontend:** exposes precomputed or permitted live results to the existing dashboard without changing the dashboard's design.

The oracle interface is the key boundary: search implementations should not depend directly on the internals of a particular DC or AC solver. The resource model should consume measured JSON and declared parameters rather than importing the grid simulator.

---

## 8. Repository architecture

The implementation can use the existing frontend structure while organizing Python backend modules in a dedicated directory. The V2 architecture names the following logical components:

```text
repository/
├── app/                    # Existing frontend routes; preserve UI/UX
├── components/             # Existing frontend components; preserve UI/UX
├── public/                 # Existing static assets
├── lib/                    # Existing frontend utilities
├── backend/
│   ├── app/                # FastAPI entry point and route modules
│   ├── gridtwin/           # Grid model, data, DC/AC flow, cascade, severity
│   ├── oracle/             # Stable evaluator interface and caches
│   ├── classical/          # Exhaustive and structured classical baselines
│   ├── qsearch/            # Quantum circuits, emulation, Grover/BBHT/DH, QAOA
│   ├── resource/           # Resource model and crossover calculations
│   ├── experiments/        # E0–E16 experiment drivers/configurations
│   ├── tests/              # Unit, integration, and validation tests
│   ├── configs/            # Versioned experiment and model settings
│   ├── data/               # Raw, processed, and synthetic data
│   ├── results/            # Generated machine-readable outputs
│   └── docs/               # Technical documentation
├── README.md
└── ...
```

The actual directory names in the repository may differ during scaffolding. If so, document the actual paths and maintain clear module boundaries rather than claiming nonexistent paths exist.

### Dependency boundaries

- The grid/cascade layer must not import quantum search modules.
- Classical and quantum search should depend on the common oracle interface rather than on solver internals.
- The resource model should depend on measured calibration outputs and explicit parameters, not on the grid simulator.
- The API should call well-defined application services rather than duplicate scientific logic.
- The frontend should remain independent from Python internals and communicate only through documented API contracts or static result artifacts.

Where practical, enforce these boundaries through automated import checks and tests.

---

## 9. Grid digital twin and data provenance

### 9.1 Benchmark systems

The V2 design identifies IEEE 14-, 30-, and 118-bus systems as benchmark networks. A network file must be loaded from a documented source, and its conversion into the internal representation must be reproducible.

### 9.2 Data categories

- **Raw data:** files acquired from a named source, kept unchanged where licensing permits.
- **Processed data:** converted and normalized representations used by the engine.
- **Synthetic data:** generated or altered values, including synthetic branch ratings.
- **Results:** outputs produced by specific experiment configurations.

Each data asset should record its origin, license or usage conditions, retrieval date where applicable, conversion procedure, version/hash, and whether values are synthetic.

### 9.3 Branch ratings

The V2 design uses synthetic, N-1-secure thermal ratings for its digital-twin plan. Synthetic ratings are a modeling choice, not evidence of actual utility limits. The precise rating formula and its parameters must be taken from the V2 specification and stored in configuration. Any deviations must be explicitly documented.

Never label synthetic ratings as official, measured, or utility-provided ratings.

### 9.4 Base operating point

The model must document how generation, demand, slack/reference buses, branch parameters, and any stress factor are established. Any redispatch or stress procedure must be deterministic under a fixed configuration and version.

### 9.5 Validation

Before evaluating large outage sets, validate:

- expected bus and branch counts;
- unique and consistent identifiers;
- valid branch endpoints;
- electrical parameter ranges;
- generation and demand consistency;
- base-case solver status;
- reference/slack-bus handling;
- topology connectivity; and
- provenance and hashes.

The V2 verification plan requires toy grids, hand-solved cases, and cross-checking against an independent power-system tool where available. Do not claim validation until the relevant tests have actually been run and their outputs are stored.

---

## 10. Cascade simulation methodology

The intended cascade is a deterministic quasi-steady-state sequence, not a dynamic simulation.

For each initial outage candidate:

1. Copy or construct the configured base network state.
2. Remove the selected \(k\) initiating branches.
3. Identify connected components/islands.
4. Apply the documented generation/load balancing policy within each island.
5. Compute power flows using the selected fidelity.
6. Compare branch flows with the configured branch ratings and trip factor.
7. Identify overloaded branches.
8. Trip branches according to the configured trip policy.
9. Recompute topology, islanding, balancing, and flows.
10. Continue until no further eligible overload trips occur, a defined termination condition is reached, or a configured maximum-round limit is hit.
11. Record final status and metrics.

### 10.1 Determinism

Given identical grid data, initial outage, rating parameters, cascade configuration, solver settings, and software version, the model should produce reproducible results within declared numerical tolerances.

### 10.2 Islanding and balancing

Island balancing is a major modeling assumption. The policy must specify how generation deficits, surplus generation, load shedding, and islands without viable generation are handled. These choices can affect \(S_0\), later flows, and the final ranking. Record the policy in configuration and in every result artifact.

### 10.3 Overload trips

The trip rule must define the comparison against ratings, whether all overloaded branches trip simultaneously or according to another rule, and how borderline numerical cases are handled. Do not silently change from one trip policy to another between methods.

### 10.4 Termination

Record why a cascade stopped: no eligible overloads, maximum rounds, solver failure, AC non-convergence, or another explicitly defined condition. A failed run must not be mislabeled as a normal cascade termination.

### 10.5 Result frames

If the dashboard shows round-by-round frames, those frames must come from actual stored simulation states or be clearly marked as illustrative. A timer that advances through predetermined rounds is not a cascade simulation.

---

## 11. DC and AC model fidelity

### 11.1 DC model

The DC model is intended for exhaustive screening and for the search predicate. It uses a linearized active-power flow approximation. Its assumptions and limitations must be documented, including the treatment of voltage magnitudes, reactive power, and losses.

### 11.2 AC model

The AC model is intended for higher-fidelity static verification of selected candidates. It must record solver status and non-convergence. An AC solution is not automatically a complete model of a real cascade, because the cascade itself remains quasi-steady-state and omits detailed dynamics and protection timing.

### 11.3 Fidelity ladder

A responsible workflow uses the DC model to screen candidates and the AC model to assess selected candidates. It should quantify ranking agreement and false negatives rather than assuming the DC ranking transfers perfectly to AC.

Where AC results do not converge, report the count and handling policy. If an interval or uncertainty convention is used for AC non-convergence, define it and apply it consistently.

---

## 12. Classical search and baselines

The project should compare quantum-search formulations with meaningful classical baselines under a fair protocol.

The V2 architecture discusses:

- exhaustive enumeration;
- random search;
- hill climbing;
- beam search;
- simulated annealing;
- genetic algorithms;
- LODF-based candidate screening/pools;
- machine-learning screening, if implemented and properly evaluated; and
- MILP or other optimization approaches where the formulation supports them.

These methods do not all provide the same guarantee. Exhaustive enumeration can certify a maximum over the evaluated candidate space if all candidates are evaluated correctly. Heuristics typically return the best candidate found within a stated budget, not a guaranteed global maximum.

### Fair comparison rules

- Use the same grid, outage cardinality, ratings, cascade configuration, and severity objective.
- Report unique expensive oracle evaluations separately from internal search iterations.
- Report runtime and evaluation budget.
- Use declared random seeds and multiple runs for stochastic methods.
- Report mean, median, percentile, and uncertainty summaries where appropriate.
- Distinguish best-found results from certified results.
- Avoid tuning a baseline on the evaluation set without documenting the procedure.
- Report failed or timed-out runs.
- Include hardware, software versions, worker counts, and parallelism.

Do not declare one method superior before running the comparison.

---

## 13. Quantum search formulation

### 13.1 Constrained search space

The target space contains only exactly-\(k\) outage sets. The V2 design considers Dicke-state and ranked-index encodings. The chosen encoding, its register size, state-preparation procedure, and mapping from quantum states to outage sets must be documented.

### 13.2 Grover-style amplitude amplification

For a black-box predicate over \(N\) candidates with \(M\) marked candidates, ideal amplitude amplification has query complexity on the order of

\[
\Theta\!\left(\sqrt{\frac{N}{M}}\right)
\]

under the relevant assumptions, compared with \(\Theta(N/M)\) evaluations for unstructured classical search. The exact constants and stopping strategy depend on the algorithm and setup.

This is a statement about query complexity. It does not include the full cost of constructing and executing a cascade oracle, error correction, data movement, state preparation, measurement, classical baselines, or practical hardware limitations.

### 13.3 BBHT-style search

BBHT-style search is relevant when the number of marked candidates is unknown. Its implementation should document the iteration schedule, randomization, stopping conditions, seeds, and evaluation accounting.

### 13.4 Dürr–Høyer maximum finding

Dürr–Høyer-style search can be used to investigate maximum finding under a comparison or threshold oracle formulation. The exact algorithm variant, initialization, stopping condition, and success probability must be stated. Discovery calls and certified-stop calls should be accounted for separately where relevant.

### 13.5 Top-\(T\) outputs

If the project returns several high-severity candidates, define whether it is finding a top-\(T\) set, repeatedly excluding prior candidates, or using another procedure. Specify tie handling and avoid presenting an approximate top-\(T\) list as a certified ranking unless all required comparisons were performed.

### 13.6 Oracle boundary

The oracle should provide consistent operations such as single-candidate severity, batched severity, high-severity predicate, fidelity identification, and a counter for unique expensive evaluations. Search algorithms should not reimplement the cascade.

---

## 14. Three-tier quantum evidence model

The V2 specification separates three kinds of work. They must not be conflated.

### Tier A — Toy circuit demonstration

Construct small instances where state preparation, oracle action, reflection, and measurement can be inspected and checked. The V2 plan includes Dicke preparation, phase-oracle construction, and reflection about the valid-cardinality state on toy search spaces, with ideal and noise-model simulation on Qiskit Aer.

Report the actual circuit size, candidate-space size, marked-state count, noise assumptions, depth, gate counts, measurement shots, and measured probabilities. Only claim that a circuit was executed on Aer after the run actually occurred.

### Tier B — Exact classical emulation

At larger candidate-space sizes, idealized Grover/Dürr–Høyer dynamics can be emulated in a reduced/class-collapsed representation to obtain query-call statistics. This is an exact classical emulation of the idealized algorithmic dynamics under the stated model, not a quantum hardware run and not a coherent circuit over the entire IEEE-scale oracle.

The README and results must label this work `[EMULATED]`.

### Tier C — Fault-tolerant resource design

The IEEE-scale oracle is a design and resource-estimation exercise. It may use component-level costs calibrated against a toy reversible micro-oracle, plus explicit assumptions about logical gates, clock time, error correction, and physical overhead.

Label these outputs `[DESIGN-STAGE]` or `[ESTIMATED]`. Do not claim that an IEEE-scale reversible cascade oracle was synthesized or executed unless it actually was.

### Reversible micro-oracle

A small reversible micro-oracle can be used to test the reversible construction and count gates such as Toffoli gates. Its validity must be checked exhaustively over the toy basis states. Its cost is calibration evidence for the modeled components; it is not proof that the complete IEEE-scale oracle is feasible.

---

## 15. QAOA comparison

QAOA is a separate exploratory approach in the V2 plan. It uses an explicit quadratic surrogate for a problem whose true cascade severity can be discontinuous and non-quadratic.

The implementation must document:

- the exact surrogate objective;
- how its coefficients are derived or fitted;
- the cardinality-constraint method;
- circuit depth \(p\);
- optimizer and stopping settings;
- shot count and seed;
- constraints and penalty choices;
- comparison against the true cascade severity; and
- the surrogate gap.

A high score on the surrogate does not automatically imply high severity under the real cascade objective. The gap between surrogate score and true severity is itself an evaluation target. Do not call a QAOA output the global optimum unless the optimization and certification procedure actually establishes that result.

---

## 16. Resource estimation and crossover analysis

The resource model should estimate when a theoretical reduction in oracle queries could become a wall-clock advantage, taking account of the cost of a reversible oracle and classical alternatives.

The V2 architecture identifies a component-level model and crossover analysis using explicit parameters such as:

- classical cascade evaluation time;
- quantum oracle cost;
- reversible gate counts;
- logical clock assumptions;
- physical/logical overhead;
- classical parallelism;
- effective classical scaling exponent;
- candidate-space size \(N\); and
- the calibration factor or measured component costs used by the model.

The model should consume recorded measurement JSON and explicit parameters. It should not import the grid simulator directly or silently treat estimates as measured data.

For every crossover plot, record its configuration and the origin of each parameter. Include sensitivity analyses over uncertain assumptions. If no plausible crossover occurs in the explored range, report that outcome.

**Do not claim quantum advantage.** The defensible question is under what assumptions a query reduction might become a wall-clock advantage. The V2 design explicitly states that no quantum advantage is demonstrated.

---

## 17. Experiment plan E0–E16

The V2 specification defines experiments E0–E16. The exact protocols and parameters in the PDF are authoritative. The following is a tracking summary, not a substitute for those protocols. The experiment plan's expected outcomes are hypotheses, not results.

| ID | Experiment | Purpose / core output | Priority in V2 |
|---|---|---|---|
| E0 | Simulator validation | Validate toy-grid flow, base cases, N-1 cases, and hand-solved cascades | Must |
| E1 | Runtime profile | Measure DC/AC evaluation time and runtime percentiles on benchmark grids | Must |
| E2 | Cascade phenomenology | Characterize severity distribution, cascade rounds/trips, cascade-induced loss, and non-monotonicity | Must |
| E3 | DC–AC agreement | Measure ranking/label agreement and false negatives between DC screening and AC verification | Must |
| E4 | Oracle and circuit equivalence | Verify Dicke preparation, reflection, phase oracle, and micro-oracle against exact references | Must |
| E5 | Grover dynamics, ideal and noisy | Compare measured marked-state probability with theory and inspect noise/depth effects | Should; ideal validation is must |
| E6 | GAS/Dürr–Høyer scaling | Measure query-call distributions and fit scaling on experiment tables | Must |
| E7 | Classical comparison | Compare amplitude-amplification emulation against classical baselines under a fair protocol | Must |
| E8 | Consult V2 experiment table | Follow the exact V2 protocol; do not infer a definition from the ID alone | Per V2 |
| E9 | Consult V2 experiment table | Follow the exact V2 protocol; do not infer a definition from the ID alone | Per V2 |
| E10 | QAOA surrogate gap | Compare quadratic surrogate optimization with true cascade severity | Per V2 |
| E11 | Rating sensitivity | Test whether findings depend on synthetic rating assumptions | Per V2 |
| E12 | Consult V2 experiment table | Follow the exact V2 protocol; do not infer a definition from the ID alone | Per V2 |
| E13 | Consult V2 experiment table | Follow the exact V2 protocol; do not infer a definition from the ID alone | Per V2 |
| E14 | Resource/crossover analysis | Explore conditions under which query reduction might change wall-clock comparison | Must for crossover question |
| E15 | Resource/crossover analysis | Follow the exact V2 protocol and sensitivity design | Must for crossover question |
| E16 | Consult V2 experiment table | Follow the exact V2 protocol; do not infer a definition from the ID alone | Per V2 |

**Important:** This summary intentionally does not invent the exact titles of E8, E9, E12, E13, or E16. Before execution or reporting, transcribe the full experiment name, method, metrics, expected hypothesis, failure interpretation, and priority from the relevant V2 table into versioned experiment configurations.

For every experiment, store:

- experiment ID and name;
- configuration file and configuration hash;
- grid/data hash;
- code version or Git commit;
- Python and dependency versions;
- random seed(s);
- hardware and execution environment;
- method and solver fidelity;
- candidate count and evaluation budget;
- measured metrics and units;
- failures and exclusions;
- result file path; and
- evidence label.

An experiment is not complete because a configuration file exists. It is complete only when it has run and produced reviewable outputs. Expected outcomes must remain labelled as hypotheses until measured.

---

## 18. Verification and testing

Verification should proceed from small cases to larger benchmarks.

### 18.1 Unit tests

Test deterministic and independently checkable behaviors such as:

- grid parsing and validation;
- branch-index mapping;
- outage cardinality and uniqueness;
- topology/island detection;
- balancing policy edge cases;
- power-flow equations on small systems;
- overload identification and trip policy;
- termination conditions;
- severity metrics and zero-\(S_0\) behavior;
- candidate enumeration and ranking;
- caching keys and invalidation;
- quantum state preparation and oracle action on toy spaces;
- resource arithmetic and unit conversion; and
- API input validation.

### 18.2 Integration tests

Test the end-to-end cascade pipeline on small grids and compare with hand calculations or an independent implementation where available. Confirm that DC and AC modes are clearly separated. Test API response schemas and error states.

### 18.3 Quantum verification

Compare circuit probabilities with exact classical state-vector or basis-state references for small cases. Verify the oracle's marked-state convention, reflection operator, valid-cardinality subspace, and circuit equivalence. State numerical tolerances explicitly.

### 18.4 Reproducibility tests

For fixed seeds and configuration, ensure outputs are reproducible within declared tolerances. Confirm that result artifacts contain hashes and environment metadata.

### 18.5 Claims lint

The V2 design calls for a claims lint (Test R4) that scans the README, PDF, and deck for unsupported phrases. A repository check should flag claims such as “quantum advantage,” “blackout prediction,” “accurate,” or “validated” unless the wording is permitted by the V2 policy and backed by the required evidence.

### 18.6 Never fake test results

Do not create tests that pass by returning hardcoded expected outputs while the implementation is missing. Do not report tests as passed unless they were executed. A placeholder test should be marked as a placeholder and should not be counted as validation.

---

## 19. API and frontend integration

The backend API is intended to expose model outputs to the existing frontend. The frontend design is frozen for the scaffolding stage: do not redesign or restyle it just to accommodate backend work.

The V2 design proposes endpoints including:

| Endpoint | Intended purpose | Expected data source |
|---|---|---|
| `GET /grids` | List supported grids | Metadata/precomputed data |
| `GET /grid/{id}` | Grid topology and base loading | Metadata/precomputed data |
| `POST /cascade` | Evaluate or retrieve a cascade for a specified outage set | Cached/precomputed results; permitted live evaluation for supported smaller grids |
| Search/ranking endpoint(s) | Return ranked candidates and evaluation metadata | Search service or stored results |
| Crossover/resource endpoint(s) | Return resource-model outputs | Versioned estimate artifacts |

The final route list must match the implementation and the V2 API section. Do not advertise endpoints that do not exist. If a minimal health endpoint is implemented for scaffolding, document it separately from scientific endpoints.

### API requirements

- Validate grid IDs and branch indices.
- Validate that exactly \(k\) distinct branches were provided.
- Return structured errors for invalid inputs, unsupported configurations, solver failures, and missing artifacts.
- Include model fidelity and configuration identity in results.
- Avoid blocking ordinary health checks with expensive computations.
- Use timeouts and explicit budgets for long-running searches.
- Distinguish a live calculation from a cached/precomputed response.
- Never expose a fabricated value as if it came from the engine.

### Frontend integrity

The existing frontend's colors, layout, typography, topology illustration, charts, animations, cards, and controls must remain unchanged unless the user explicitly authorizes UI changes. Backend integration should happen through a documented API boundary in a later task.

If a dashboard element currently uses mock data, retain it only with an honest status label or document that it remains illustrative. A visual animation is not evidence of a running cascade engine.

---

## 20. Installation and development setup

The commands below are templates. Verify that the actual files and dependencies exist before claiming that these commands work. The frontend and Python backend are separate development environments.

### 20.1 Python environment — Windows PowerShell

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, follow your machine's approved execution-policy procedure or invoke the virtual environment's Python executable directly. Do not change machine-wide security settings casually.

### 20.2 Python environment — Linux/macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 20.3 Dependencies

Keep baseline dependencies minimal. FastAPI and an ASGI server are sufficient for a basic health endpoint. Scientific dependencies should be added when their corresponding modules are implemented and tested. Potential later dependencies include NumPy/SciPy, a power-system analysis library, Qiskit/Aer, and plotting or experiment utilities, but the README must not imply these are installed unless they are listed in the actual dependency files.

Keep `requirements.txt` and `pyproject.toml` consistent. Pin versions for reproducible experiments once the dependency set is established.

### 20.4 Frontend setup

Use the repository's existing package manager and lockfile. For example, if the repository uses pnpm:

```bash
pnpm install
pnpm run dev
```

Do not regenerate the frontend lockfile merely to create backend scaffolding. Confirm the actual package scripts before publishing commands as verified.

---

## 21. Running the project

### 21.1 Current scaffold

At the scaffolding stage, the only backend behavior that may be considered operational is a minimal API startup and health check, if implemented and tested. All grid, cascade, search, quantum, and resource features must remain marked as not implemented until the real code exists.

A typical FastAPI launch command, if the module and app object match, is:

```bash
uvicorn app.main:app --reload
```

Run it from the `backend/` directory when `backend/app/main.py` defines the ASGI application named `app` and the dependencies are installed. If the actual import path differs, document the correct command instead.

If FastAPI's automatic docs are enabled, they are typically available at `/docs` on the local server. Only document this as available after verifying the application.

### 21.2 Planned scientific workflow

Once the relevant code has been implemented, the intended workflow is:

1. Validate environment and dependencies.
2. Load the selected grid and provenance metadata.
3. Validate the base operating point.
4. Run small-grid validation cases.
5. Run the selected cascade mode.
6. Compute severity metrics.
7. Generate or retrieve candidate results.
8. Run AC verification for selected DC-screened candidates.
9. Execute quantum toy-circuit experiments and/or exact emulation.
10. Run resource/crossover calculations.
11. Store versioned artifacts.
12. Serve only verified results through the API and frontend.

These steps are a roadmap, not a claim that a command for every step currently exists.

---

## 22. Configuration and reproducibility

Keep model and experiment settings in versioned configuration files rather than scattering constants through source code.

The V2 document gives an illustrative configuration with values such as:

- grid: `ieee118`;
- outage cardinality \(k=3\);
- a proportional rating family;
- stress factor \(\lambda=1.10\);
- cascade maximum rounds of 30;
- default cascade mode `dc`;
- severity threshold \(\tau=0.20\);
- quantum encoding `binary_dicke`;
- BBHT parameter \(\lambda_{\mathrm{BBHT}}=1.2\); and
- resource-model assumptions for gate time, cost factors, and core counts.

These are **design parameters from V2**, not proof of a completed run or universal defaults. Preserve the precise names, meanings, units, and values from the full V2 configuration section. If a project configuration changes, record the change and its rationale.

Each experiment should record a configuration hash. Cache keys for truth tables or candidate results should include at least the grid hash, configuration hash, and code version. Changing the data, rating model, cascade rules, or code must invalidate incompatible cached results.

Use explicit random seeds for stochastic methods. Avoid relying on implicit global random state.

Do not commit `.env` secrets, virtual environments, caches, or large generated artifacts unless the project explicitly requires them. Keep `.env.example` safe and free of credentials.

---

## 23. Results, artifacts, and reporting

All scientific claims should be reproducible from scripts and recorded configurations.

A result artifact should include, where applicable:

```json
{
  "experiment_id": "E0",
  "status": "NOT_RUN",
  "evidence_label": "[PROPOSED]",
  "grid_id": "toy-grid",
  "grid_hash": null,
  "config_hash": null,
  "code_version": null,
  "seed": null,
  "method": null,
  "fidelity": null,
  "metrics": {},
  "environment": {},
  "notes": "Placeholder schema only; not an experimental result."
}
```

This example is a schema illustration, not an actual measurement. Do not store it in a way that could be mistaken for a completed experiment.

Prefer machine-readable JSON/CSV plus scripts that regenerate plots and tables. Figures shown in the presentation should be produced from the recorded artifacts rather than manually typed numbers. Keep raw outputs separate from processed summaries.

Every reported runtime should state the hardware, software, grid, \(k\), fidelity, candidate/evaluation budget, and whether the number is a mean, median, percentile, estimate, or single run.

---

## 24. Evidence labels

Use the V2 labels wherever a statement could be mistaken for a result.

| Label | Meaning |
|---|---|
| `[IMPLEMENTED]` | Code exists in the repository, is covered by tests, and can be run by a reviewer. |
| `[MEASURED]` | A number produced by an experiment script in the repository, with its configuration hash recorded. |
| `[SIMULATED]` | Produced by running a model of a physical device, such as a noise model, on a classical computer. |
| `[EMULATED]` | Exact classical computation of the dynamics an ideal quantum algorithm would follow; not a quantum runtime. |
| `[DESIGN-STAGE]` | A specification or value derived from formulas and stated placeholder parameters; no experiment has produced it. |
| `[ESTIMATED]` | An analytical resource estimate, not a synthesized circuit count unless explicitly stated. |
| `[PROPOSED]` | Planned work not yet performed. |
| `[OPTIONAL]` | Work that will be reported if completed and otherwise omitted from claims. |

A file's presence alone is insufficient for `[IMPLEMENTED]`; the feature must be runnable and tested. A result must not be labelled `[MEASURED]` without an actual experiment output and its configuration identity.

---

## 25. Claims policy

The V2 claims policy is binding. Use scoped, evidence-backed language.

| Avoid or qualify | Safer wording |
|---|---|
| “Quantum advantage” | “We estimate the conditions under which a \(\sqrt{N}\) query reduction could become a wall-clock advantage; none is demonstrated.” |
| “Grover finds the worst blackout faster” | “Amplitude amplification has approximately square-root query scaling under the stated oracle assumptions; no wall-clock claim is made.” |
| “\(\sqrt{\binom{L}{k}}\) speedup” | “\(\sqrt{\binom{L}{k}}\) query complexity; no wall-clock claim.” |
| “Blackout prediction” | “Ranking of high-severity outage sets under a quasi-steady-state cascade model.” |
| “Ground truth” for the DC reference table | “Exhaustive DC reference table”; use “AC verification” when describing the AC check. |
| “Realistic cascade” | “Quasi-steady-state overload cascade without dynamics, protection timing, or operator action.” |
| “Real-world deployment” | “The oracle interface is designed to accept other network models; operational use would require utility data and validation.” |
| “Validated” | Use only after the stated cross-checks and experiment have been completed; name the checks and measured agreement. |
| “Optimized” | Prefer “searched for the highest-severity set” unless the optimization guarantee is established. |
| “Accurate” | Report the measured error values and comparison method. |
| “Solves” | Prefer “searches” or “identifies under this model.” |
| “Demonstrates” | Use only for implemented items; use “emulates” for Tier B and “estimates” for Tier C. |
| “Practical” | Avoid unless practical feasibility is established; discuss measured crossover conditions instead. |
| “Circuits executed on Aer” | Safe only after execution; state search-space size and noise model. |
| “Tier B emulates idealized Grover exactly” | Use only when the actual Tier B emulation matches the specified idealized dynamics. |
| “Classical wins on IEEE grids” | Treat as a hypothesis until E7 measures it. |

No result should be described as a quantum advantage merely because the theoretical query count is smaller. No real-grid claim should be made from synthetic ratings without explicit qualification. No experiment should be described as complete before its script runs and artifacts exist.

---

## 26. Limitations and threats to validity

### 26.1 Static model limitation

A quasi-steady-state overload cascade is not a dynamic power-system simulation. It does not reproduce transient stability, frequency dynamics, detailed relay timing, or operator intervention.

### 26.2 DC approximation

DC power flow is useful for screening but omits aspects of AC behavior, including reactive power, voltage magnitudes, and losses. Ranking fidelity must be measured rather than assumed.

### 26.3 Synthetic ratings

Synthetic branch ratings can strongly influence overloads and cascade behavior. Sensitivity experiments are required to understand whether findings depend on the chosen rating rule.

### 26.4 Island balancing

Different balancing and load-shedding policies can produce different values of \(S_0\), \(S\), and \(C\). The policy is part of the model and must be versioned.

### 26.5 Solver non-convergence

Non-convergence is a meaningful outcome and must be reported. Silently discarding failed cases can bias rankings.

### 26.6 Search bias

Heuristics can miss high-severity candidates. A best-found candidate is not automatically a certified maximum. Fair comparisons require comparable budgets and transparent accounting.

### 26.7 Quantum resource assumptions

Fault-tolerant resource estimates depend on reversible oracle design, logical gate counts, error-correction overhead, clock assumptions, and data encoding. Estimates should include sensitivity analyses and uncertainty rather than false precision.

### 26.8 Query complexity versus runtime

A query-complexity improvement does not automatically imply a runtime improvement. Oracle construction and execution can dominate the cost, and classical methods can exploit structure that an unstructured-search comparison ignores.

### 26.9 UI and illustrative data

A frontend may display mock metrics, sample rankings, or illustrative network geometry. Such elements must not be cited as experimental evidence. A visually polished dashboard does not validate the underlying engine.

---

## 27. Security and responsible use

- Do not connect this demonstration to live utility control systems.
- Do not expose operational network credentials or confidential grid data.
- Validate API inputs and limit computationally expensive requests.
- Record the provenance and license of external data.
- Avoid publishing unsupported claims about real infrastructure vulnerability.
- Label synthetic and illustrative data visibly.
- Treat results as outputs of the stated model, not instructions for operating or attacking a real network.
- Do not include secrets in the repository or experiment artifacts.

---

## 28. Development roadmap

The order below follows the V2 architecture and validation dependencies.

### Phase 1 — Repository foundation

- Preserve the existing frontend.
- Add backend package structure, configuration, dependency files, tests, and documentation.
- Establish minimal application startup and health checks.
- Confirm that no UI files were changed.

### Phase 2 — Grid model and validation

- Implement data loading and provenance metadata.
- Add branch-index mapping and topology checks.
- Implement synthetic rating configuration exactly as specified.
- Validate toy cases and benchmark base operating points.

### Phase 3 — Cascade engine

- Implement DC flow and islanding/balancing.
- Implement overload detection, tripping, termination, and result frames.
- Implement severity metrics.
- Validate on hand-solved cases before larger experiments.

### Phase 4 — AC verification

- Add AC static power-flow and cascade verification.
- Record convergence status.
- Run DC–AC fidelity experiments.

### Phase 5 — Oracle and classical baselines

- Define a stable oracle interface and cache keys.
- Implement exhaustive search for tractable spaces.
- Implement and benchmark the selected structured baselines.
- Record evaluation counts and runtime.

### Phase 6 — Quantum components

- Implement and verify toy state preparation and oracle circuits.
- Run ideal and noise-model experiments.
- Add exact classical emulation for the explicitly supported reduced-space formulation.
- Implement the reversible micro-oracle at toy scale.

### Phase 7 — Resource and QAOA studies

- Build the resource model from calibrated measurements.
- Add crossover and sensitivity analyses.
- Implement the QAOA surrogate experiment and measure its gap to true severity.

### Phase 8 — Experiments and reporting

- Execute E0–E16 according to the full V2 experiment table.
- Generate artifacts and figures from scripts.
- Add claims lint and reproducibility checks.
- Clearly mark any experiment that remains incomplete.

### Phase 9 — API and frontend integration

- Add endpoints only after their service-layer behavior exists.
- Prefer precomputed results where appropriate.
- Integrate through API contracts without changing the frontend design unless explicitly authorized.
- Ensure that mock and live states are clearly distinguished.

---

## 29. Contribution workflow

1. Read the V2 specification before changing model definitions.
2. Create a focused change in one layer at a time.
3. Add or update tests with the implementation.
4. Run the relevant tests and record the command and result.
5. Keep grid simulation, search, resource estimation, API, and UI responsibilities separate.
6. Do not embed experiment outputs directly in source code as hardcoded results.
7. Add a configuration file for new experiments.
8. Save machine-readable output and environment metadata.
9. Regenerate figures from scripts.
10. Update documentation and the implementation-status ledger.
11. Review all public claims against the claims policy.
12. Preserve the frontend's existing UI/UX unless a change is explicitly requested.

---

## 30. Troubleshooting

### Dependency installation fails

Check the Python version, virtual environment, package-manager output, and platform compatibility. Do not resolve conflicts by silently installing arbitrary latest versions. Pin and document tested versions.

### API module cannot be imported

Run the command from the documented working directory and verify the package path and ASGI object name. Ensure package files exist and the command matches the repository structure.

### Grid file is missing

Do not substitute an undocumented dataset. Follow the data README, verify the source and license, and record the file hash and conversion procedure.

### DC and AC rankings differ

This may reflect model fidelity rather than a software bug. Verify solver setup and compare cases systematically. Report the ranking disagreement and false negatives instead of hiding them.

### Cascade never terminates

Check the overload-trip rule, topology updates, repeated trips, solver failures, and maximum-round condition. Record termination status and prevent silent infinite loops.

### Quantum probabilities differ from theory

Check the state preparation, valid-cardinality subspace, phase-oracle sign convention, reflection operator, number of marked states, iteration count, and noise settings. Compare with exact small-instance references.

### Results cannot be reproduced

Check configuration and data hashes, random seeds, dependency versions, solver versions, parallelism, and cached outputs. Ensure caches are keyed by the grid, configuration, and code version.

### Dashboard values look real but the engine is missing

Treat them as illustrative/mock data. Do not infer scientific functionality from the presence of charts, animations, export buttons, or a topology view.

---

## 31. Glossary

- **AC power flow:** Nonlinear alternating-current power-flow calculation that includes voltage magnitude and reactive-power behavior.
- **Amplitude amplification:** Quantum algorithmic framework that increases the probability of measuring marked states under specified oracle assumptions.
- **Base operating point:** The documented starting network state, including generation, demand, and electrical parameters.
- **Branch:** A transmission line or transformer represented as an edge in the network.
- **Cascade:** A sequence of overload-driven branch trips and subsequent network re-evaluations.
- **Candidate outage set:** A set of exactly \(k\) initiating branch outages.
- **DC power flow:** Linearized active-power flow approximation used for screening in this project.
- **Dicke state:** A superposition over bitstrings with a fixed Hamming weight, relevant to exactly-\(k\) encodings.
- **Dürr–Høyer search:** A quantum maximum/minimum-finding approach based on repeated search/comparison.
- **False negative:** A high-severity candidate under the verification criterion that is missed by the screening criterion.
- **Hamming weight:** Number of set bits in a bitstring.
- **Marked candidate:** A candidate satisfying the predicate used by a search algorithm.
- **Oracle:** A common interface that evaluates candidate severity or a predicate over candidates.
- **Quasi-steady-state:** A model that repeatedly solves static operating states between discrete trips rather than simulating fast physical dynamics.
- **\(S\):** Final unserved-load fraction.
- **\(S_0\):** Initial unserved-load fraction before overload-driven cascade trips.
- **\(C\):** Cascade-induced loss, \(S-S_0\).
- **\(A\):** Diagnostic ratio \(S/\max(S_0,\varepsilon)\).
- **Tier A:** Toy-scale quantum circuit demonstration.
- **Tier B:** Exact classical emulation of idealized quantum-search dynamics.
- **Tier C:** Fault-tolerant oracle and resource design/estimation.
- **Synthetic rating:** A rating generated by a documented rule rather than supplied as an actual utility rating.

---

## 32. References and source of truth

The primary technical source is:

- **Grid Doomsday Finder — Solution Design & Architecture V2.0**, Q-Hack India 2026, Track 04. This document supersedes V1 and defines the problem formulation, model assumptions, severity metrics, quantum-search approach, tier definitions, experiment plan E0–E16, software architecture, and claims policy.

Where this README summarizes the design, the full V2 PDF is authoritative. If a detail is not stated here or cannot be confirmed in the repository, consult the relevant V2 section rather than guessing.

External benchmark datasets and software libraries must be cited in the implementation documentation with their actual versions, licenses, and source details. Do not add invented references.

---

## 33. Current implementation status

**This table must be edited to match the actual repository and real verification results. Do not leave a component marked implemented just because a file exists.**

| Component | Initial scaffold status | Evidence required to mark implemented |
|---|---|---|
| Existing frontend | Present in repository; scientific outputs may still be mock/illustrative | Build verification and inspection of actual data flow |
| Backend package structure | Scaffolded when files exist | File inventory |
| Minimal API health endpoint | Not implemented until verified | Successful startup and HTTP response |
| Grid loading | Not implemented until coded | Loader tests and benchmark file provenance |
| Base operating point | Not implemented until coded | Base-case solver output and validation tests |
| DC power flow | Not implemented until coded | Hand-solved and independent cross-check tests |
| Island detection/balancing | Not implemented until coded | Edge-case tests and documented policy |
| Cascade engine | Not implemented until coded | Reproducible end-to-end cascade tests |
| Severity metrics | Not implemented until coded | Tests for \(S\), \(S_0\), \(C\), and \(A\) |
| AC verification | Not implemented until coded | AC solver tests and convergence reporting |
| Classical baselines | Not implemented until coded | Executed benchmark artifacts and fair budget accounting |
| Quantum toy circuits | Not implemented until coded | Circuit runs and exact small-instance verification |
| Tier B emulation | Not implemented until coded | Emulation outputs and equivalence tests |
| Reversible micro-oracle | Not implemented until coded | Exhaustive toy basis-state verification and gate counts |
| QAOA surrogate | Not implemented until coded | Executed experiment and surrogate-gap results |
| Resource/crossover model | Not implemented until coded | Versioned inputs, calibration, calculations, and plots |
| Experiments E0–E16 | Not run until artifacts exist | Per-experiment scripts, configurations, logs, and results |
| API scientific endpoints | Not implemented until verified | Endpoint tests and actual response behavior |
| Frontend/backend integration | Not implemented until verified | API-driven result path without unintended UI changes |
| Quantum advantage | **Not demonstrated** | Must not be claimed without relevant measured evidence |

### Final project principle

The purpose of Grid Doomsday Finder is not to assume that quantum search wins. It is to build a reproducible, model-scoped benchmark that separates cascade severity, classical search, quantum query complexity, circuit-level evidence, emulation, and fault-tolerant resource estimates. The credibility of the project depends on keeping those categories distinct and reporting measured outcomes honestly.
