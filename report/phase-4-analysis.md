# Phase 4 — Analysis Report

**When:** 2026-11-06T14:07–14:10Z. **Artifacts:** `docs/findings.md` (F-01…F-15, H-1…H-4),
`docs/architecture-analysis.md`, `docs/orchestration-analysis.md`,
`docs/execution-lifecycle.md`, `docs/tool-behavior.md`, `docs/context-management.md`,
`docs/limitations.md` (L-1…L-9), `docs/public-capabilities.md`.

## Correlation work performed
- 15 findings cataloged, each with ID, RQ link, source experiment, observation,
  interpretation, alternative explanations, confidence class, reproduction pointer, residual
  uncertainty (directive §7 template).
- Cross-experiment patterns identified: the false-green family (F-03 + F-08, two independent
  instances in different subsystems) → elevated to a design rule in the reference
  implementation. The recovery-loop shape (F-02) held across scripted (Exp-03) and natural
  (F-14) failures → treated as a genuine behavioral regularity at n=4 samples.
- Architecture reconstruction kept strictly layered: observable (§1) / documented (§3) /
  inferred (§4) / alternatives (§5). Three alternative internal architectures (A1 single
  generative loop, A2 planner-executor, A3 multi-specialist) were shown to predict ALL
  observations equally — no discrimination claim made (directive §2E honored: no agents or
  models inferred from style/speed).

## Confidence distribution
VERIFIED: 14 findings · INFERRED components: 2 (wall-clock overlap; replanning representation) ·
HYPOTHESIS: 4 (H-1…H-4) · UNKNOWN: internals per L-1/L-3, cross-turn continuity per L-4.

## Deviations
None. Analysis introduced no new claims beyond the evidence ledger.
