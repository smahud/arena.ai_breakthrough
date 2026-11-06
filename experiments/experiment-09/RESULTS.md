# Experiment 09 — RESULTS (transient faults & blind-retry policy)

Executed: 2026-11-06T14:53:37Z (before) / 14:54:15Z (after).
Evidence: `evidence/exp09-before.log`, `evidence/exp09-after.log`.

## Observed behavior

**Before (gap confirmation, S1):** flaky command (counter-file model: fails attempt 1,
succeeds attempt 2) run through `minagent` with no repair fn:
`BEFORE-CHANGE RESULT: {'flaky': 'failed'} attempts_total: 1`, trace
`tool_result(exit 1) → failure_classified(cls=runtime) → FAILED`. The F-02-derived policy
("retry only after a patch") is correct for deterministic faults but leaves transient faults
unrecoverable — exactly as predicted in DESIGN.

**After (S2):** minimal extension — `Task.blind_retries: int = 0` + one branch in `_execute`
emitting a `blind_retry` trace event. Same workload:
`AFTER-CHANGE RESULT: {'flaky': 'done'} attempts_total: 2`, trace
`tool_result(exit 1) → failure_classified → blind_retry → tool_result(exit 0) → DONE`.

## Criteria

| | Result |
|---|---|
| S1 gap recorded pre-change | MET (exp09-before.log, `GAP CONFIRMED`) |
| S2 post-change recovery w/ `blind_retry` event | MET (exp09-after.log) |
| S3 pre-existing tests pass UNMODIFIED | MET — 41 prior tests untouched; suite now **44 passed**, pipeline `RESULT: OK` |
| S4 justification row added; scope = 1 field + 1 branch | MET (JUSTIFICATIONS.md row 13; diff touches types.py, agent.py, tests only) |

## New tests (3)

`test_blind_retry_recovers_transient_fault_exp09` (DONE@2 + trace event),
`test_blind_retry_default_zero_preserves_f02` (default policy unchanged: FAILED@1),
`test_blind_retry_exhaustion_still_reports` (always-failing cmd, blind_retries=3/max=3 →
FAILED after exactly 3 attempts, 2 `blind_retry` events — bounded, never concealed).

## Interpretation

Retry policy is fault-class-dependent: deterministic faults justify patch-then-retry (F-02);
transient faults justify bounded identical re-runs. An agent architecture needs both, with the
transient budget **off by default** and always bounded + traced. This closes one L-5 gap
(transient class now tested) using an honest deterministic model of flakiness; genuinely
nondeterministic flakiness (intermittent, load-dependent) remains UNKNOWN.

## Hygiene side-fix (same window)

15 `.pyc` files tracked since checkpoint `d713a28` were untracked (`git rm --cached`): the
cross-message workspace snapshot excludes `__pycache__`, so tracked `.pyc`s reappear as
phantom deletions each session — F-12 extended: *.gitignore must cover every snapshot-excluded
directory name, and audits should run `git status` at session start.*
