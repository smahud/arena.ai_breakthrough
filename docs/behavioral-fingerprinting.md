# Phase 2 behavioral fingerprint (observable, not model identity)

**Purpose:** Compare *execution conditions and artifacts* across runs/sessions without asserting a proprietary model, hidden agent, worker count, or planner representation. Design fixed in [`phase2-research-plan.md`](phase2-research-plan.md); raw data in [`../evidence/phase2/`](../evidence/phase2/); compact machine-readable snapshot [`behavioral-fingerprint.json`](../evidence/phase2/behavioral-fingerprint.json), schema `phase2.behavioral-fingerprint.v1`.

## Measurement schema and denominators

| Dimension | Field / calculation | Raw source and evidence class | Missing/limitations |
|---|---|---|---|
| Planning | written task/dependency map before edit; later documented revision count; dependency violations = executed dependent tasks started before recorded prerequisites | `exp11-events.md` plus pre-change Tier-1 patch/hashes, **VERIFIED for written artifacts** | No internal plan trace; many stages have only coarse UTC, so an exact dependency-correctness fraction is **UNKNOWN** (do not invent a denominator). |
| Execution | call category, return status, per-call `duration_ms` where present; bash interval `span=max(end)-min(start)` and pairwise `min(end_i,end_j)>max(start_i,start_j)`; file-tool mtime completion only | Exp-10 raw `S1/S2/L1/L2` JSON, `analysis.log`, `dispatch-results.md`, `mixed-analysis.log` (**VERIFIED**, conditioned on comparable clocks) | File tool start, model latency, queue/worker count, cross-host clock offset UNKNOWN. Duration minus inside sleep includes launch/tool/transport, not pure platform overhead. |
| Quality | tests passed / tests collected; pipeline gates passed / 7; original 44 tests unchanged; security response status; reproducible patch file/hash match | Exp-11 logs and replay, `main-security-fix-validation.log` (**VERIFIED**) | Passing tests do not prove all security or production-scale behavior. Fixture 50 and main 45 are **different artifacts**, not competing counts. |
| Adaptation | failure→first passing rerun steps; scripted requirement resolution; checkpoint recovery actions; persistence by path at a *real* user-turn boundary | Exp-11 red/green logs, `turn-boundary-check.log`, `exp11-recovery.log` (**VERIFIED** for artifacts) | Exact total agent steps/token usage, new-chat conversation context and compaction event UNKNOWN. Deliberate tests are not organic failures. |
| Resources | local HTTP integration `RUSAGE_SELF_MAXRSS_KB=19828`; if retained, label process scope | `exp11-live-integration.log` (**VERIFIED** for one Python process) | Not whole agent/model/platform CPU or memory; no comparable resource sample for other categories. |

**Counting discipline:** 19 logged *check actions* across Tier-1 (3), Tier-2 (2), security probe/red (2), reconstruction (1), corrected security/full/pipeline/live/static (5), independent patch replay (3), and main remediation (3). This is a ledger count with heterogeneous denominators, **not** “19 validation actions per run” or a normalized rate. One unanticipated observable replan moved the excluded scratch fixture and restored from a patch; a scripted requirement change is recorded separately and is *not* an unplanned replan. No CI for one engineering case.

## Fingerprint values (narrow conditions, no unsupported precision)

| Condition | Trials | Time span (s) | Pairwise bash interval overlaps | Comparison meaning |
|---|---:|---|---|---|
| Historical Exp-08 bash batch, N=4 and N=8, 1 s sleep | 1 per N | 4.064 / 7.076 | 2/6 and 7/28 (adjacent only) | mostly serial with short adjacent overlap, original trial **still valid** |
| Exp-10 explicit parallel wrapper, N=3, 0.25 s sleep | 2 | **0.2738–0.2959** | **3/3 each** | all-pair overlap under these conditions |
| Exp-10 explicit parallel wrapper, N=3, 0.75 s sleep | 2 | **0.7726–0.7732** | **3/3 each** | all-pair overlap under these conditions |
| Exp-10 **prospectively added exploratory** matched T4 N=4, 1.0 s | 1 | **1.0433** | **6/6** | N/d alone insufficient under this wrapper; historical mode/session confounded |
| Exp-10 mixed tools | 1 | bash 0.610 s inside interval | 2 healthy file completions before bash end; 1 failed write isolated | write-file starts UNKNOWN; statuses preserved |
| Exp-11 heterogeneous engineering | 1 case + 1 artifact replay | Tier-1 47/47, final fixture 50/50, main after security fix 45/45; pipelines 7/7 | not a scheduling trial | category/tool/quality fingerprint only; **artifact replay ≠ independent agent run** |

**Variability:** two controlled within-session replicates per Exp-10 service duration permit **min–max only**, not confidence intervals. Primary Exp-10 vs historic Exp-08 differs in N, duration, assistant tool invocation envelope (not saved), and possibly session environment. The **matched X1 control** removes N/d as a *sole* explanation in this wrapper/session, but still cannot isolate invocation mode, session, jitter or other causes. The contrast refutes a *universal* serial-batch rule, not F-16's original raw observations. There is no model label/identity in the fingerprint; similarity/difference between fingerprints cannot identify a model.

## Reproduction and audit procedure

1. Read `experiments/experiment-10/DESIGN.md`, `interval.py` and the 12 preserved JSONs. Run `python3 experiments/experiment-10/analyze.py` and compare each span/overlap with `evidence/phase2/exp10/analysis.log` and the `timing_trials` array in `behavioral-fingerprint.json`. Check the JSON concatenation digest using trial order `S1,S2,L1,L2` and index order `0,1,2`; expected SHA-256 `c4832186c7972fdf477dc8921b0965c65fe13631285b722a2fb35e19df3e0ec9`. The separately preregistered exploratory X1 has four files, span 1.043323 s and 6/6 overlaps; its index-order concatenation digest is `4ed022dc949ae297b33020462e89b7309646fc75ff710a76f085780ad8cfd36a` (`matched-analysis.log`).
2. Recompute the historical Exp-08 spans from `evidence/h1/{A*,B*,Cseq}.txt` using the exact overlap predicate above; Phase-2's independent arithmetic is in `evidence/phase2/baseline-evidence-crosscheck.log`.
3. For the heterogeneous row, inspect the original/final tests and exit codes in `exp11-{tier1,tier2-red,tier2-green,security-before,security-red,security-after-and-validation,independent-verification}.log` and `main-security-fix-validation.log`. Compare `exp11-tier1-checkpoint.log`'s SHA-256 hashes to `exp11-recovery.log`; do **not** count the second fixture worktree as a second agent run.
4. To reproduce fixture quality on a fresh checkout of `c0caa6e`, `git worktree add --detach /home/user/arena-phase2-fixture-check c0caa6e`; `git -C /home/user/arena-phase2-fixture-check apply --check /home/user/arena.ai_breakthrough/evidence/phase2/exp11-fixture.patch`; then `apply`, `cd` there and `python3 -m pytest -q tests/`. Run the existing pipeline on a disposable copy to avoid overwriting tracked historical evidence. Remove only your reproduction worktree when done.
5. Cross-session/new-chat experiments require a **genuine future chat** following `phase2-research-plan.md` and `evidence/phase2/continuity-checkpoint.md` (PENDING); never fill missing rows with self-reports or inferred compaction events.

No additional orchestration infrastructure, database, message queue or remote telemetry collector is used. Measurement artifacts are the existing Python scripts/pytest/git and simple logs.
