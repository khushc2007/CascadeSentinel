# API

The current service exposes only `GET /health`, returning `{\"status\":\"ok\"}`. All simulation and search routes are reserved and intentionally absent. Future routes must use versioned schemas, reject unknown case identifiers, validate exactly-k constraints, and return evidence labels with every scientific field.

A planned route may accept a case reference, outage cardinality, solver configuration, and experiment manifest. It should return the candidate outage set, base-case status, cascade trace, severity vector, scalar score, provenance, and implementation/evidence status. No route may imply that a toy case is a utility prediction.
