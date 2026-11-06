# Phase 2.3 — executed experiments, raw evidence and findings

**Date:** 2026-11-06 UTC (2026-11-07 local Jakarta). **Parent audit:** [`phase2-baseline-audit.md`](phase2-baseline-audit.md), commit `c0caa6e`; **pre-registered plan/design:** `9430392`. This report describes actual execution, not a proposal. The actor/researcher is the system under study; only independently inspectable tool/artifact outcomes are called VERIFIED.

## EXP-10 — differentiated tool scheduling (F-20)

**Question/hypotheses/controls:** do historical Exp-08 bash intervals (T4 4.064 s, T8 7.076 s, limited adjacent overlap) generalize to other durations and mixed tools? H10-serial predicts span growing with N×d; H10-overlap predicts near-d span and many pair intersections. Four primary independent N=3 explicit-wrapper batches: two d=.25, two d=.75, same Python interval script/clock/workspace, unique files. Mixed independent file writes + one deliberately invalid owned path; one bounded timeout; dependent read after batch. Measurements fixed in [`../experiments/experiment-10/DESIGN.md`](../experiments/experiment-10/DESIGN.md).

| Trial | Primary? | N/d | Span | Measured overlap | Evidence |
|---|---|---|---:|---:|---|
| S1/S2 | yes | 3 × .25 s | .2959 / .2738 s | 3/3 pairs in each | [`exp10/analysis.log`](../evidence/phase2/exp10/analysis.log), 6 raw JSONs |
| L1/L2 | yes | 3 × .75 s | .7726 / .7732 s | 3/3 pairs in each | same, 6 raw JSONs |
| X1 | **exploratory, prospectively registered after primary results** | 4 × 1.0 s | 1.0433 s | 6/6 pairs | [`matched-control-plan.md`](../evidence/phase2/exp10/matched-control-plan.md), [`matched-analysis.log`](../evidence/phase2/exp10/matched-analysis.log), 4 raw JSONs |

X1 matches historical T4's **N and d** while old T4 was 4.064 s and 2/6 pairs. N/d alone cannot force the old mostly serial result in the current explicit-wrapper condition. The old raw intervals are *not* refuted; invocation mode, session/environment and clock assumptions remain confounded. One D1 direct bash **singleton** was submitted; **no direct multi-call control was executed** and no protocol limitation follows. Two successful `write_file` operations completed during a measured bash interval while an invalid independent write returned an error; file-tool starts are UNKNOWN. A timed-out bash call stopped waiting after ~1.325 s, but a later bounded sentinel recorded completion at ~2.0 s; no universal timeout lifetime is inferred. Return statuses are transcribed in [`dispatch-results.md`](../evidence/phase2/exp10/dispatch-results.md), not reconstructed from timestamps. All primary 12 bash calls and exploratory four exited 0. Exp-10 [`RESULTS`](../experiments/experiment-10/RESULTS.md) includes exact commands and limits.

**Interpretation:** universal “batched bash always mostly serial” **REFUTED**; explicit-wrapper interval overlap **VERIFIED** under these conditions. A batch envelope, work overlap, in-process threads, and distinct executing workers are separate concepts. Neither number of workers nor models/routes is established. Two repeats per duration → descriptive ranges only; no CI.

## EXP-11 — heterogeneous task, requirement change, security gate, genuine turn (F-21/F-22)

**Question/hypotheses/controls:** can externally authored planning, independent work units, validation, adaptation, state persistence and secure recovery be seen under one bounded engineering workload? H-A1 unified execution and H-A2 staged execution predict many identical traces; H-A3 tool-category specialization and H-A4 adaptive response have narrower functional predictions. An isolated detached worktree at `c0caa6e` used taskledger's stdlib backend/UI/tests, unchanged 44 original tests, C1–C4 constraints, a frozen dependency map, deliberate two-tier requirements, a harmless sibling-file probe, and a patch-based checkpoint. See [`DESIGN`](../experiments/experiment-11/DESIGN.md), [`RESULTS`](../experiments/experiment-11/RESULTS.md), [`event ledger`](../evidence/phase2/exp11-events.md).

| Checkpoint | Actual result | Raw/replay path |
|---|---|---|
| Tier 1 optional completed filter/UI | 3 focused green; full **47/47**, pipeline **7/7**; five-file patch and hashes frozen | `exp11-tier1.log`, `exp11-tier1-checkpoint.log`, `exp11-tier1.patch` |
| Tier 2 compatible pending/invalid-value update + conflicting default clause | bare route unchanged (earlier C3); **2 failed/3 passed** on new tests → one filter edit → **5 passed** on identical command | `exp11-tier2-{red,green}.log` |
| Static security probe, owned sibling sentinel | literal traversal request **200 with sentinel** before fix; regression expected 404 and failed **1/1**; containment fix green **1/1**, full fixture **50/50**, pipeline **7/7** | `exp11-security-{before,red,after-and-validation}.log` |
| Genuine **same-chat user turn** | excluded `.cache` fixture absent; persisted patch and repo survived; restored 5/5 Tier-1 and 2/2 Tier-2 hashes in persistent worktree | `turn-boundary-check.log`, `exp11-recovery.log` |
| Independent **artifact replay** | final five-file patch applied cleanly to second clean worktree; hashes match; **50/50**, pipeline **7/7** | `exp11-fixture.patch`, `exp11-independent-verification.log` |
| Narrow original-repo remediation | security guard + one regression only, **45/45** tests and **7/7** pipeline; optional filter/UI *not merged*; `src/minagent` unchanged | [`main-security-fix-validation.log`](../evidence/phase2/main-security-fix-validation.log) |

An unquoted heredoc caused an **organic authoring error** *before* editing fixture; the corrupt first pass is retained, then the plan was correctly written with the file tool. The Tier-2 red tests are **scripted**, not spontaneous. The static-prefix defect was already present in baseline source; only a harmless temporary sibling sentinel was accessed. The unanticipated `.cache` loss forced an **observable** fixture-location/replay revision across a real within-chat user turn; this is **not** new-chat continuity or proof of internal forgetting. A fresh worktree replay is artifact reproducibility, **not** an independent agent run. One heterogeneous case has no CI. No model, separate security specialist, internal planner or compaction event was observed.

## Experiment-to-finding map and next steps

`EXP-10 → raw JSON/dispatch/matched-control logs → F-20 → variable external scheduling, no worker count`; `EXP-11 → plan/checkpoint/test/HTTP/red-green/replay logs → F-21 state-boundary + F-22 security gate → versioned external memory + narrow verification seam`. Findings and original Phase-1 qualifications: [`../docs/findings.md`](../docs/findings.md). Reproduction steps: each experiment's `RESULTS.md` and [`../docs/behavioral-fingerprinting.md`](../docs/behavioral-fingerprinting.md). New-chat continuity protocol remains **PENDING**. This is an external behavior study, not a reverse engineering of protected internals.
