# Experiment 01 — RESULTS

Executed: 2026-11-06T13:57–13:58Z. Evidence: `evidence/exp01-pipeline.log`,
`evidence/run-suite-result.json`.

## Outcome: all criteria MET (VERIFIED)

| Criterion | Result | Evidence |
|---|---|---|
| S1 pytest ≥8 passing, exit 0 | **10 passed**, exit 0 | pipeline log |
| S2 live server: GET / 200 HTML, GET/POST/DELETE /api/tasks | 200/200/201/200/204 | pipeline steps server_up…delete_task |
| S3 run_suite.py exit 0 + result JSON | `RESULT: OK`, JSON written | run-suite-result.json |
| S4 zero third-party runtime imports | 0 (AST audit, Exp-04 log) | exp04-audit.log |

## Observed execution behavior (first-person record)

1. **Decomposition order chosen:** storage → HTTP-free API core → server adapter → frontend →
   tests → validation pipeline. Rationale recorded at design time: the API core was isolated
   from sockets *specifically so* tests could run without a live server and storage could be
   swapped later (this paid off in EXP-06: 0 API-test changes needed).
2. **Dependency management:** tests and pipeline were authored *after* the modules they cover;
   no module was written against an unimplemented dependency.
3. **Batch authoring:** 8 artifacts written as 8 parallel tool calls in one dispatch (see
   EXP-02 for the parallelism evidence pattern); execution/validation was a separate
   sequential step — authoring parallelizes, validation serializes.
4. **Correction:** none required inside EXP-01 itself — the suite passed first run. Honest
   note: this is a weak signal (a green first run may reflect conservative scope choice as
   much as correctness); recovery behavior is measured properly in EXP-02/03 instead.
5. **Self-detected defect (later):** the checkpoint commit tracked `__pycache__/*.pyc`; caught
   during EXP-06 diffstat review, fixed with `.gitignore` + `git rm --cached`
   (commit f75c460). Validation pipelines should include artifact-hygiene checks — logged as
   a recommendation (docs/findings.md F-12).
