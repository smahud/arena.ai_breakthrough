# Experiment 10 — RESULTS (explicit parallel wrapper, variable duration/mixed tools)

**Executed:** 2026-11-06T16:18–16:20Z, *after* committed pre-registration `9430392`; exploratory D1 addendum was registered after S1–L2 observations and before D1 singleton. **Research question:** Is Exp-08's mostly serial bash pattern stable for different call lengths and mixed tool categories in this invocation mode? **Hypotheses/alternatives/independent and controlled variables:** `DESIGN.md` (fixed N=3, d=0.25/0.75, two batches per d; same script/workspace; alternative wrapper mode, scheduler, clock skew and jitter).

## Raw observations and measurement procedure

Each independent bash call wrote `evidence/phase2/exp10/{S1,S2,L1,L2}-{0,1,2}.json` containing **inside-call start/end `time.time_ns()`** and its expected sleep; analyzed with `python3 experiments/experiment-10/analyze.py > .../analysis.log` (exact stdout in [`../../evidence/phase2/exp10/analysis.log`](../../evidence/phase2/exp10/analysis.log)). Platform return metadata was transcribed immediately to [`../../evidence/phase2/exp10/dispatch-results.md`](../../evidence/phase2/exp10/dispatch-results.md); it is not an internal trace. Commands: `python3 experiments/experiment-10/interval.py TRIAL INDEX SECONDS` for each of three independent calls **in the same explicit `multi_tool_use.parallel` wrapper**. All 12 exit codes **0**.

| Trial | N × in-tool sleep | Total span (s) | Intersecting pairs | Ordered start gaps (ms) | Pattern |
|---|---|---:|---:|---|---|
| S1 | 3 × 0.25 s | 0.2959 | **3/3** | 44.753, 1.038 | all three overlap |
| S2 | 3 × 0.25 s | 0.2738 | **3/3** | 21.530, 1.916 | all three overlap |
| L1 | 3 × 0.75 s | 0.7726 | **3/3** | 4.762, 17.694 | all three overlap |
| L2 | 3 × 0.75 s | 0.7732 | **3/3** | 2.659, 20.429 | all three overlap |

Per-call `duration_ms` was 334–370 (short) and 840–896 (long); subtracting the inside-call interval gives 83.87–145.86 ms including Python launch, tool wrappers and other unseparated costs, **not** an isolated platform overhead. Two repeats per condition report a *range*, not a confidence interval.

**Mixed batch (M1):** a 0.6 s bash interval + two independent healthy `write_file` calls + one deliberately invalid file child. Both healthy writes returned `success` and later read back exactly; invalid write returned `error`: `Cannot create directory "arena.ai_breakthrough/evidence/phase2/exp10/blocker": a file already exists at that path`. Bash returned exit 0 (`duration_ms=722`). File mtimes fell **11 ms and 127 ms after** the bash interval started and **599 ms and 483 ms before** its end (same filesystem clock assumption), so file-write **completion** occurred during the measured bash interval; file-tool *start* is not exposed. Raw mtime/contents: [`../../evidence/phase2/exp10/mixed-analysis.log`](../../evidence/phase2/exp10/mixed-analysis.log). `read_file(marker-a)` was called **only after** the batch returned; it confirmed content but does not show automatic dependency enforcement by the platform.

**Bounded timeout pair:** independent `write_file` sibling succeeded; a bash call with `timeout=1` returned `status=timeout`, `exit_code=null`, `duration_ms=1325` and start marker. A later record shows the bounded Python sleep **finished 2.00 s after start**, so under these conditions the process continued after the tool stopped waiting; see [`../../evidence/phase2/exp10/timeout-analysis.log`](../../evidence/phase2/exp10/timeout-analysis.log). This is not a general guarantee of persistence, teardown, or process liveness under other timeouts.

**Exploratory D1 control:** `D1-0.json` exists from **one submitted direct** `functions.bash` call (`duration_ms=867`); no 3-call direct envelope was submitted or recorded. **No D1 batch or comparison was executed**; the singleton is excluded. It cannot establish a protocol restriction, wrapper cause, or session/platform change.

**Exploratory matched N/d control X1 (added *prospectively* after primary results):** registered question, predictions and measurements in [`../../evidence/phase2/exp10/matched-control-plan.md`](../../evidence/phase2/exp10/matched-control-plan.md) before running. Four bash calls with **N=4, d=1.0 s**, like historical Exp-08 T4, ran in one explicit wrapper. All exit 0, **span 1.043323 s, 6/6 pairwise overlaps**, start order 0→3→1→2, ordered gaps 22.76/10.47/9.98 ms. Historical T4: **span 4.064 s, 2/6 overlaps** (`baseline-evidence-crosscheck.log`). All four raw `X1-{0..3}.json` and returned statuses are in [`../../evidence/phase2/exp10/`](../../evidence/phase2/exp10/); exact arithmetic in `matched-analysis.log`. Thus different **N and d alone** cannot explain the contrast under this wrapper/session's measured conditions. Wrapper envelope vs historical invocation, between-turn environment, policy, and clock placement are still confounded; a single exploratory matched trial does not prove which factor mattered or establish a trend.

## Criteria and interpretation

| Criterion | Outcome |
|---|---|
| S1 12 raw timed records, two repeats per length | **MET**; all well-formed and analyzed |
| S2 mixed per-unit failure isolation | **MET** for two healthy markers + one failed independent write; no bad child created |
| S3 timeout result and later sentinel | **MET** under one bounded condition; other timeout semantics UNKNOWN |
| S4 raw commands, metadata, limits/repro preserved | **MET**; no hidden worker/model claim |

**VERIFIED (narrow):** these 4 *explicit-wrapper* bash batches executed with genuine all-pair **interval overlap** for both service durations; at least two file writes completed during a bash interval; one failed write did not block healthy siblings; and the one timed-out bounded command continued after the wait ended. **REFUTED as a universal claim:** “batched bash calls always execute mostly serially” (the old F-16 headline when generalized). Exp-08's **own raw intervals remain valid**, and the old claim was already narrowed in the Phase-2 baseline audit. Different session/dispatch interface (explicit wrapper vs historical original batch envelope not preserved), N and d confound a causal comparison. This is observable **scheduling variability**, not proof of different models, hidden routing, distinct workers, or a platform implementation change. H-A1/H-A2 remain non-discriminated; H-A3 tool-category behavior differs in available telemetry; H-A4 cannot be inferred from scheduling alone.

**Reproduction:** on an authorized disposable workspace, use the committed `interval.py` in four separate N=3 `multi_tool_use.parallel` batches with S1/S2 at .25 s and L1/L2 at .75 s, then run `python3 experiments/experiment-10/analyze.py`. Mixed invalid path must be a *regular file* `blocker` under `evidence/phase2/exp10/`; timeout call is capped at two seconds. Compare spans and pairwise intersections from JSON, not returned `duration_ms`; reproduce in a **fresh detached worktree/copy** with the same fixed trial names rather than overwriting this repository's preserved evidence. Exact current trial artifacts are in the linked directory.
