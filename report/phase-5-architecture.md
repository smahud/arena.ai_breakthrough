# Phase 5 — Architecture Reconstruction Report

**When:** 2026-11-06T14:10Z. **Artifacts:** `reference-architecture/ARCHITECTURE.md`,
`reference-architecture/JUSTIFICATIONS.md`.

## What was produced
A functional reference architecture with 8 components (Planner, Executor, ToolRegistry +
adapters, RecoveryPolicy, Validator, StateStore, TraceReporter, AgentLoop termination rule),
each mapped to the evidence that justifies it, plus an explicit **deliberate-absences list**
(no message bus, no vendor SDK, no rollback engine, no delegation layer) with the finding or
limitation that vetoed each (contract rule 3 audit trail).

## Key reconstruction choices and their basis
1. **ToolResult telemetry shape** (output, exit_code, duration_ms, command) mirrors exactly
   what was observable about tool results in this environment (F-13) — not an idealized schema.
2. **False-green guard in Validator** — direct encoding of F-03/F-08: exit 0 is necessary,
   never sufficient; require positive markers, forbid known false-green strings.
3. **Recovery = classify(exit code + error text) → repair → re-run**, no blind retries —
   the F-02 loop shape; validated again organically in Phase 6 (see phase-6 report).
4. **Parallel dispatch of dependency-free tasks, serialized validation** — F-01/F-15 +
   observed authoring/validation split.
5. **A2 (explicit planner) chosen for inspectability**, with the honest note that A1/A3 fit
   the evidence equally (architecture-analysis §5) — the implementation claims functional
   equivalence to observations, not fidelity to unknowable internals.

## Deviations
None from Phase 4 conclusions; no component added without a JUSTIFICATIONS row.
