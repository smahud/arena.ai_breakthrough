# Phase 2.1 — Baseline verification and consistency audit

**Objective:** Establish the live repository baseline, independently check preserved claims, and reconcile current documentation *before* any Phase 2 experiment. Audit time: 2026-11-06T16:11–16:13Z; baseline `79412fd52b2db8c23855a35aec867e9a27384fc4` on `master` of `smahud/arena.ai_breakthrough`.

## Actions, inspected files, commands, evidence

- Cloned the public GitHub repository anonymously, checked `git ls-remote --symref origin HEAD`, `git rev-parse HEAD`, `git status --porcelain=v1`, complete `git ls-files` tree (114 tracked files), `git fsck --no-reflogs --full` (no errors), and anonymous GitHub repository API (`full_name`, `default_branch=master`, `private=false`). Initial post-clone tree clean. This Phase 2 audit itself added untracked `evidence/phase2/`; the later probe showing it untracked is expected, not a pre-existing change. Raw output: [`../evidence/phase2/baseline-repository-probe.log`](../evidence/phase2/baseline-repository-probe.log).
- Read `README.md`, `CONTRACT.md`, `FINAL_REPORT.md`, all relevant `docs/`, `reference-architecture/`, every `experiments/experiment-01…09/{DESIGN,RESULTS}.md`, earlier phase reports, all evidence logs/intervals, `benchmarks/`, `src/`, `tests/`, and `report/`. Inspected `git` history/checkpoint diff; the baseline includes **nine** experiment pairs and **18** formally registered findings (F-01…F-18). The sole orphan reference is `F-19` (in F-10). No experiment-10 or finding F-20 exists at baseline.
- Independently re-analyzed Exp-08 epoch files, not rerunning the old experiment: T4 4.064 s, 2/6 adjacent overlaps; T8 7.076 s, 7/28 adjacent overlaps; sequential control 4.018 s, 0/6. Thus **dominantly serial intervals with small genuine adjacent overlap** were observed for those bash calls; strict non-overlap and worker counts are *not* established. Checked Exp-06 source-only diff (`server.py` and `storage.py`, unchanged `api.py`/frontend/API tests), Exp-05 canonical byte counts (122 B each, matching SHA-256), and missing designed evidence aliases. Raw output: [`../evidence/phase2/baseline-evidence-crosscheck.log`](../evidence/phase2/baseline-evidence-crosscheck.log).
- Ran `python3 -m pytest --collect-only -q tests/`, `python3 -m pytest -q tests/`, `python3 benchmarks/run_suite.py` on a clean **`git archive HEAD` copy** in `/home/user/.cache/arena-phase2-baseline` so that the pipeline could write its result JSON without changing the historically tracked `evidence/run-suite-result.json`. **44 collected; 44 passed; pipeline 7/7 PASS, exit 0.** Raw commands, results and exit codes: [`../evidence/phase2/baseline-validation.log`](../evidence/phase2/baseline-validation.log). The historical 41-test count remains true *for the earlier Phase 7 snapshot*, not for HEAD.

## Audit of historical findings (classification for this baseline, not retroactive deletion)

| IDs | Independent check and boundary |
|---|---|
| F-01, F-15, F-16 | Exp-02 logs show separate stream outputs and failed B, but original platform batch-invocation envelope was not preserved as a standalone raw artifact. Exp-08 interval files independently confirm dominant serial execution with adjacent short overlaps for **bash**, not all tool types and not worker topology. Original “parallel batch” phrasing is not supportable as execution concurrency. |
| F-02–F-04, F-08, F-14 | Failure logs, masked exit, zero-test signal, and staged recoveries present; F-03's word “dominant” is a prevalence claim unsupported by two incidents. Exp-03's missing-binary subcase (F3a) has no same-command recovery despite its overall S3 blanket MET statement; scope S3 to the fixed subcases. |
| F-05–F-07 | Exp-06 checkpoint diff supports **two source files** changed and API tests unchanged; causation and the hypothetical monolith counterfactual are not directly tested. Exp-04 records a *scripted* contradiction and no `requests` import; no test of a later real user change or internal constraint resolver. Exp-07 preserved normative excerpts and green tests, not a raw search/fetch call transcript. |
| F-09–F-12 | Historical environment probe present (not a promise about a new sandbox). F-10's no-publication conclusion was superseded by the later anonymous public verification and current API/remote HEAD. F-11's preserved payloads are **122 B**, not 92 B or ~2 KB; an extra 2541-B run lacks preserved raw byte/hash evidence. F-12's history shows tracked `.pyc` files at the early checkpoint. |
| F-13, F-17, F-18 | F-13 describes telemetry of this user-facing interface, not every possible platform capability. Exp-09 before/after traces and 3 added tests are preserved (minagent, not necessarily the platform's own recovery policy). F-18 is documented by a later incident report plus platform snapshot-exclusion rule, but the original commit-failure stderr is **not preserved as an independent raw log**; the proposed cause is plausible, not independently re-verified here. |

## Traceable correction ledger (applies to *current guidance*; original evidence/history remains)

Every row names an original statement, supporting evidence, reason, updated statement, and affected documents. Historical phase reports remain as dated records; addenda/cross-references mark supersession rather than silently editing old reports.

| ID | Original statement and evidence | Reason for correction / updated statement | Documents affected |
|---|---|---|---|
| C01 publication | `CONTRACT.md` “No claim of publication is or will be made”; `docs/limitations.md` L-9 “GitHub delivery unverified”; `report/final-summary.md` historical delivery; phase-1 and phase-8 original sections. Phase-1 connector response really was `unsupported` (`evidence/phase1-environment-probe.log`). | Later `evidence/delivery-verification.log`, `report/phase-8-delivery.md` UPDATE, `FINAL_REPORT.md`, anonymous GitHub API and remote HEAD show **public publication**. Connector status ≠ repository delivery status. Retain old text as time-stamped history with prominent supersession notes; now public at baseline `79412fd`. | `CONTRACT.md`, `docs/limitations.md`, `docs/public-capabilities.md`, `docs/execution-lifecycle.md`, `report/final-summary.md`, `README.md`, F-10/F-19 |
| C02 execution vocabulary | F-01 “dispatch concurrently,” F-15 “parallel batch,” Exp-02 DESIGN “executes … concurrently,” Exp-08/F-16 “execute sequentially,” architecture §2/§5 “parallel dispatch,” and README headline; Exp-02/08 results, `evidence/h1/*.txt`. | One-message **batched invocation** and per-unit results are observed; **concurrent dispatch** (same message) says nothing about runtime. Exp-08 shows **mostly serial execution with measurable adjacent overlap** for bash, not strictly sequential execution or independent worker count. In-process threads in minagent are a distinct tested mechanism. | `docs/findings.md`, `docs/architecture-analysis.md`, `docs/orchestration-analysis.md`, `reference-architecture/{ARCHITECTURE,JUSTIFICATIONS}.md`, `README.md`, Exp-02 DESIGN/RESULTS addenda, `report/final-summary.md` addendum |
| C03 registry | F-10 refers to F-19, but the registry headings end at F-18 (`baseline-repository-probe.log`). | Register **F-19 as a retrospective publication finding**, *not a newly run experiment*; next new finding is F-20. | `docs/findings.md`, `README.md` |
| C04 test counts | README inventory/command say 41 tests and F-01…F-15, while header/FINAL_REPORT say 44. Phase-7 snapshot really recorded 41; Exp-09 added three; 44 tests collected and pass at HEAD (`baseline-validation.log`). | Label 41 as historical Phase-7 and 44 as present baseline; update live README inventory/command. Preserve historical phase-7/final-summary counts as dated, with addendum. | `README.md`, `report/final-summary.md` addendum |
| C05 evidence paths | Exp-06 DESIGN names `evidence/exp06-durability.log` and `exp06-tests-after.log`; neither exists, while restart/test output resides in `evidence/exp06-verification.log` (`baseline-evidence-crosscheck.log`). | Mark both original planned paths superseded by the **combined preserved file**; no fabricated logs. | `experiments/experiment-06/DESIGN.md` addendum, this audit |
| C06 measurement/attribution | Exp-05 RESULTS “92-byte canonical” and “2541-byte … also matched”; Exp-05 DESIGN “~2 KB”; F-11 “also verified at 2541 B.” Actual files each 122 B + three SHA-256 matches; no 2541-B artifact (`baseline-evidence-crosscheck.log`). | Narrow VERIFIED to **one 122-B three-method match**; other size comparison UNKNOWN without raw artifacts. Preserve historical assertion in an explicit correction addendum, not as a validated result. | `experiments/experiment-05/{DESIGN,RESULTS}.md`, `docs/findings.md`, this audit |
| C07 evidence strength | F-16 “one sandbox worker (INFERRED),” F-03 “dominant,” F-05 untested counterfactual, F-18 “VERIFIED” incident cause, F-13 blanket telemetry, Exp-03 S3 all faults recovered. Raw epochs, logs, git diff and incident narrative (above). | Restrict scope: worker count UNKNOWN; two observed false-green incidents (no prevalence); causal/counterfactual implications INFERRED; F-18 original failure raw stderr not preserved; telemetry surface only; F3a diagnosis but no same-command retry. | `docs/findings.md`, `docs/limitations.md`, `experiments/experiment-03/RESULTS.md`, `docs/architecture-analysis.md` |
| C08 contract continuity | Existing contract requires evidence, reproducibility, security, test+pipeline validation before commit and phase reports. Its consequence section has a stale status; classification key lacks REFUTED, and the pipeline overwrites its tracked historical JSON if run at source HEAD. | Keep rules 1–12 binding; **add** dated Phase-2 continuation clarifying publication supersession, six labels incl. REFUTED, Phase 2 experiment fields, historical-output preservation via clean archive, and original status as history. No security or research safeguard weakened. | `CONTRACT.md`, `docs/findings.md`, this audit |

## Failures, unresolved questions, next actions

- **Observed audit failures:** one dangling finding ID; two stale evidence path names; inaccurate file size; competing execution terminology; stale publication/test counts. No baseline test or integrity failure. Formal correction status and final modified-file list will be appended before this phase closes.
- **Unresolved:** original F-01 batch envelope unavailable as independently replayable artifact; F-18 raw commit-failure stderr missing; hidden scheduling/worker/model/planner boundaries remain UNKNOWN. Public delivery is confirmed, but this session has not yet established *write* authorization; no push is claimed.
- **Next:** pre-register a small high-information experiment set (Phase 2.2). Do not rerun completed Experiments 01–09.

## Phase close — corrections applied

C01–C08 are applied through dated notes and narrowed current claims in: `CONTRACT.md`,
`README.md`, `FINAL_REPORT.md`, `docs/{architecture-analysis,execution-lifecycle,findings,
limitations,orchestration-analysis,public-capabilities}.md`, `experiments/experiment-02`
DESIGN/RESULTS, experiment-03 RESULTS, experiment-05 DESIGN/RESULTS, experiment-06 DESIGN,
experiment-08 RESULTS, `reference-architecture/{ARCHITECTURE,JUSTIFICATIONS}.md`, and
`report/{final-summary,phase-6-implementation,phase-9-followup}.md`. Raw historical evidence
files were **not edited**. F-19 is retrospective, not an extra completed experiment.

Independent baseline validation was green as recorded above; `git diff --check` passed.
An attempted `rg` search failed because `rg` is not installed; equivalent `grep -RInE`
succeeded. A first registry checker also failed by counting this audit's prospective “F-20”
as an already cited finding; the corrected check excluded this explicit forward reference and
found 19 unique registered IDs and **zero unregistered findings cited as established**.
Both checker attempts and the 44/44 tests + pipeline green on the corrected working-copy
snapshot are preserved in `evidence/phase2/audit-validation.log`. The corrections deliberately
leave old claims
visible in dated reports / experiment-design addenda rather than retroactively changing raw
observations. Any further previously unrecognized contradiction must receive its own dated
correction entry. No new experiment has yet been executed at this phase boundary.
