# Findings Catalog

Classification key (directive §1): **VERIFIED** = directly observed & reproducible here;
**DOCUMENTED** = authoritative public docs; **INFERRED** = indirect behavioral evidence;
**HYPOTHESIS** = plausible, unvalidated; **UNKNOWN** = insufficient evidence;
**REFUTED** = a prior scoped claim contradicted by newer evidence.
Every finding: ID · research question · source · observation · interpretation · alternatives ·
confidence · reproduction · residual uncertainty. Full raw data lives in `evidence/`.

---

**F-01 — Independent tool calls can be batched in one invocation** · RQ2 · Exp-02 (+Exp-01 batch authoring)
Three `bash` calls issued in one assistant message returned three independent structured
results (637/380/468 ms). Eight `write_file` calls likewise returned in one batch.
*Interpretation:* the user-facing tool interface accepts batched independent tool calls in
a single assistant-message round-trip; per-call results are returned. The historical
“concurrent work units” interpretation is **REFUTED as broad execution overlap** by Exp-08:
bash intervals were mostly serial *with short adjacent overlap* (F-16), not all-at-once.
*Alternatives:* the earlier “likely parallel” reading relied only on batch acceptance; raw
intervals rule out all-at-once overlap, but do not establish worker topology. *Confidence:*
batched invocation/results **VERIFIED** from the earlier first-person record; runtime pattern
**VERIFIED** only for Exp-08's timed bash calls (original batch envelope was not separately
preserved; see `report/phase2-baseline-audit.md`). *Repro:* `experiments/experiment-08/` interval method.
*Uncertainty:* non-bash tool types not interval-instrumented (no clock access); platform-
specificity UNKNOWN.

**F-02 — Recovery loop shape is detect→localize→minimal-patch→re-verify** · RQ3 · Exp-03 (+F-14)
All 3 injected faults and 1 natural fault (F-14) followed the identical loop, each closing in
one additional tool call; patches were 1 line. Error text (file/line/symbol) drove localization.
*Confidence:* **VERIFIED** for observed classes (syntax/logic/env). *Uncertainty:* deeply
non-local faults (concurrency, heisenbugs) untested.

**F-03 — Two observed false-green validation signals** · RQ3/RQ5 · Exp-02, Exp-05 P2
Two observed instances (no prevalence ranking established): (a) `pytest | tee` masked failure (`$?`=tee's 0); (b) `unittest
discover` on pytest-style tests reported `NO TESTS RAN` in success-shaped output. Exit status
alone is insufficient; validation must assert positive evidence of work (test count > 0,
expected markers). *Confidence:* **VERIFIED**. *Repro:* run either command pair.
*Consequence:* encoded in `src/minagent/validate.py`.

**F-04 — Managed process lifecycle beats shell backgrounding** · RQ3 · Exp-05 P4
`start_process`: 704 ms return with pid/log/ports; `stop_process` → clean stop. `nohup &` in
bash: call hung to its 30 s timeout (~28.5 s dead time); cleanup via `pkill -f` matched the
invoking shell's own cmdline and killed the session mid-script (`exit_code: -1`, log truncated;
target confirmed dead post-mortem). *Confidence:* **VERIFIED** (both hazards directly observed).
*Rule derived:* launch-by-PID, kill-by-PID; never pattern-kill from a shell whose own cmdline
contains the pattern.

**F-05 — Existing seam enabled a localized adaptation** · RQ1/RQ4 · Exp-06 vs Exp-01
Storage interface + HTTP-free dispatch core (chosen in Exp-01 planning) allowed CR-1 (SQLite)
to land as: +62 lines new class, +10/-3 factory, **0** changes to api.py, frontend, or the 10
pre-existing API tests; durability verified against SIGKILL. *Interpretation:* the existing storage seam is consistent with the localized change;
its causal advantage and the hypothetical monolith counterfactual are **INFERRED**, not
experimentally compared. *Confidence:* **VERIFIED** for 2 changed source files and unchanged
API tests (diffstat + commit pair d713a28→f75c460).

**F-06 — Early constraints persist; contradictions resolve toward the contract** · RQ4 · Exp-04
C-1 (T0) survived 7 interleaved experiments to the T3 audit (0 violations, AST-verified). The
T2 **scripted**, not user-initiated, contradiction was explicitly documented as conflicting
with C-1; code uses stdlib urllib and contains no `requests` import. This verifies the
*recorded resolution and artifact*, not an internal constraint resolver. *Confidence:*
within-session artifact/decision record **VERIFIED**; real user changes and cross-message
retention **UNKNOWN** (L-4).

**F-07 — Retrieval tools have distinct roles: search discovers, fetch extracts** · RQ3 · Exp-05 P3, Exp-07
Search returned a paraphrase missing the BNF and leading-zero rules; only `fetch_page` yielded
implementation-grade normative text. Semverlite was buildable from fetch output alone, not from
search output alone. *Confidence:* **VERIFIED** for this source pair; generalization
**INFERRED**.

**F-08 — Verification instrumentation itself needs verification** · RQ5 · Exp-04 T3, Exp-02
The first C-1 audit flagged sanctioned pytest usage (false positive): the checker encoded a
stricter rule than the contract's text. Fixed by re-reading the governing document and refining
the scanner; both passes preserved. Same class as F-03. *Confidence:* **VERIFIED**.

**F-09 — Sandbox profile** · environment · Phase-1 probe
Python 3.13.16 + pytest 9.0.3 + Node 20 + git, 2 vCPU / ~2 GB RAM / 21 GB disk, outbound HTTPS
works (pypi 200/36 ms). *Confidence:* **VERIFIED** (`evidence/phase1-environment-probe.log`).

**F-10 — Connector-only delivery limitation (historical; superseded by F-19)** · delivery · Phase-1 connector probe
`list_connector_tools("github")` → `{"status":"unsupported"}`. Per directive §8, deliverables
preserved as a fully committed local git repo; publishing steps documented in
`report/phase-8-delivery.md`. Nothing was published; no claim of publication is made.
*Confidence:* **VERIFIED** (platform status response).
**SUPERSEDED 15:08Z (same day):** the connector remains `unsupported`, but the user explicitly
authorized delivery and provided a PAT; repo created private via REST (`POST /user/repos` →
201) and pushed over HTTPS; publication **VERIFIED** by `git ls-remote` HEAD match
(`a15021ff…`) + repo API 200 — see `report/phase-8-delivery.md` UPDATE section and
`evidence/delivery-verification.log`. Lesson (F-19): a platform connector being unsupported
does not imply the capability is unreachable — authorized user-supplied credentials via
standard APIs (git/HTTPS) are a legitimate alternative delivery path; token hygiene: transient
use, redacted logs, no persistence in repo/config/commits.

**F-11 — Three authoring methods matched for one 122-byte payload** · RQ3 · Exp-05 P1
The three preserved files are each **122 bytes** and share identical SHA-256; this verifies
byte fidelity in **one small trial**, not tool-independence at arbitrary sizes. The older
92-B and 2541-B assertions lack matching preserved evidence for those lengths and are
**UNKNOWN** (`evidence/phase2/baseline-evidence-crosscheck.log`). *Confidence:* **VERIFIED**
for the 122-B comparison only.

**F-12 — Artifact hygiene defects are caught by diff review, not by tests** · process · Exp-01/06
Checkpoint commit tracked `__pycache__/*.pyc`; detected while reading `git diff --stat` for
Exp-06 S2, fixed in f75c460 (.gitignore + untrack). Tests never cover repo hygiene; review
steps must. *Confidence:* **VERIFIED** (single instance; frequency UNKNOWN).

**F-13 — Self-observability boundary** · RQ5 · all experiments
The only execution telemetry available about the acting system itself is what tool results
return: stdout/stderr, exit codes, `duration_ms`, process/port status. No token counts,
routing decisions, or internal planner traces were exposed **by this user-facing tool
surface in these runs**. Everything beyond behavior + artifacts is inference. *Confidence:*
**VERIFIED** for observed result fields, not universal platform absence; internals
**UNKNOWN** by construction.

**F-14 — Natural and injected failures recover identically** · RQ3/RQ4 · Exp-02 stream B
An *unplanned* arithmetic error in a test expectation (`2.67 != 3.0`) produced the same loop
shape and one-call latency as the scripted Exp-03 faults — evidence the loop is a genuine
behavioral pattern, not an artifact of fault-injection scripting. *Confidence:* **VERIFIED**
(n=1 natural sample).

**F-15 — Failure isolation across batched results** · RQ2 · Exp-02
Stream B's test failure did not prevent streams A and C from completing green in the same
batch; the failure was handled in a later sequential step. Batched execution isolates unit
failures; aggregation is where failures surface. *Confidence:* **VERIFIED**.

**F-16 — Batched bash calls: mostly serial intervals with short adjacent overlap** · RQ2 · Exp-08
Each of 4 (then 8) batched bash calls epoch-stamped its own `sleep 1` interval: T4 span 4.064 s,
T8 span 7.076 s, scaling 1.74 (parallel predicts ≈1.0); overlaps occur only between *adjacent*
calls (~0.05–0.14 s — next starts before previous finishes), never non-adjacent. Per-call
`duration_ms` (~1.06 s, uniform) could not discriminate — the interval method was required.
*Interpretation:* these batches were **not all-at-once concurrent**: spans grew with N.
They were **not strictly sequential either**: adjacent timed `sleep` intervals sometimes
overlap. “Pipelined” describes the observable handoff pattern, **not** a verified worker
implementation. Worker count, scheduler mechanism, and whether other workloads/instances
behave alike are **UNKNOWN**. Corrects F-01/Exp-02 interpretation. *Confidence:*
**VERIFIED** for raw bash interval overlap and span in these two trials only; independent
Phase-2 re-analysis: `evidence/phase2/baseline-evidence-crosscheck.log`. **Phase-2
comparison (F-20):** a different explicit-wrapper bash batch showed *all-pair overlap*;
therefore F-16 is **not a universal scheduling rule**. The original trial's own intervals
remain verified. Non-bash start times and cause of between-trial variation remain UNKNOWN.

**F-17 — Transient faults require an explicit, bounded, off-by-default blind-retry budget** · RQ3 · Exp-09
Deterministic-fault policy (retry only after patch, F-02) left a flaky command unrecoverable:
FAILED@1 with the success-on-attempt-2 command never re-run (`exp09-before.log`, GAP CONFIRMED).
Minimal extension (`Task.blind_retries=0` default; +1 branch; `blind_retry` trace event)
recovered it DONE@2 (`exp09-after.log`) with exhaustion still reported (3 new tests; suite
44/44; pre-existing 41 tests unmodified). *Confidence:* **VERIFIED** in minagent; policy
generalization to agents at large **INFERRED**. *Uncertainty:* genuinely nondeterministic
flakiness untested (L-5 remainder).

**F-18 — Session-boundary state loss in excluded paths** · environment/process · Phase-9 incident
A Phase-9 incident report records a second-session commit failure (`Author identity unknown`,
exit 128). `.git/config` is excluded from cross-message snapshots (documented platform
behavior), so loss of repo-local identity is a plausible cause, **not independently
re-verified** here: the original command stderr was not preserved as a standalone raw log. Same family as the phantom `.pyc` deletions
(`__pycache__` excluded but previously tracked). *Interpretation:* repo-local config and tracked cache artifacts should not be **assumed** to
survive snapshot boundaries; re-establish configuration when necessary and avoid tracking
excluded caches. Persistence behavior of other excluded state is UNKNOWN. *Confidence:* snapshot exclusions **DOCUMENTED**; original incident **DOCUMENTED** by
`report/phase-9-followup.md`; causal diagnosis **INFERRED**; independent reproduction
**PENDING**. *Repro:* configure repo-local identity, start a genuinely new user session,
attempt a commit without re-establishing excluded configuration. *Mitigation adopted:* global identity + commit-readiness
check recommended for validation pipelines. A later genuine **same-chat user-turn** observation
(F-21) directly verifies loss of one `.cache` fixture, but does not reproduce the original
`.git/config` incident or test a separate new-chat boundary.

**F-19 — Public GitHub delivery via authorized alternative path (retrospective registration)** · delivery · Phase-8 UPDATE + Phase-2 baseline
F-10's connector-limited historical conclusion was superseded: the preserved delivery log
records a user-authorized REST creation, git HTTPS push, and explicit public visibility
change; a Phase-2 anonymous API request verifies `private=false`, `default_branch=master`,
and `git ls-remote` verifies the public remote HEAD `79412fd…` at baseline.
*Confidence:* current public state and read access **VERIFIED**; details of the earlier
credentialed publication **DOCUMENTED** by `evidence/delivery-verification.log` and
`report/phase-8-delivery.md` (not replayed with a token); this session's write authorization
**UNKNOWN** until tested. This is a **registry repair of an earlier F-10 reference**, not a
newly executed experiment. *Architectural implication:* connector support does not imply or
preclude standard, separately authorized git/API access; no platform internals follow.

**F-20 — Explicit-wrapper batches overlap; scheduling is not universal** · RQ2/RQ3 · Exp-10
Four primary N=3 `multi_tool_use.parallel` bash batches (two 0.25 s, two 0.75 s) recorded
**3/3 overlapping interval pairs each**; spans 0.2738–0.2959 s and 0.7726–0.7732 s.
A **prospectively added, exploratory** N=4/d=1.0 s wrapper batch X1 also showed
**6/6 overlaps**, 1.0433 s span, versus historical Exp-08 T4's 2/6 and 4.064 s
with the *same N/d* (invocation mode and session still differ).
Two independent file-tool completions fell inside a bash interval; one invalid file path
failed without blocking healthy siblings. A bounded timeout returned `status=timeout` at
~1.325 s, while its command later wrote a 2.00 s completion marker.
*Interpretation:* call batching can exhibit broad **actual interval overlap** in the
explicit wrapper, contrary to a universal “serial batches” rule derived from F-16.
*Alternatives:* wrapper vs historical batch invocation envelope (not preserved),
instance/session changes, interaction with workload, jitter or clocks; matched X1 rules
out **N/d alone** under this wrapper, not those alternatives. Results do **not** identify
workers or a model change. File-tool **start** remains unmeasured. *Confidence:* **VERIFIED** narrowly for
12 primary timestamped bash calls + 4 exploratory matched calls + two file completion
mtimes + one timeout; generic scheduling rule **REFUTED**; N/d **alone** do not force
the old pattern in the matched wrapper control; causal difference **UNKNOWN**. *Repro:*
`experiments/experiment-10/DESIGN.md`, `interval.py`, `analyze.py`,
`evidence/phase2/exp10/{analysis.log,matched-control-plan.md,matched-analysis.log,dispatch-results.md,*.json}`.

**F-21 — Actual user-turn checkpoint distinguishes persisted vs excluded state** · RQ4 · Exp-11
Before a real user's “Lanjutkan” turn, an isolated fixture existed under excluded `.cache`,
with a persisted Tier-1 patch and five file hashes. On the next turn `.cache` fixture was
absent, while the main repo and evidence persisted; git still listed a prunable worktree.
Recreate at `c0caa6e` outside excluded paths + apply patch → **5/5 Tier-1 hashes match**;
reapply recorded Tier-2 edits → **2/2 prior hashes match**, focused tests pass. The
unanticipated recovery required an observable plan change (fixture location, checkpoint
restore). *Alternatives:* platform snapshot policy, process/workspace lifecycle, or their
combination; no evidence of internal forgetting. *Confidence:* **VERIFIED** for this
within-chat **turn** and these paths; *new chat* context transfer **PENDING**. *Repro:*
`evidence/phase2/{turn-boundary-check.log,exp11-recovery.log,exp11-tier1.patch}`.
On a **second genuine same-chat** user turn, the later persistent worktrees, patch SHA
and uncommitted publication-update draft also survived (`second-turn-check.log`).
This strengthens the *path-scoped artifact* observation; do not simulate a different
chat or infer internal conversational memory.

**F-22 — Security test exposed a baseline artifact defect and drove a narrow fix** · RQ3/RQ5 · Exp-11
The baseline taskledger static guard used string prefix `startswith(STATIC)`; a literal
`/../static_extra/audit.txt` fetched only a harmless fixture sentinel **HTTP 200** despite
being outside `static/`. A focused regression failed (exit 1), then `realpath` +
`commonpath` containment made it pass; fixture 50/50 tests, fresh-patch replay 50/50,
and the **main repository** received only the security guard + one focused regression
(45/45 tests and pipeline green). *Interpretation:* an independent security gate uncovered
a test gap that ordinary functional tests missed; this is not evidence of a distinct
security agent. *Confidence:* **VERIFIED** for sibling-path escape and corrected fixture/main
tests; absence of every traversal variant beyond tested sibling/symlink paths **UNKNOWN**.
*Repro:* `evidence/phase2/exp11-security-{before,red,after-and-validation}.log`,
`tests/test_taskledger_security.py`; read only owned temporary sentinels.

**Open questions (HYPOTHESIS/UNKNOWN):** H-1 as a **universal batch-scheduling rule is
REFUTED** by contrasting F-16/F-20; why conditions differ and worker count remain UNKNOWN.
H-2 internal planner boundaries remain UNKNOWN (H-A1/A2 equivalent here). H-3 *same-chat*
workspace-vs-excluded-path continuity is now observed (F-21), but genuine new-chat
constraint-resolution remains **PENDING**. H-4 compaction is **DOCUMENTED** by public help,
yet no compaction event or context-limit pressure was verified in these experiments.
