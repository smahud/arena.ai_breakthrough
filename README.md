# arena.ai_breakthrough

Evidence-driven study of **agentic AI execution behavior** and an independent, minimal
reference architecture reproducing the *observable* functional patterns. Executed autonomously
inside an authorized sandbox on 2026-11-06 by the agentic system under study (first-person
methodology; see `docs/limitations.md` L-1 for the epistemic ceiling this imposes).

**Historical Phase-1/follow-up baseline:** **9/9 experiments executed** (7 core + 2 follow-up) ·
**44/44 tests green** · validation pipeline OK. **Phase 2:** EXP-10/11 executed,
main repository **45/45** tests green after one security regression, pipeline **7/7**;
experimental fixture **50/50** tests green in an independently replayed worktree.
The **historical baseline is PUBLISHED — PUBLIC**:
[github.com/smahud/arena.ai_breakthrough](https://github.com/smahud/arena.ai_breakthrough)
(created private 15:08Z; public since 16:03Z on explicit user authorization, anonymously
verified; full record in `report/phase-8-delivery.md`). **Phase-2 commits are local,
NOT published:** a noninteractive `git push --dry-run` failed with exit 128 because no
GitHub credentials were available and the GitHub connector is unsupported; anonymous
remote master remained `79412fd` ([publication record](evidence/phase2/publication-attempt.log)).
No token was stored, no force push attempted. **Phase-2 final report:**
[`report/phase2-final-report.md`](report/phase2-final-report.md) (seven questions,
local commit/evidence map, publication blocker). Historical report:
[`FINAL_REPORT.md`](FINAL_REPORT.md).

## What's here

```
CONTRACT.md               12 binding rules (written before any implementation)
docs/                     findings F-01…F-22, architecture, public-capability matrix,
                          hypothesis evaluation, behavioral fingerprinting and limitations
experiments/01…09         historical DESIGN.md + RESULTS.md per experiment
experiments/experiment-10/11  Phase-2 designs/results, timing scripts and fixture replay
evidence/                 raw logs: timestamps, exits, hashes, diffs, red/green tests
benchmarks/               run_suite.py historical 7-gate validation pipeline
reference-architecture/   ARCHITECTURE.md + JUSTIFICATIONS.md (functional, evidence-traced)
src/                      taskledger (narrow Phase-2 security fix), semverlite, unchanged minagent
tests/                    45 in main (historical 44 + 1 security regression); fixture has 50
report/                   phase reports; original FINAL_REPORT.md preserved as dated history
```

## Headline results (details & classifications in `docs/findings.md`)

1. **Batches are not governed by one universal timing pattern.** Historical Exp-08
   bash intervals were mostly serial with short adjacent overlap (T8 7/28 pairs);
   Phase-2 EXP-10's explicit wrapper showed all-pair overlap (N=3: 3/3 each;
   exploratory matched N=4/d=1: 6/6 vs old T4 2/6). The different invocation
   mode/session remains confounded; neither independent workers nor models follow
   from interval overlap (F-16/F-20, scoped VERIFIED).
2. **Recovery loop shape** is regular: detect → localize from error text → minimal (1-line)
   patch → re-verify, closing in one extra step; identical for injected and *organic* failures
   (F-02, F-14 — VERIFIED, n=4).
3. **Two false-green signals were observed** (not a prevalence estimate): exit-code masking through pipes;
   a test runner reporting success with zero tests executed (F-03, F-08 — VERIFIED). The
   reference implementation's validator therefore requires positive evidence of work.
4. **A storage seam supported a localized change**: the SQLite adaptation touched two
   source files and zero pre-existing API tests; restart durability was verified against
   SIGKILL. Causal superiority over other designs remains INFERRED (F-05).
5. **Written constraints and checkpoints enable visible continuity.** Scripted Tier-2
   conflict preserved the default API contract; across a genuine **same-chat user turn**
   a lost excluded fixture was restored from saved patch/hashes. A **new-chat** continuity
   test remains PENDING; compaction was not observed (F-06/F-21).
6. **Security verification found a real baseline defect.** An owned sibling static path
   returned 200 until a red test and `realpath`/`commonpath` correction; main has only
   that narrow fix (45/45 tests), while optional filter/UI work stays in the fixture
   (F-22). No protected files were accessed.
7. **Internal architecture remains unidentifiable:** unified, staged and specialist
   alternatives predict all these exterior behaviors; no particular model, worker count
   or hidden agent can be inferred from speed/style (`docs/hypothesis-evaluation.md`).

## Run it

```bash
python3 benchmarks/run_suite.py          # full validation pipeline (needs pytest)
python3 -m pytest -q tests/              # 45 tests in main after Phase-2 security regression
cd src && python3 -m taskledger.server 8000   # the EXP-01/06 app (TASKLEDGER_DB=… for SQLite)
```

Requirements: Python ≥3.10, pytest (tests only). Zero third-party **runtime** dependencies
(constraint C-1, AST-audited — `evidence/exp04-audit.log`).

## Honesty policy

Every claim carries an evidence classification (VERIFIED / DOCUMENTED / INFERRED / HYPOTHESIS /
UNKNOWN). Failures — including this project's own defects — are preserved verbatim in
`evidence/` and narrated in `report/phase-3-execution.md`. No telemetry, trace, or capability
is reported that was not actually observed.
