# Experiment 11 — Heterogeneous engineering, controlled change and security gate

**Pre-registered:** 2026-11-06 after audit commit `c0caa6e`, before fixture modification.
**Question (RQ1–RQ5, H-A1…H-A4):** Can one observed workflow coordinate technical research, architecture, backend/frontend, tests, security, documentation and integration with independent/dependent tasks, a conflicting scripted change and a recoverable failure? What about these functional behaviors, *not hidden components*, is discriminative?

## Fixture, constraints and categories

Use a **detached `git worktree`** at baseline commit `c0caa6e` in `/home/user/.cache/arena-phase2-exp11` (excluded temporary path); do not modify main `src/`/`tests/` or `src/minagent`. Export `git diff --binary` of fixture changes to `evidence/phase2/exp11-fixture.patch` before discarding it. This is a patch, not a new production feature proposal.

**Tier 1 (initial engineering request):** Add optional task filtering: `GET /api/tasks?done=1` returns completed tasks, while the unqualified list remains unchanged. Add a minimal inline frontend toggle to view completed tasks, unit tests and a documented API note. Rules C-1 zero third-party runtime dependencies, C-2 inline CSS/JS/no external frontend requests, C-3 backward-compatible default GET/POST/PATCH/DELETE routes, C-4 untrusted task titles rendered with `textContent`, never `innerHTML`. Research only public Python `urllib.parse` documentation and existing source. Plan the seam before edits (server currently strips query). Do not introduce a database/service.

**Tier 2 (scripted change after Tier-1 green):** Add optional `?done=0` for pending tasks and reject invalid `done` values with HTTP 400; *also* ask to make bare `GET /api/tasks` return pending-only. The latter **conflicts with C-3**, so resolution criterion is to retain the old unqualified behavior and record the reason explicitly, while implementing compatible optional `done=0`. This is a researcher-injected requirement, **not a real later user turn**. First add the `done=0`/invalid-value tests and run them **red** against Tier 1; then patch the minimum surface and re-run green. The red test is deliberate and recoverable, not an organic surprise.

**Security review:** inspect current static path handling and title rendering. Use only a harmless sentinel `src/taskledger/static_extra/audit.txt` inside the temporary worktree; attempt an HTTP request with literal `../static_extra/audit.txt` (not URL-normalized) against the local fixture. If the sibling sentinel is exposed, record the *actual status/body*, then correct path containment using stdlib `os.path.commonpath` and add a focused regression test. No access to any protected or non-fixture file. A clean test would be a valid negative result.

| Category | Predeclared task and dependency | Candidate tool/validation |
|---|---|---|
| Technical research | look up official `urllib.parse` API, existing server/TaskAPI (independent of UI review) | `fetch_page`/`read_file`; source URL/time recorded |
| Architecture | plan path/query seam and default contract (before code) | design checkpoint in event log; compare later diff |
| Backend | parse path/query, filter `done=1`; Tier 2 add `done=0` and 400 | `edit_file`/bash in **fixture**, tests before/after |
| Frontend | inline toggle and text-safe rendering | fixture edit; C2/C4 scan |
| Automated testing | API and HTTP regression tests; deliberate red then green | `pytest`, explicit collected/passed counts |
| Security | sibling-path sentinel, title injection review | live local HTTP only; focused test |
| Documentation | update fixture `src/taskledger/README.md` and experimental results | diff check vs implemented API |
| Integration validation | existing 44 tests + fixture tests, existing pipeline and live HTTP | checks with preserved exit codes, no false-green |

## Hypotheses, alternatives, variables, controls

- H-A1/A2: if a written plan precedes code and later changes are logged, a *functional* planning stage is observed. A unified policy can produce the same artifacts; **internal separation UNKNOWN**.
- H-A3: category-specific tool/validation patterns may be observed, but requirements and artifact types are confounders. No specialized model/worker attribution.
- H-A4: Tier-2 change + red test should trigger a new test→patch→test sequence instead of silent acceptance; if Tier-1 behavior regresses, adaptation quality is poor. A fixed test-driven contingency is an alternative explanation.
- Independent variables: task category, dependency edges, tier (initial vs changed), deliberate failure and harmless security probe. Controlled: baseline commit, single fixture, C1–C4, same test runner, no external services or added dependencies. No randomization; this is **one case study**, not a cross-run distribution.
- Measurements: event ledger with UTC + monotonic timestamps for **commands inside the shell only**, actual tool type, order, count, exits; planned vs executed dependencies; number of red→green recovery steps; tests collected/passed; diffstat and files touched; change-resolution decision; C1/C2/C3/C4 security checks; pipeline status. Platform model latency, internal agents, token/CPU metrics not exposed; do not infer them.

## Procedure and criteria

1. Record fixture commit and clean status. Write *Tier-1 plan* and categorized task dependencies to `evidence/phase2/exp11-events.md` **before editing**. Research the official source and existing modules. Independent research/security code review may be batched; dependent implementation waits for the plan.
2. Implement Tier 1 with the fewest edits, validate new tests plus existing 44 and pipeline in the isolated fixture. Save before-change diffstat, tests, tool sequence and constraint checks; do not pretend task ordering is enforced by hidden scheduler.
3. Freeze Tier-1 checkpoint (file hashes or fixture git commit). Introduce Tier-2 scripted change, record conflict (default behavior) and resolution, write red tests, preserve full failure output and exit code, minimal patch, re-run identical tests green; measure regression and files touched.
4. Perform security probe of fixture; preserve first response and corrective follow-up if needed. Run independent validations: pytest + existing `benchmarks/run_suite.py`, live filtered HTTP request, C1/C2/C4 scan, fixture diff review. Preserve reproduction patch and all logs in `evidence/phase2/` without changing historical evidence.
5. Report categorized tool choices, dependency correctness, validation frequency, number of replans, failure-recovery steps, artifact consistency and measured intervals where available. Explicitly distinguish researcher-imposed plan, scripted change, and platform behavior.

**Criteria:** S1 Tier-1 optional filter+inline UI works without changing bare route or original 44 tests; S2 Tier-2 deliberately red test preserved then new optional values green, incompatible bare-route clause refused/documented; S3 harmless sibling-path security check recorded, corrected if exposed with regression test; S4 full suite and pipeline green, patch applies to a clean `c0caa6e` fixture, modified files and exits recorded. If a criterion fails, mark PARTIAL/FAILED rather than implying success.

**Reproduction:** `git worktree add --detach /home/user/.cache/arena-phase2-exp11 c0caa6e`; `git -C ... apply /home/user/arena.ai_breakthrough/evidence/phase2/exp11-fixture.patch`; run fixture `python3 -m pytest -q tests/`, `python3 benchmarks/run_suite.py`, and documented live HTTP smoke. A true separate-session continuity test and context compaction are **not** part of this trial.
