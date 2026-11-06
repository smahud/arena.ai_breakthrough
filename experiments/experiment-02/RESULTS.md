# Experiment 02 — RESULTS

Executed: 2026-11-06T13:55–13:56Z. Evidence: `evidence/exp02-stream-{a,b,c}.log`,
`evidence/exp02-stream-b-fix.log`, `evidence/exp02-integration.log`.

## Observations (all VERIFIED unless noted)

1. **Parallel dispatch:** Three independent `bash` tool calls were issued in a single assistant
   message and returned three independent results (durations 637 ms, 380 ms, 468 ms). The
   platform accepted and executed the batch as one round-trip. → Concurrent *tool-level*
   execution of independent units is directly observable. (Whether the three shells overlapped
   in wall-clock time is not measurable from the returned data — marked INFERRED-likely.)
2. **Unplanned genuine failure in Stream B:** test asserted `avg_word_len == 3.0`; actual 2.67
   (chars 5+2+1=8, /3). Log quote: `{'avg_word_len': 2.67} != {'avg_word_len': 3.0}`.
   Recovery: single-line `sed` fix of the *expectation* (the implementation was right), re-run
   → `3 passed`, exit 0. Time-to-recovery: one additional tool call.
3. **Measurement error found in our own harness:** `pytest | tee log; echo EXIT=$?` reported
   `STREAM_B_EXIT=0` despite pytest failing — `$?` after a pipeline is the *last* command's
   (tee) status; `pipefail` was off. Fixed by `set -o pipefail` in the recovery run. This is an
   instance of the agent's verification instrumentation being wrong and self-correcting —
   relevant to RQ3 (never trust an unvalidated success signal).
4. **Integration (sequential step):** `pipeline.py` composes the three streams via `sys.path`
   only; combined test passed (1 passed, exit 0).
5. **Independence audit (S3):** grep over stream sources shows imports of stdlib only
   (`re`; `json, os, tempfile`); no stream imported another.

## Criteria

| Criterion | Result |
|---|---|
| S1 parallel dispatch, all exit 0 | MET (after 1 recovery loop on B) |
| S2 integration test passes | MET |
| S3 no cross-stream imports | MET (audit output preserved) |
| S4 wall-clock comparison | PARTIAL — per-call durations captured; true overlap not measurable from tool results. UNKNOWN. |

## Interpretation

Independent work units decompose cleanly and can be dispatched concurrently at tool-call
granularity; integration is a separate sequential aggregation step. Coordination cost was zero
between streams (no shared state) and one pipeline step for aggregation. The dominant risk
observed was not scheduling but *validation signal integrity* (finding 3).

## ADDENDUM — correction issued 2026-11-06T14:53Z (contract rule 2)

Experiment 08 (interval-timestamp method) showed batched bash calls execute **sequentially with
~0.13 s pipelined handoffs**, not in wall-clock parallel: streams A/B/C ran one after another
inside their batch. The phrase "dispatched concurrently" above is correct only at the
*dispatch* level (one round-trip, three independent results); the execution-overlap reading
("INFERRED-likely" in observation 1, PARTIAL/UNKNOWN in S4) is hereby **resolved as refuted** —
see F-16 and `experiments/experiment-08/RESULTS.md`. Conclusions about decomposition, failure
isolation (F-15 — which does not depend on overlap: B's failure surfaced in its own result
either way), and aggregation are unaffected.
