# Execution Lifecycle (as observed from inside one session)

Reconstructed strictly from tool-call/result traffic and artifacts (F-13 boundary applies).

## Per-turn cycle (VERIFIED shape)

1. **Interpret** — map the goal + accumulated context to candidate next actions.
2. **Dependency-check** — split candidates into independent (batchable) and dependent
   (must wait). Observed discipline: calls whose inputs depend on prior outputs are never
   batched with those priors.
3. **Dispatch** — emit the batch; platform returns one structured result per call:
   `stdout`, `stderr`, `exit_code`, `duration_ms`, plus tool-specific fields (ports, pid,
   process status, chunk info, search results).
4. **Reflect** — read results as evidence: exit codes AND content (F-03: content can
   contradict exit code; `NO TESTS RAN` with exit 0).
5. **Branch:**
   - success → advance plan; persist artifacts/evidence;
   - failure → recovery loop (F-02): localize from error text → minimal patch → re-run same
     command → verify; typically one extra call;
   - contradiction with standing constraints → arbitrate toward earlier written contract
     (F-06), log resolution.
6. **Checkpoint/Report** — git commit at meaningful boundaries; write phase/experiment reports.

## Session-level phases actually executed (this project)

Discovery (env+connector probes) → Design (7 DESIGN.md before any experiment code) →
Execution (interleaved where independent: P1 measurements ran alongside Exp-07 retrieval) →
Analysis (docs) → Architecture reconstruction → Reference implementation → Verification →
Delivery. Phase reports: `report/phase-*.md`.

## Termination behavior (VERIFIED)

Work stops when acceptance criteria are checkable-green: pipeline exit 0 + audits exit 0 +
all RESULTS criteria tables filled + delivery status resolved (published OR documented as
unavailable — here the latter, F-10). No unbounded iteration was observed; retry counts were
always exactly "until green", max 1 retry per fault in this session.

## Time profile (from platform `duration_ms`, selected)

env probe 731 ms · stream batch 637/380/468 ms · validation pipeline 1164 ms · fault suite
747 ms · CR-1 verification 2437 ms · nohup hazard 30 000 ms (timeout) · managed start 704 ms.
Total measured tool time ≈ 45 s excluding model generation time (not observable — F-13).
