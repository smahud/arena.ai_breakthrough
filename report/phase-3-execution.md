# Phase 3 — Execution Report

**When:** 2026-11-06T13:54–14:06Z (~12 min wall, ~45 s measured tool time).
**Evidence:** 14 raw logs in `evidence/`; per-experiment RESULTS.md ×7.

## Execution ledger (chronological)

| Time (UTC) | Activity | Outcome |
|---|---|---|
| 13:54 | Exp-05 P1 (authoring fidelity) | 3 methods → 1 sha256 (VERIFIED) |
| 13:54 | Exp-07 retrieval (search ∥ fetch) | normative spec captured |
| 13:55 | Exp-02 three parallel streams | A,C green; B natural failure → 1-call recovery |
| 13:56 | Exp-02 integration + audit | green; no cross-imports |
| 13:57 | Exp-01 taskledger (8 artifacts, one batch) | written |
| 13:58 | Exp-01 validation pipeline | 7/7 PASS, exit 0 |
| 13:58 | Exp-05 P2 (pytest vs unittest) | false-green class found ("NO TESTS RAN") |
| 13:58–14:00 | Exp-05 P4 (process lifecycle) | start_process clean; nohup hang 30 s; pkill self-kill |
| 14:01 | Exp-07 validation | 15/15 pass; spec chain reproduced |
| 14:01 | Exp-03 fault injection F1/F2/F3 | all failed→recovered, 1-line fixes |
| 14:03 | git checkpoint d713a28 | baseline for Exp-06 |
| 14:04 | Exp-06 CR-1 (SQLite + conflict T2) | 28/28; SIGKILL durability; requests refused |
| 14:05 | Exp-04 T3 audit pass 1 | false positive (pytest) → refined |
| 14:06 | audit pass 2 | 0 violations, exit 0 |

## Incidents (all preserved, contract rule 9)
1. Stream B arithmetic expectation error (natural) — recovered, F-14.
2. `tee` exit-code masking (harness defect) — pipefail adopted, F-03.
3. nohup 30 s call hang + `pkill -f` self-kill (`exit_code: -1`, truncated log) — F-04.
4. Audit scanner false positive vs contract text — F-08.
5. `.pyc` tracked in checkpoint commit — hygiene defect, fixed in f75c460 — F-12.

## Parallelization behavior observed
5 dispatch batches contained multiple independent calls (2–8 per batch); dependent steps were
always serialized into later turns. No batch mixed a call with its own dependency.
