# arena.ai_breakthrough

Evidence-driven study of **agentic AI execution behavior** and an independent, minimal
reference architecture reproducing the *observable* functional patterns. Executed autonomously
inside an authorized sandbox on 2026-11-06 by the agentic system under study (first-person
methodology; see `docs/limitations.md` L-1 for the epistemic ceiling this imposes).

**Historical Phase-1/follow-up baseline:** **9/9 experiments executed** (7 core + 2 follow-up) ·
**44/44 tests green** · validation pipeline OK. **Phase 2 in progress.** **PUBLISHED — PUBLIC**:
[github.com/smahud/arena.ai_breakthrough](https://github.com/smahud/arena.ai_breakthrough)
(created private 15:08Z; public since 16:03Z on explicit user authorization, anonymously
verified; full record in `report/phase-8-delivery.md`). Final report:
[`FINAL_REPORT.md`](FINAL_REPORT.md).

## What's here

```
CONTRACT.md               12 binding rules (written before any implementation)
docs/                     findings catalog (F-01…F-19 at Phase-2 baseline), architecture,
                          orchestration, lifecycle, tool behavior, context management, limitations
experiments/01…09         DESIGN.md (pre-registered criteria) + RESULTS.md per experiment
evidence/                 raw logs: timestamps, exit codes, hashes, diffstats, verbatim errors
benchmarks/               run_suite.py validation pipeline + EXP-02 workstreams
reference-architecture/   ARCHITECTURE.md + JUSTIFICATIONS.md (every component evidence-traced)
src/                      taskledger (EXP-01/06 app), semverlite (EXP-07), minagent (reference impl)
tests/                    44 tests at Phase-2 baseline (41 at historical Phase 7 + 3 Exp-09)
report/                   one report per execution phase + final research summary
```

## Headline results (details & classifications in `docs/findings.md`)

1. **Independent tool calls can be invoked as one batch; timed bash execution was mostly
   serial, with short adjacent interval overlap** (Exp-08: T8/T4 span scaling 1.74, not ~1.0;
   7/28 interval pairs overlap in T8). Batching reduces round-trips but does not establish
   independent workers or all-at-once runtime concurrency (F-16/F-15, scoped VERIFIED).
2. **Recovery loop shape** is regular: detect → localize from error text → minimal (1-line)
   patch → re-verify, closing in one extra step; identical for injected and *organic* failures
   (F-02, F-14 — VERIFIED, n=4).
3. **Two false-green signals were observed** (not a prevalence estimate): exit-code masking through pipes;
   a test runner reporting success with zero tests executed (F-03, F-08 — VERIFIED). The
   reference implementation's validator therefore requires positive evidence of work.
4. **A storage seam supported a localized change**: the SQLite adaptation touched two
   source files and zero pre-existing API tests; restart durability was verified against
   SIGKILL. Causal superiority over other designs remains INFERRED (F-05).
5. **Early written constraints survive the whole session and beat contradictory late
   requirements** (F-06 — VERIFIED within-session; cross-turn UNKNOWN).
6. **Internal architecture is not identifiable from behavior**: three alternative internal
   architectures predict every observation here; none is privileged (`docs/architecture-analysis.md`
   §5 — UNKNOWN by construction; no models/agents inferred from style or speed).

## Run it

```bash
python3 benchmarks/run_suite.py          # full validation pipeline (needs pytest)
python3 -m pytest -q tests/              # 44 tests at Phase-2 baseline
cd src && python3 -m taskledger.server 8000   # the EXP-01/06 app (TASKLEDGER_DB=… for SQLite)
```

Requirements: Python ≥3.10, pytest (tests only). Zero third-party **runtime** dependencies
(constraint C-1, AST-audited — `evidence/exp04-audit.log`).

## Honesty policy

Every claim carries an evidence classification (VERIFIED / DOCUMENTED / INFERRED / HYPOTHESIS /
UNKNOWN). Failures — including this project's own defects — are preserved verbatim in
`evidence/` and narrated in `report/phase-3-execution.md`. No telemetry, trace, or capability
is reported that was not actually observed.
