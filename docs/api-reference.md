# API reference

Run `uvicorn grid_doomsday.api.main:app --app-dir backend/src --reload`.

- `GET /health` returns service status.
- `GET /grids/toy` returns topology metadata.
- `POST /cascade` with `{case, outages, trip_multiplier}` returns replayable rounds and severity metrics.
- `POST /search` with `{case, k, max_candidates}` performs a bounded deterministic search and labels output `EMULATED`.
- `GET /resource/crossover?candidates=1000` returns an analytical `ESTIMATED` model, not a benchmark.

IEEE cases are intentionally not bundled in this prototype; adding a pandapower adapter is a documented next step rather than silently substituting data.
