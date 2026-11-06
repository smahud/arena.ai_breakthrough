# Context Management (observed strategies)

## Externalization hierarchy actually used

| Layer | Artifact | Role | Example from this session |
|---|---|---|---|
| Normative | `CONTRACT.md` | constraints that outrank later instructions | C-1 refused the T2 `requests` injection ~12 min and ~35 tool calls after declaration |
| Episodic | `evidence/*.log` | raw, timestamped, append-only memory | diagnoses quote log text verbatim (exp03) |
| Semantic | `DESIGN.md`/`RESULTS.md` | consolidated per-workstream knowledge | criteria tables reference evidence paths |
| Versioned | git commits | recoverable checkpoints + measurement baseline | `d713a28` enabled exact blast-radius diff |
| Working | transcript | sequencing + short-term state | dependency ordering of tool batches |

## Observed behaviors

1. **Write-then-reference:** anything needed later (constraints, hashes, exit codes, PIDs) was
   persisted to files at the moment of observation, not held implicitly.
2. **Constraint re-checking:** early constraints were re-verified late by *executable* audits
   (AST import scan, HTML grep) rather than by recall — memory claims converted to
   measurements (exp04 T3).
3. **Contradiction handling:** new information conflicting with written constraints was
   resolved toward the earlier written artifact and the resolution logged (F-06); no silent
   overwriting observed.
4. **Chunk discipline:** `fetch_page` chunk 0 sufficed for exp07; fetching all chunks was
   avoided — context budget treated as a resource (directive §3 "avoid unnecessary repeated
   tests" applied to retrieval).
5. **Batching as context economy:** independent calls batched into one block reduces
   round-trips and keeps the transcript compact (F-01).

## Limits of these observations

Within-session only. How context behaves near window limits, whether the platform compacts or
summarizes older turns, and how constraints survive across separate user messages/days are
**UNKNOWN** (H-3/H-4, limitations L-4) — no compaction event was observable in this session's
telemetry, and none can be induced on demand.

## Phase-2 addendum (supersedes only the final “separate user messages” clause)

**Original statement:** “Within-session only ... how constraints survive across separate
user messages/days UNKNOWN.” **Evidence:** EXP-11 was interrupted by an actual user
“Lanjutkan” message; `evidence/phase2/turn-boundary-check.log` records the `.cache`
fixture absent but the main repo and persisted patch/evidence present; reapplication
matched 5/5 earlier file hashes and 2/2 recorded Tier-2 hashes
(`exp11-recovery.log`). **Reason for correction:** a real within-chat user-turn boundary
was subsequently observed. **Updated statement:** state **in persisted artifacts**
survived this *same chat* turn and enabled precise reconstruction; one excluded `.cache`
path did not. A second genuine user continuation preserved the new persistent worktrees,
patch SHA-256 and an uncommitted publication-update draft (`second-turn-check.log`).
This verifies an externalized-state recovery strategy, not a model's
unassisted memory or cross-chat constraint survival. A genuine **new-chat** continuity
check remains PENDING; a real context compaction event is **UNKNOWN**. Public
[token-limit documentation](https://help.arena.ai/articles/3975292349-arena-troubleshooting-session-token-limits)
describes Agent Mode compaction (**DOCUMENTED**, not a trace of this chat).

**Affected documents:** this file's original limits paragraph, `limitations.md` L-4,
`findings.md` F-18/F-21, `architecture-analysis.md` §6–7, and Phase-2 reports. Phase-1
context observations and original evidence are retained, not rewritten as a new-chat test.
