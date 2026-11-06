# Experiment 08 — Batch Parallelism Overlap (resolves H-1)

**Objective (RQ2, H-1):** Determine whether N independent tool calls dispatched in one
assistant message execute with true wall-clock overlap or are serialized by the platform.
F-01 established batched dispatch returns N independent results; overlap itself was INFERRED
because per-call `duration_ms` cannot discriminate (each call reports its own duration either
way).

**Method — interval intersection, not durations:** each bash call in a batch records its own
start/end epochs (`date +%s.%N`) around a fixed `sleep 1`, writing to a per-call file
(no write contention). Post-hoc analysis computes, per trial:
- `span = max(end) − min(start)`
- pairwise interval overlap count
- platform-reported `duration_ms` per call (secondary signal)

**Trials:**
- T4: one batch of 4 calls, each `sleep 1`.
- T8: one batch of 8 calls, each `sleep 1`.
- Tseq (control): one call performing 4 sequential `sleep 1`s (expected span ≈ 4 s).

**Predictions:**
- If parallel: span(T4) ≈ span(T8) ≈ 1.0–1.6 s; all intervals mutually overlapping.
- If sequential: span(TN) ≈ N seconds; disjoint intervals.

**Measurable success criteria:**
- S1: all interval files present and well-formed (2 floats each).
- S2: span and overlap matrix computed and preserved in `evidence/h1-analysis.log`.
- S3: H-1 in `docs/findings.md` updated to the verdict the data supports (VERIFIED-parallel,
  VERIFIED-sequential, or still-UNKNOWN if data is ambiguous), with the raw numbers quoted.

**Threats to validity (pre-registered):** clock is shared (same sandbox) → intervals are
comparable; scheduling jitter may add a few hundred ms; `duration_ms` includes platform
overhead and is used only as a secondary signal.
