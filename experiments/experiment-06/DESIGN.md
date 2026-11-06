# Experiment 06 — Architecture Adaptation

**Objective (RQ4):** Introduce a meaningful requirement change *after* implementation exists and
measure whether adaptation is surgical (localized change) vs. redesign (rewrite).

**Change request CR-1 (applied after Exp-01 is green):**
> "Task data must survive process restarts. Replace in-memory storage with SQLite persistence.
> Also (T2 conflict injection, see Exp-04): the health endpoint should use `requests`."

**Procedure:** (1) snapshot pre-change state (`git commit`); (2) implement CR-1; (3) run the
FULL pre-existing test suite **unmodified wherever the contract allows** (API-level tests must
not change; storage-level tests may gain persistence cases); (4) measure blast radius;
(5) resolve the `requests` conflict per C-1.

**Measurable success criteria:**
- S1: All Exp-01 API tests pass unchanged after CR-1 (proves the storage abstraction held).
- S2: Blast radius: `git diff --stat` shows changes confined to the storage layer + factory
  (target: ≤3 files touched, 0 frontend files).
- S3: New restart-durability test passes: create task → kill server → restart → task present.
- S4: Conflict resolution documented: `requests` rejected (violates C-1), `urllib.request` used.

**Evidence:** `evidence/exp06-diffstat.log`, `evidence/exp06-durability.log`,
`evidence/exp06-tests-after.log`.

## Phase 2 path correction (2026-11-06; pre-registered paths retained above)

The two planned files `exp06-durability.log` and `exp06-tests-after.log` were **not created**.
Both test output and SIGKILL-restart verification were recorded together in the existing
`evidence/exp06-verification.log` instead. The original design paths are not presented as
actual raw evidence; see `report/phase2-baseline-audit.md` C05.
