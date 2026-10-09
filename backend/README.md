# Grid Doomsday Finder Backend

## Purpose

This directory is the backend scaffold for the Grid Doomsday Finder research prototype. It is intentionally separated from the existing Next.js frontend. The backend currently provides only a minimal FastAPI health endpoint; all grid simulation, search, quantum, experiment, and data workflows are design-stage scaffolding and must not be interpreted as validated results.

## Authoritative specification

`Grid_Doomsday_Finder_Solution_Design_V2.pdf` is the technical source of truth. The implementation plan is to identify a transmission network, enumerate exactly-k outages, replay a deterministic quasi-steady-state cascade, score severity, and compare classical search with resource-estimation tiers for quantum methods. The equations, evidence labels, severity definitions, quantum tiers, and E0–E16 experiment plan below are preserved as research requirements, not completed claims.

## Scope and evidence labels

- **IMPLEMENTED:** module or endpoint exists as a starter scaffold.
- **DESIGN-STAGE:** architecture or algorithm has been described but not validated.
- **PROPOSED:** future method or experiment design.
- **EMULATED:** a classical simulation of a quantum-inspired or quantum algorithm, not a quantum execution.
- **ESTIMATED:** analytical resource estimate, not a measured runtime or speedup.
- **NOT IMPLEMENTED:** no production behavior exists.

No real utility case, blackout forecast, AC-fidelity claim, quantum advantage, or experimental result is included in this repository.

## Layout

- `app/`: future FastAPI application and domain packages.
- `tests/`: backend tests; currently only scaffold tests are expected.
- `data/`: input case documentation; no utility data is bundled.
- `results/`: result provenance and storage conventions.
- `scripts/`: reproducibility and conversion scripts (not implemented).
- `docs/`: architecture, methodology, API, experiments, quantum approach, limitations, and evidence policy.

## Local setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
curl http://localhost:8000/health
```

The expected health response is `{"status":"ok"}`. The frontend is deliberately not connected to this service.

## Technical workflow (planned)

1. Load a documented network case and validate bus, branch, generator, load, and rating data.
2. Solve the base case and reject invalid or non-converged inputs.
3. Enumerate exactly-k outage sets without duplicates.
4. Recompute DC or AC flow, detect islanding, balance load and generation, and remove overloaded elements according to the specified deterministic rule.
5. Repeat cascade rounds until stable or the stopping rule fires.
6. Calculate the severity vector and scalar score, retaining the complete trace.
7. Rank candidates and compare against the frozen classical baselines.
8. Report quantum tiers as emulation or analytical estimates until hardware and circuit evidence exist.

## Equations and definitions to preserve

The planned DC model uses the reduced nodal equation

`B_red theta = P_net`, with `P_net = P_gen - P_load` and branch flow `F_ij = b_ij (theta_i - theta_j)`.

The overload ratio is `rho_l = |F_l| / F_l^max`. An element is overloaded only under the threshold and persistence rule specified by V2; the exact constants must be read from the PDF and recorded in a versioned configuration rather than silently changed in code.

The severity definition is the V2 multi-component score: served-load loss, overload exposure, islanding/blackout impact, and cascade extent, with normalization and weights treated as specification parameters. A result must include the component vector, scalar score, thresholds, and trace. A scalar without provenance is invalid evidence.

## Quantum tiers

- **Tier A:** oracle/search formulation and circuit-resource accounting only; PROPOSED.
- **Tier B:** simulator or emulation comparison against exact classical search; EMULATED.
- **Tier C:** hardware execution with noise, calibration, shot counts, and reproducible circuits; NOT IMPLEMENTED.
- **Tier D:** end-to-end crossover analysis including data loading and verification overhead; ESTIMATED/PROPOSED.

## E0–E16 experiment plan

The frozen plan is tracked as follows: E0 environment and provenance; E1 case validation; E2 base-case solve; E3 single-outage sanity checks; E4 exactly-k enumeration; E5 cascade determinism; E6 severity calibration; E7 exhaustive baseline; E8 classical candidate ranking; E9 search scaling; E10 oracle encoding; E11 Grover emulation; E12 Dürr–Høyer minimum-finding emulation; E13 QAOA formulation; E14 resource estimation; E15 noise/hardware sensitivity; E16 final crossover and evidence audit. None of these experiments is claimed complete by this scaffold.

## Development policy

Keep inputs, configuration, code version, and outputs tied by a manifest. Never overwrite raw inputs. Never report a design-stage estimate as an observation. Add tests before implementing scientific behavior. See `docs/CLAIMS_AND_EVIDENCE.md` and `docs/LIMITATIONS.md`.

## Status

The only required working feature is `GET /health`. Everything else is intentionally a minimal starter module or documentation placeholder.
