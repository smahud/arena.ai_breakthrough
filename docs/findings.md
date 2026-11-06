# Findings Catalog

Classification key (directive §1): **VERIFIED** = directly observed & reproducible here;
**DOCUMENTED** = authoritative public docs; **INFERRED** = indirect behavioral evidence;
**HYPOTHESIS** = plausible, unvalidated; **UNKNOWN** = insufficient evidence.
Every finding: ID · research question · source · observation · interpretation · alternatives ·
confidence · reproduction · residual uncertainty. Full raw data lives in `evidence/`.

---

**F-01 — Independent tool calls dispatch concurrently** · RQ2 · Exp-02 (+Exp-01 batch authoring)
Three `bash` calls issued in one assistant message returned three independent structured
results (637/380/468 ms). Eight `write_file` calls likewise returned in one batch.
*Interpretation:* the execution layer accepts and processes batched independent tool calls in
a single round-trip. ~~Work-unit concurrency is real at tool granularity~~ — **CORRECTED by
Exp-08 (14:52Z):** batched calls execute *sequentially* with ~0.13 s pipelined handoffs; the
batch economy is round-trip elimination, not concurrent execution (see F-16).
*Alternatives:* the earlier "likely parallel" reading was an inference from batch acceptance;
interval timestamps (Exp-08) refuted it. *Confidence:* batched dispatch & independent results
**VERIFIED**; wall-clock overlap **REFUTED → F-16 VERIFIED (sequential+pipelined)** for bash
calls in this environment. *Repro:* `experiments/experiment-08/` interval method.
*Uncertainty:* non-bash tool types not interval-instrumented (no clock access); platform-
specificity UNKNOWN.

**F-02 — Recovery loop shape is detect→localize→minimal-patch→re-verify** · RQ3 · Exp-03 (+F-14)
All 3 injected faults and 1 natural fault (F-14) followed the identical loop, each closing in
one additional tool call; patches were 1 line. Error text (file/line/symbol) drove localization.
*Confidence:* **VERIFIED** for observed classes (syntax/logic/env). *Uncertainty:* deeply
non-local faults (concurrency, heisenbugs) untested.

**F-03 — False-green signals are the dominant validation risk** · RQ3/RQ5 · Exp-02, Exp-05 P2
Two independent instances: (a) `pytest | tee` masked failure (`$?`=tee's 0); (b) `unittest
discover` on pytest-style tests reported `NO TESTS RAN` in success-shaped output. Exit status
alone is insufficient; validation must assert positive evidence of work (test count > 0,
expected markers). *Confidence:* **VERIFIED**. *Repro:* run either command pair.
*Consequence:* encoded as `validator.py` guard in the reference implementation.

**F-04 — Managed process lifecycle beats shell backgrounding** · RQ3 · Exp-05 P4
`start_process`: 704 ms return with pid/log/ports; `stop_process` → clean stop. `nohup &` in
bash: call hung to its 30 s timeout (~28.5 s dead time); cleanup via `pkill -f` matched the
invoking shell's own cmdline and killed the session mid-script (`exit_code: -1`, log truncated;
target confirmed dead post-mortem). *Confidence:* **VERIFIED** (both hazards directly observed).
*Rule derived:* launch-by-PID, kill-by-PID; never pattern-kill from a shell whose own cmdline
contains the pattern.

**F-05 — Early decomposition sets later adaptation cost** · RQ1/RQ4 · Exp-06 vs Exp-01
Storage interface + HTTP-free dispatch core (chosen in Exp-01 planning) allowed CR-1 (SQLite)
to land as: +62 lines new class, +10/-3 factory, **0** changes to api.py, frontend, or the 10
pre-existing API tests; durability verified against SIGKILL. *Interpretation:* abstraction at
seams predicted to change is what makes replanning surgical; a monolith would have forced
redesign. *Confidence:* **VERIFIED** (diffstat + commit pair d713a28→f75c460).

**F-06 — Early constraints persist; contradictions resolve toward the contract** · RQ4 · Exp-04
C-1 (T0) survived 7 interleaved experiments to the T3 audit (0 violations, AST-verified). The
T2 injection ("use requests") was refused *as a C-1 violation*, downgraded to stdlib urllib,
and logged. *Confidence:* within-session **VERIFIED**; cross-message **UNKNOWN** (L-4).

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

**F-10 — GitHub delivery unavailable on this instance** · delivery · Phase-1 connector probe
`list_connector_tools("github")` → `{"status":"unsupported"}`. Per directive §8, deliverables
preserved as a fully committed local git repo; publishing steps documented in
`report/phase-8-delivery.md`. Nothing was published; no claim of publication is made.
*Confidence:* **VERIFIED** (platform status response).

**F-11 — File-authoring fidelity is tool-independent** · RQ3 · Exp-05 P1
Identical payload via `write_file`, heredoc, Python → identical sha256 (1 distinct hash/3
methods; also verified at 2541 B). *Confidence:* **VERIFIED**.

**F-12 — Artifact hygiene defects are caught by diff review, not by tests** · process · Exp-01/06
Checkpoint commit tracked `__pycache__/*.pyc`; detected while reading `git diff --stat` for
Exp-06 S2, fixed in f75c460 (.gitignore + untrack). Tests never cover repo hygiene; review
steps must. *Confidence:* **VERIFIED** (single instance; frequency UNKNOWN).

**F-13 — Self-observability boundary** · RQ5 · all experiments
The only execution telemetry available about the acting system itself is what tool results
return: stdout/stderr, exit codes, `duration_ms`, process/port status. No token counts, no
routing decisions, no internal planner traces are observable. Everything beyond behavior +
artifacts is inference. *Confidence:* **VERIFIED** (absence directly observed); internals
**UNKNOWN** by construction.

**F-14 — Natural and injected failures recover identically** · RQ3/RQ4 · Exp-02 stream B
An *unplanned* arithmetic error in a test expectation (`2.67 != 3.0`) produced the same loop
shape and one-call latency as the scripted Exp-03 faults — evidence the loop is a genuine
behavioral pattern, not an artifact of fault-injection scripting. *Confidence:* **VERIFIED**
(n=1 natural sample).

**F-15 — Failure isolation within a parallel batch** · RQ2 · Exp-02
Stream B's test failure did not prevent streams A and C from completing green in the same
batch; the failure was handled in a later sequential step. Batched execution isolates unit
failures; aggregation is where failures surface. *Confidence:* **VERIFIED**.

**F-16 — Batched tool calls execute sequentially with pipelined handoffs** · RQ2 · Exp-08
Each of 4 (then 8) batched bash calls epoch-stamped its own `sleep 1` interval: T4 span 4.064 s,
T8 span 7.076 s, scaling 1.74 (parallel predicts ≈1.0); overlaps occur only between *adjacent*
calls (~0.05–0.14 s — next starts before previous finishes), never non-adjacent. Per-call
`duration_ms` (~1.06 s, uniform) could not discriminate — the interval method was required.
*Interpretation:* one sandbox worker (INFERRED) processing a batch queue with pipelined
teardown/startup; batching saves model↔platform round-trips, not execution wall-time.
Corrects F-01/Exp-02 interpretations (correction addenda filed in both).
*Confidence:* **VERIFIED** (raw epochs preserved, analysis reproducible). *Uncertainty:*
write_file-batch timing UNKNOWN; other platforms UNKNOWN.

**F-17 — Transient faults require an explicit, bounded, off-by-default blind-retry budget** · RQ3 · Exp-09
Deterministic-fault policy (retry only after patch, F-02) left a flaky command unrecoverable:
FAILED@1 with the success-on-attempt-2 command never re-run (`exp09-before.log`, GAP CONFIRMED).
Minimal extension (`Task.blind_retries=0` default; +1 branch; `blind_retry` trace event)
recovered it DONE@2 (`exp09-after.log`) with exhaustion still reported (3 new tests; suite
44/44; pre-existing 41 tests unmodified). *Confidence:* **VERIFIED** in minagent; policy
generalization to agents at large **INFERRED**. *Uncertainty:* genuinely nondeterministic
flakiness untested (L-5 remainder).

**F-18 — Session-boundary state loss in excluded paths** · environment/process · Phase-9 incident
Second-session commit failed (`Author identity unknown`, exit 128): repo-local `.git/config`
is excluded from cross-message workspace snapshots (platform credential-path policy), so
session-1 git identity did not survive. Same family as the phantom `.pyc` deletions
(`__pycache__` excluded but previously tracked). *Interpretation:* any state stored in
snapshot-excluded paths is session-scoped; persistence requires files outside excluded paths
(e.g. `~/.gitconfig`) or re-establishment at session start. *Confidence:* **VERIFIED** (both
incidents directly observed, fixes applied). *Repro:* configure repo-local git identity, start
a new message, attempt a commit. *Mitigation adopted:* global identity + commit-readiness
check recommended for validation pipelines.

**Open questions (HYPOTHESIS/UNKNOWN):** ~~H-1~~ **RESOLVED by Exp-08 → F-16 (sequential+
pipelined, not parallel)**; H-2 whether planning is a distinct internal
phase or emerges per-step from the same generative process (UNKNOWN — both architectures
predict all observations here; see architecture-analysis §5); H-3 cross-turn constraint
persistence (UNKNOWN, L-4); H-4 behavior under context-window pressure (UNKNOWN — session was
short relative to limits; no compaction event was observable).
