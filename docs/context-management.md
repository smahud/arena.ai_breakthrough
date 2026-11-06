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
