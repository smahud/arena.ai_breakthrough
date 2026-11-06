# Phase 9 — Follow-up Research Report (continuation session)

**When:** 2026-11-06T14:51–14:55Z (same day, new user turn "Lanjutkan").

## Scope

Executed the two highest-value items from `report/final-summary.md` §7: (1) batch-size vs
timing study to resolve H-1; (2) transient-fault class to probe L-5, with a minimal
evidence-gated extension of the reference implementation.

## Actions & outcomes

1. **GitHub connector re-checked** (statuses can change per reply): still `unsupported`
   (14:51:31Z). Delivery mode unchanged: local repo + runbook.
2. **EXP-08 (new):** interval-timestamp method (design pre-registered threats to validity).
   Verdict: **batched bash calls execute sequentially with ~0.13 s pipelined handoffs**;
   T8/T4 span scaling 1.74 vs parallel-predicted 1.0. H-1 RESOLVED → F-16.
3. **Corrections issued** (contract rule 2 / directive §2E): F-01 amended, EXP-02 RESULTS
   addendum, architecture-analysis §6, README headline, ARCHITECTURE.md executor note. The
   study's earlier "INFERRED-likely parallel" reading was *wrong* and is now labeled refuted —
   this is the contract's contradiction-handling rule exercised on the study's own findings.
4. **EXP-09 (new):** deterministic flaky model → current policy gap confirmed (FAILED@1) →
   minimal extension `Task.blind_retries` (default 0 = semantics preserved) → recovery DONE@2
   with `blind_retry` trace event → 3 new tests → **44/44 green**, pipeline OK → F-17.
5. **Hygiene:** 15 phantom-deleted tracked `.pyc` files untracked; root cause documented
   (snapshot exclusions vs git index across sessions) as an F-12 extension.

## Verification at close of phase

`pytest tests/` 44 passed exit 0 · `benchmarks/run_suite.py` RESULT: OK exit 0 ·
C-1 audit unaffected (extension is stdlib-only, no new imports).

## Deviations

None from contract; one prior conclusion revised by new evidence (item 3) — the intended
behavior of an evidence-driven process, logged rather than silently edited.

## Incident log (this session)

- **Commit blocked: `Author identity unknown` (exit 128).** Root cause: the platform excludes
  `.git/config` from cross-message snapshots (credential-path policy), so the repo-local
  identity configured in session 1 was gone in session 2. Fix: identity set in the persistent
  `~/.gitconfig` (workspace file, not an excluded path) + repo-local re-set. Recorded as
  **F-18** in findings.md: *environment state that lives in excluded paths must be
  re-established (or made persistent outside them) at the start of every session; validation
  pipelines should include a commit-readiness check.*
- 15 phantom-deleted tracked `.pyc` files (same root-cause family: snapshot exclusions vs git
  index) — untracked this session (item 5 above).
