# Orchestration Analysis

## Observed coordination patterns (all VERIFIED, sources in `evidence/`)

1. **Batch dispatch of independent units.** Tool calls with no data dependency were issued in
   a single block and returned as a set (Exp-02: 3 streams; Exp-01: 8 artifact writes). The
   invariant actually used: *independence is decided at authoring time* — streams A/B/C had
   zero shared code by design, which made conflict resolution unnecessary rather than solved.
2. **Failure isolation in batches.** A failing unit (stream B) neither blocked nor corrupted
   siblings (A, C green in same batch); the failure surfaced at aggregation (F-15).
3. **Sequential aggregation step.** Integration (`pipeline.py`) ran strictly after all streams
   completed, in its own call, importing outputs via path composition only.
4. **Validation is serialized.** Test/pipeline/audit runs were never batched with the writes
   they validate — validate-after-author, one gate at a time (Exp-01 → run_suite; Exp-06 →
   full-suite + diffstat + grep).
5. **Checkpointing around risky change.** git commit before CR-1 made blast radius measurable
   (`git diff --stat <sha>`) — orchestration uses VCS as an observation instrument (F-05).
6. **Managed lifecycle for long-running units.** Servers via `start_process` (returns pid +
   ports), stopped via `stop_process`; never backgrounded inside bash (F-04 hazards).

## Delegation & specialization

No sub-agent delegation interface was exposed or observed in this environment; the only
delegation observed is **tool delegation** (work handed to sandboxed processes). Statements
about hidden specialist agents are not supportable (architecture-analysis §5: A1–A3 all fit).
Writing-style shifts between artifacts (e.g., code vs prose) are NOT treated as evidence of
different generators, per directive §2E.

## Shared context management

- **Contract file** = normative long-term memory (constraints C-1/C-2, rule 12).
- **Evidence files** = append-only episodic memory (timestamps, exit codes, quotes).
- **RESULTS/DESIGN files** = consolidated semantic memory per workstream.
- Conversation transcript itself was the only channel for short-term sequencing; no external
  task queue existed. The pattern "externalize anything needed later into a file" was used
  throughout and is the behavior the reference implementation codifies (`state.py`).

## Conflict resolution instances

| Conflict | Resolution | Evidence |
|---|---|---|
| T2 `requests` vs C-1 | earlier contract wins; stdlib substitute; logged | exp06-verification.log |
| Audit rule vs contract text | contract text wins; scanner refined | exp04-audit.log (both passes) |
| pytest-style tests vs unittest runner | runner switched to pytest; guard added | exp05-p2-runners.log |

Pattern: conflicts resolved toward the **earlier, more authoritative, written** artifact, and
the resolution itself is recorded — never silent.
