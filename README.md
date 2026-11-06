# arena.ai_breakthrough

Evidence-driven study of **agentic AI execution behavior** and an independent, minimal
reference architecture reproducing the *observable* functional patterns. Executed autonomously
inside an authorized sandbox on 2026-11-06 by the agentic system under study (first-person
methodology; see `docs/limitations.md` L-1 for the epistemic ceiling this imposes).

**Status:** research complete · 7/7 experiments executed · 41/41 tests green · validation
pipeline OK · GitHub delivery **unavailable on this instance** (connector `unsupported`) →
delivered as a fully committed local git repository; publishing runbook in
`report/phase-8-delivery.md`.

## What's here

```
CONTRACT.md               12 binding rules (written before any implementation)
docs/                     findings catalog (F-01…F-15), architecture analysis, orchestration,
                          lifecycle, tool behavior, context management, limitations (L-1…L-9)
experiments/01…07         DESIGN.md (pre-registered criteria) + RESULTS.md per experiment
evidence/                 raw logs: timestamps, exit codes, hashes, diffstats, verbatim errors
benchmarks/               run_suite.py validation pipeline + EXP-02 workstreams
reference-architecture/   ARCHITECTURE.md + JUSTIFICATIONS.md (every component evidence-traced)
src/                      taskledger (EXP-01/06 app), semverlite (EXP-07), minagent (reference impl)
tests/                    41 tests, each mapped to a finding where applicable
report/                   one report per execution phase + final research summary
```

## Headline results (details & classifications in `docs/findings.md`)

1. **Independent tool calls dispatch concurrently** in one batch; failures isolate per unit
   (F-01, F-15 — VERIFIED behaviorally; true wall-clock overlap INFERRED).
2. **Recovery loop shape** is regular: detect → localize from error text → minimal (1-line)
   patch → re-verify, closing in one extra step; identical for injected and *organic* failures
   (F-02, F-14 — VERIFIED, n=4).
3. **False-green signals are the dominant validation risk**: exit-code masking through pipes;
   a test runner reporting success with zero tests executed (F-03, F-08 — VERIFIED). The
   reference implementation's validator therefore requires positive evidence of work.
4. **Early decomposition sets later adaptation cost**: a mid-flight storage-technology change
   landed in 2 files with 0 changes to pre-existing API tests, verified against SIGKILL
   (F-05 — VERIFIED via commit-pair diffstat).
5. **Early written constraints survive the whole session and beat contradictory late
   requirements** (F-06 — VERIFIED within-session; cross-turn UNKNOWN).
6. **Internal architecture is not identifiable from behavior**: three alternative internal
   architectures predict every observation here; none is privileged (`docs/architecture-analysis.md`
   §5 — UNKNOWN by construction; no models/agents inferred from style or speed).

## Run it

```bash
python3 benchmarks/run_suite.py          # full validation pipeline (needs pytest)
python3 -m pytest -q tests/              # 41 tests
cd src && python3 -m taskledger.server 8000   # the EXP-01/06 app (TASKLEDGER_DB=… for SQLite)
```

Requirements: Python ≥3.10, pytest (tests only). Zero third-party **runtime** dependencies
(constraint C-1, AST-audited — `evidence/exp04-audit.log`).

## Honesty policy

Every claim carries an evidence classification (VERIFIED / DOCUMENTED / INFERRED / HYPOTHESIS /
UNKNOWN). Failures — including this project's own defects — are preserved verbatim in
`evidence/` and narrated in `report/phase-3-execution.md`. No telemetry, trace, or capability
is reported that was not actually observed.
