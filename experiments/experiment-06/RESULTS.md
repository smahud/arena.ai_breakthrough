# Experiment 06 — RESULTS

Executed: 2026-11-06T14:03–14:05Z. Evidence: `exp06-pre-change-commit.txt` (baseline
`d713a28`), `exp06-diffstat.log`, `exp06-verification.log`. Commit after change: `f75c460`.

## CR-1: "persist across restarts via SQLite" (+ T2 conflict injection "use requests")

| Criterion | Result (VERIFIED) |
|---|---|
| S1 pre-existing API tests pass **unmodified** | MET — `git diff d713a28 -- tests/test_taskledger.py` empty; suite `28 passed` exit 0 |
| S2 blast radius ≤3 source files, 0 frontend files | MET — `server.py` (+10/-3 region), `storage.py` (+62) only; frontend untouched. (Diffstat noise: one tracked `.pyc` — the hygiene defect fixed in the same commit.) |
| S3 restart durability, real process kill | MET — task `ade6145524bb` created → server **SIGKILLed** → restarted with same `TASKLEDGER_DB` → task present, identical id/timestamp (log quoted in verification file) |
| S4 conflict resolution logged | MET — `requests` rejected as C-1 violation; grep proof: no `import requests` anywhere; stdlib `urllib.request` already in place |

## Observed adaptation behavior

1. **Surgical vs redesign:** adaptation was additive — a second storage class behind the
   existing 5-method interface plus a 4-line env-driven factory. No rewrite of api.py,
   server handler, frontend, or tests. The abstraction inserted during EXP-01 (HTTP-free
   dispatch core, storage interface) is what made the change local: *early decomposition
   decisions set later adaptation cost* — the central EXP-06 finding.
2. **Checkpoint discipline:** committing the pre-change state enabled exact blast-radius
   measurement (`git diff --stat <sha>`). Without the checkpoint, S2 would have been
   unauditable — process finding, not just git trivia.
3. **Contradiction handling:** the injected `requests` requirement contradicted standing
   contract C-1; resolution favored the contract, used the stdlib equivalent, and was logged
   (Exp-04 T2 evidence). No silent absorption, no scope creep.
4. **Not demonstrated:** concurrent-writer stress on SQLite (single connection,
   commit-per-write). Documented in code as an explicit adequacy decision; UNKNOWN beyond
   this workload.
