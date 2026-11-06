# Experiment 01 — Complex Software Delivery

**Objective (RQ1, RQ3):** Deliver a small but complete application — backend, frontend,
automated tests, documentation, validation pipeline — and observe planning, decomposition,
testing, and correction behavior end-to-end.

**Deliverable:** `taskledger`, a zero-dependency task ledger:
- Backend: Python `http.server`-based JSON REST API (`src/taskledger/`) with a storage layer.
- Frontend: single static HTML page using only inline JS/CSS (sandbox preview constraint),
  served by the same backend.
- Tests: pytest suite (`tests/test_taskledger.py`) covering API + storage.
- Docs: `src/taskledger/README.md`.
- Validation pipeline: `benchmarks/run_suite.py` running lint-free import check, unit tests,
  and a live server smoke test.

**Measurable success criteria:**
- S1: pytest exit code 0 with ≥8 passing tests.
- S2: live server responds 200 to `GET /` (HTML) and `GET /api/tasks` (JSON); `POST /api/tasks`
  creates a task retrievable by `GET`.
- S3: `run_suite.py` exits 0 and writes a machine-readable result JSON.
- S4: ≤0 third-party runtime imports (constraint C-1).

**Procedure:** (1) plan module breakdown; (2) implement storage → API → frontend → tests;
(3) run pytest; (4) start server as background process, curl endpoints, stop; (5) run pipeline;
(6) record all raw outputs to `evidence/exp01-*.log`.

**Observation targets:** decomposition order actually chosen, dependency handling between
modules, whether tests are written against behavior observed or assumed, correction loops.
