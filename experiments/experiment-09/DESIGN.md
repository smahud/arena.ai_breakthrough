# Experiment 09 — Transient (Flaky) Faults and Blind-Retry Policy

**Objective (RQ3, extends L-5):** The Exp-03 fault classes were deterministic; the adopted
recovery policy (F-02) retries only *after a successful patch*, never blindly. Deterministic
faults make blind retry useless — but **transient** faults (flaky external commands) succeed on
identical re-execution. Question: does the current `minagent` policy handle transient faults,
and if not, what minimal, evidence-justified extension does?

**Design:**
1. Build a flaky command: shell snippet backed by a counter file — fails (exit 1) on the first
   invocation, succeeds on the second. This is the honest minimal model of flakiness
   (deterministic *given attempt count*, transient *from the agent's viewpoint*).
2. Run it through `minagent.AgentLoop` **as-is** (no repair fn): predict FAILED after 1 attempt
   (per Phase-6 semantics: no patch → no retry). Record actual behavior.
3. If (2) confirms the gap: extend minimally — new optional `Task.blind_retries: int = 0`
   field; `_execute` permits up to `blind_retries` identical re-runs when no repair applies.
   No other component changes. Default stays 0 (existing semantics and tests untouched).
4. Re-run: flaky task now recovers via blind retry; full suite stays green.

**Measurable success criteria:**
- S1: pre-change behavior recorded with trace showing FAILED at attempts=1 (gap confirmed).
- S2: post-change: flaky task DONE with attempts=2, trace event `blind_retry` present.
- S3: all pre-existing tests pass UNMODIFIED (default 0 preserves F-02 semantics).
- S4: `reference-architecture/JUSTIFICATIONS.md` gains a row citing THIS experiment; no
  speculative retry machinery beyond the single field (contract rule 3).

**Evidence:** `evidence/exp09-before.log`, `evidence/exp09-after.log`.
