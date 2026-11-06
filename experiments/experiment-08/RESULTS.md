# Experiment 08 — RESULTS (H-1 resolution)

Executed: 2026-11-06T14:51:59–14:52:57Z. Evidence: `evidence/h1/A*.txt`, `B*.txt`, `Cseq.txt`
(raw epoch intervals), `evidence/h1-analysis.log` (computed spans/overlaps).

## Data (VERIFIED)

| Trial | n | Span | Overlapping pairs | Pattern |
|---|---|---|---|---|
| T4 (batch of 4, `sleep 1` each) | 4 | **4.064 s** | 2/6 (adjacent only: 0.095 s, 0.052 s) | staggered sequential |
| T8 (batch of 8) | 8 | **7.076 s** | 7/28 (adjacent only: ~0.125–0.144 s each) | staggered sequential |
| Tseq control (1 call, 4 sequential sleeps) | 4 | 4.018 s | 0/6 (gaps ~0.002 s) | in-call sequential |

Scaling T8/T4 = **1.74** (parallel predicts ≈1.0; sequential predicts ≈2.0; the shortfall from
2.0 is exactly the pipelined handoff: each call starts ~0.13 s before its predecessor ends).
Platform `duration_ms` was ~1.06 s for **every** batched call in both trials — confirming the
design premise that per-call durations cannot discriminate execution mode.

## Verdict

**H-1 RESOLVED: batched tool calls in this environment execute SEQUENTIALLY with pipelined
handoffs (~0.13 s boundary overlap), not in wall-clock parallel.** The batch economy is real
but comes from eliminating model↔platform round-trips (one generation step dispatches N calls),
not from concurrent sandbox execution.

## Corrections issued (contract rule 2; directive §2E "previous result contradicts new
evidence")

1. `docs/findings.md` F-01: "wall-clock overlap INFERRED (likely)" → **refuted**; new F-16
   records the measured behavior.
2. `experiments/experiment-02/RESULTS.md` interpretation 1: corrected via addendum (streams
   A/B/C ran sequentially inside their batch; conclusions about decomposition/isolation stand —
   only the concurrency characterization changed).
3. `docs/architecture-analysis.md` §6: H-1 marked resolved.
4. `README.md` headline 1 reworded.
5. `reference-architecture/ARCHITECTURE.md`: note added distinguishing platform-level batch
   serialization (F-16) from minagent's in-process ThreadPoolExecutor parallelism, which is
   real and measured (3×0.25 s sleeps in <0.6 s wall, `test_independent_tasks_run_concurrently_F01`
   — the reference implementation runs *inside one* platform call, so F-16 does not constrain it).

## Criteria

S1 MET (24 well-formed interval records). S2 MET (analysis log preserved with per-pair
overlaps). S3 MET (verdict + raw numbers entered into findings; corrections propagated).

## Residual uncertainty

- Only `bash` calls were interval-instrumented; whether `write_file` batches serialize the same
  way is UNKNOWN (no clock access from that tool). Behavior may be environment-specific
  (single-sandbox worker); a multi-worker platform could differ — generalization INFERRED at best.
- The ~0.13 s handoff mechanism (container reuse, process teardown overlap) is not observable
  from inside: UNKNOWN.

## Phase 2 interval re-analysis (2026-11-06; original verdict preserved)

The raw T4/T8 intervals themselves show **2/6 and 7/28 pairwise overlaps**, respectively;
strict “sequential execution” / “one worker” is therefore stronger than the data. For these
bash trials, intervals were **mostly serial with short real adjacent overlap**, and all-at-once
execution is REFUTED. Worker count and the reason for overlap are **UNKNOWN**. The original
Exp-02 streams did not have raw per-stream epochs; Exp-08 cannot establish their exact order.
Independent arithmetic: `evidence/phase2/baseline-evidence-crosscheck.log` (F-16 revised).
