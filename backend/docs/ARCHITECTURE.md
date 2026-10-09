# Architecture

The backend is a layered research scaffold. The API layer will accept validated requests and return versioned response schemas. Grid loading and network validation will own case provenance. Simulation will contain base-case flow, island balancing, cascade replay, ratings, and severity. Search will own exact enumeration and classical baselines. Quantum will own formulation, emulation, and resource estimates without claiming hardware execution. Experiments will orchestrate manifests and immutable result artifacts.

## Boundaries

`app/api` must not implement power-flow mathematics. `app/simulation` must receive typed network data and deterministic configuration. `app/search` must treat the simulator as a pure evaluator. `app/quantum` must be explicit about EMULATED and ESTIMATED evidence. `app/experiments` must record code version, case checksum, configuration, seed, and evidence label.

## Runtime

FastAPI is the thin HTTP boundary. A future deployment may run behind a reverse proxy, but this scaffold has no authentication, persistence, queue, or frontend integration. The health endpoint is the only working route.

## Reproducibility

Every result should be traceable to an input manifest, solver configuration, outage set, deterministic seed where applicable, and software revision. Raw case files and generated results belong outside source control unless explicitly approved.
