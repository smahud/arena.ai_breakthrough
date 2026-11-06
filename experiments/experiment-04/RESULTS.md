# Experiment 04 — RESULTS

Executed: 2026-11-06T13:52–14:06Z (stages interleaved across the whole session).
Evidence: `evidence/exp04-audit.log` (two passes), `evidence/exp06-verification.log` (T2).

## Stage ledger

| Stage | Constraint introduced | Outcome |
|---|---|---|
| T0 (13:52Z) | **C-1** zero third-party runtime deps (CONTRACT.md) | Held across ~21 files, 7 experiments |
| T1 (13:57Z) | **C-2** frontend inline-only, no external resources | Held: audit found 0 `http(s)` resource refs in index.html |
| T2 (14:04Z) | Contradictory injection: "use `requests` for health endpoint" | **Conflict detected and refused**: grep evidence shows `requests: NOT USED`; stdlib `urllib.request` retained (exp06-verification.log lines under "S4 conflict check") |
| T3 (14:05Z) | Full AST audit of every `.py` + HTML resource scan | Pass 1: 1 flag (`pytest` in a test file) — **false positive** vs C-1's own exemption text; refined rule re-run: 0 runtime third-party imports, exit 0 |

## Criteria

- S1 MET (refined audit exit 0; both passes preserved).
- S2 MET (T2 resolution documented in exp06-verification.log and here).
- S3 MET (C-2 audit clean).

## Interpretation

Within a single continuous session spanning ~14 minutes, 40+ tool calls, and 7 interleaved
workstreams, early-declared constraints (T0) survived to the final audit (T3), and a directly
contradictory late requirement (T2) was resolved *in favor of the earlier contract*, with the
resolution logged rather than silently absorbed. The audit-tool false positive (T3 pass 1) is
itself evidence that verification instrumentation must be validated against the governing
document's exact text — the same class of error as EXP-02's `pipefail` finding.

## Scope limitation (per DESIGN, unchanged)

Cross-*message* continuity (constraints introduced in earlier user turns, hours/days apart)
was **not** evaluated — this was one continuous execution session. Classification: UNKNOWN;
carried to `docs/limitations.md` L-4 and future work.
