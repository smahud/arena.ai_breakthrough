# Experiment 03 — RESULTS

Executed: 2026-11-06T14:01:42–43Z. Evidence: `evidence/exp03-faults.log` (all runs, including
failures, preserved verbatim). Faulty+fixed artifacts: `experiments/experiment-03/faults/`.

## Fault ledger (all VERIFIED against the log)

| Fault | Class | First run | Diagnosis quote (literal from log) | Fix | Re-run |
|---|---|---|---|---|---|
| F1 `f1_faulty.py` | compile-time | exit 1 | `SyntaxError: expected ':'` (line 1, caret at `def area(w, h)`) | 1 line (add `:`) | exit 0, `area(3,4)=12` |
| F2 `f2_paginate.py` | logic/test-time | exit 1, `1 failed, 2 passed` | `FAILED faults/test_f2.py::test_remainder - assert 2 == 3` | 1 line (`//` → ceiling idiom) | `3 passed`, exit 0 |
| F3a missing binary | runtime/env | exit **127** | `definitely-not-a-real-tool-xyz: command not found` | n/a — diagnosed as environment, not code | n/a |
| F3b `f3_partial.py` | runtime + partial state | exit 1 | `FileNotFoundError: [Errno 2] … '/nonwritable-root/step3.txt'` | 1 line (path) | exit 0; `step0..3.txt` present |

## Criteria

S1 MET (three nonzero first-run exits preserved). S2 MET (every diagnosis quotes log text).
S3 MET (each failure followed by same-command success). S4 MET (every fix = 1 line; ≤5 target).

## Observed recovery-loop shape

`execute → capture(stderr+exit code) → localize (error text names file/line/symbol) → minimal
patch → re-execute same command → verify exit 0`. Latency: one tool call per recovery in all
three cases.

## Additional observations

- **Partial-state handling (F3b):** the crashed run left `step0-2.txt` on disk. The fixed
  re-run was idempotent (overwrote steps 0–2, added step3). No explicit rollback was needed
  *because the operation was naturally idempotent* — recorded as a design lesson, not a
  demonstrated rollback capability. A non-idempotent variant (e.g., appends) would have
  required cleanup-first; not tested → UNKNOWN for that class.
- Exit-code semantics were informative across classes: 1 (Python fatal), 127 (shell: command
  not found), pytest exit 1 (tests failed). Recovery keyed on the code+text pair.
- Honesty note per DESIGN: faults were scripted; what is evidenced is the loop's shape and
  latency, not spontaneous error discovery.
