# Phase 2.6 — independent artifact verification and repository integrity

**Date:** 2026-11-06T17:38 UTC. **Baseline:** [`phase2-baseline-audit.md`](phase2-baseline-audit.md) at public master `79412fd…`, audit commit `c0caa6e`, plan/design `9430392`. **This verification is independent of the fixture's first worktree, not independent of the researcher/agent/model.**

## Checks and raw logs

| Claim/check | Outcome | Preserved evidence |
|---|---|---|
| Historical baseline tests/pipeline | 44/44 and 7/7 at baseline; historical counts retained rather than rewritten | [`baseline-validation.log`](../evidence/phase2/baseline-validation.log) |
| Final **main** taskledger with only verified static-file remediation | **45/45** tests, **7/7** pipeline in a disposable copy; source diff whitespace check clean (**raw-evidence exception below**) | [`main-security-fix-validation.log`](../evidence/phase2/main-security-fix-validation.log); [`final-validation.log`](../evidence/phase2/final-validation.log) |
| Final **fixture** at base `c0caa6e` | **50/50**, **7/7** in prior independent clean-worktree patch replay; current verifier **50/50** again on that replay worktree; all five changed file hashes match first fixture | [`exp11-independent-verification.log`](../evidence/phase2/exp11-independent-verification.log), [`final-validation-retry.log`](../evidence/phase2/final-validation-retry.log) |
| Reproducible timing/fingerprint | 12 primary JSON values and 4 X1 exploratory records; raw hashes and spans match machine-readable snapshot; no D1 comparison included | `exp10/analysis.log`, `exp10/matched-analysis.log`, [`behavioral-fingerprint.json`](../evidence/phase2/behavioral-fingerprint.json), `final-validation-retry.log` |
| Links, constraints and blast radius | 20 changed/new Markdown docs checked for broken relative links (0); main `src/minagent` unchanged; optional experimental API filter/UI absent in main | `final-validation-retry.log`; compare `git diff` / fixture patch |
| Security containment | owned sibling and symlink paths blocked while index served; prior 200 and red regression retained, no protected file reads | `exp11-security-before.log`, `exp11-security-red.log`, `exp11-security-after-and-validation.log`, `tests/test_taskledger_security.py` |

**Verification harness failure, preserved (not swept away):** the first *audit script*, **not the program under test**, used a nonexistent plural filename `tests/test_taskledger_filters.py`; the actual five-file patch contains singular `tests/test_taskledger_filter.py`. The first verifier exited **1 after** main suite 45/45, disposable pipeline 7/7, and fixture suite 50/50 had already passed. The raw failure remains in `final-validation.log`; a narrow corrected verifier in `final-validation-retry.log` matched **five/five** hashes, fingerprint digests/values and 20/20 link targets, and exited **0**. No evidence was fabricated or retroactively renamed. This is a small organic auditing error and demonstrates why an exit code must be attributed to the correct stage.

**Raw-evidence whitespace exception:** when first staged, `git diff --cached --check`
reported trailing whitespace / EOF-blank warnings in four **preserved raw artifacts**:
`exp11-events-first-pass.log`, `exp11-fixture.patch`, `exp11-tier1.patch`, and
`exp11-tier2-red.log`. They are original failed-authoring, generated patch and literal
pytest evidence, so their bytes were **not** rewritten to make the generic whitespace
checker green. The restricted source/test/curated-ledger check
`git diff --cached --check -- src/taskledger/server.py tests/test_taskledger_security.py experiments/experiment-11/RESULTS.md evidence/phase2/exp11-events.md`
passed, as did tests, patch digest and replay. The earlier unstaged `git diff --check`
in `final-validation.log` was green because untracked raw artifacts were not yet staged;
**do not misreport it as an all-files staged check**.

**Integrity and scope:** final fixture patch `evidence/phase2/exp11-fixture.patch` SHA-256 `b813bdeca507de692a9c5fc8e478db5cbffe02edd5c9b757c4d47eecbef08c25`, five files, 117 insertions/6 deletions, applicable to base `c0caa6e`. The experiment feature remains **fixture-only**; main contains only static guard + focused regression. Historical results (`44`, Exp-08 timing, Phase-8 publication) remain dated records. User-turn `.cache` loss was genuine within-chat continuity evidence (F-21) but genuine **new-chat** continuity remains PENDING; no model identity, hidden worker/router trace or compaction event is claimed.

**Before publication:** inspect staged diff for secrets, run final `git diff --check`/tests as needed, commit and verify local HEAD; attempt authorized, noninteractive `git push` without force or stored tokens, check anonymous remote HEAD. If publication cannot proceed, record exact failure and leave reproducible local commits. A public historical repo is not proof that these new Phase-2 commits are public.
