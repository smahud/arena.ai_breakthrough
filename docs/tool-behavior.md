# Tool Behavior (observed properties only)

Catalog of the authorized tool surface used in this study, with empirically measured behavior.
Telemetry columns reflect what results actually expose (F-13); nothing here claims internals.

| Tool | Used for | Result telemetry observed | Behavior notes (evidence) |
|---|---|---|---|
| `bash` | builds, tests, probes, faults | stdout, stderr, `exit_code`, `duration_ms`, timeout status | `$?` after pipes = last command only → `set -o pipefail` mandatory (exp02). Backgrounded processes hold the call open → 30 s timeout, `exit_code: null` (exp05 P4). Patterns in `pkill -f` can match the invoking shell (exp05 P4). |
| `write_file` | artifacts, docs, designs | success flag only | Byte-fidelity equal to heredoc/Python (sha256, exp05 P1). No timing metadata. Parent dirs auto-created (VERIFIED: `evidence/…` paths). |
| `edit_file` | surgical CR-1 changes | success flag | Exact-match replacement; used for +10/-3 server.py and storage.py header changes (exp06 diffstat). |
| `start_process` | servers | pid, `process_id`, log tail, `new_ports` | 704 ms return; survives across calls; requires 0.0.0.0 bind for preview. `stop_process` → `status: stopped` (exp05 P4). |
| `stop_process` | teardown | final status | Clean; only works on managed processes (nohup children unmanageable). |
| `get_process_output` | not needed beyond startup telemetry | — | Available; startup `wait_for` unused because ports arrived with the start result. |
| `web_search` | discovery | ranked results w/ snippets, ids, urls | Condensed paraphrases — orientation-grade (exp05 P3). |
| `fetch_page` | normative extraction | chunked markdown, `hasMore`, title | Chunk 0 of semver.org contained rules 01–11 + BNF; later chunks deliberately not fetched (exp07). |
| `list_connector_tools` | connector probing | status string | `github → unsupported`; status semantics drove delivery fallback (F-10). |
| git (via bash) | checkpoints, blast-radius measurement | normal git output | `git diff --stat <sha>` as adaptation-cost instrument (exp06). |

## Cross-cutting measured properties

- **Idempotence matters:** re-runs after fixes were safe because operations overwrote rather
  than appended (exp03 F3b). Non-idempotent retries: UNKNOWN, untested.
- **Sandbox scope:** files persist under /home/user across calls; processes persist across
  calls too (both servers answered from later calls) but only managed ones are stoppable by
  the platform.
- **Selection rules adopted** (from Exp-05 matrix): servers→start_process; measurement→bash
  with pipefail; known-content files→write_file; generated content→bash/Python;
  discover→search; extract→fetch; kill→by recorded PID.

## Phase-2 timing and heterogeneous tools (F-20; narrow addendum)

**Vocabulary:** *batching* = bundling calls for one user-facing tool request;
*dispatch* = actual invocation; *interval overlap* = measured inside-tool operations
in progress at the same time; *sequential execution* = no such overlap;
*in-process parallelism* = concurrent computation **inside** one tool or program;
*independent workers* = distinct executing entities. Only the first three can be
observed here; interval overlap alone does **not** identify distinct workers/models.

- Historical Exp-08 N=4/8 bash batches had predominantly serial start spacing with short
  adjacent overlaps (F-16). EXP-10's four N=3 **explicit wrapper** batches had 3/3
  pairwise bash interval overlaps each; the prospectively added exploratory matched
  N=4/d=1 control also had 6/6, unlike old T4 2/6. These are **different measured
  conditions**. The invocation/session cause is UNKNOWN, not evidence of a policy/model
  switch. See `experiment-10/RESULTS.md` for raw timestamps, spans and caveats.
- Mixed bash/file invocation: two `write_file` files' mtimes fell *inside* one bash
  interval; a third invalid sibling write failed harmlessly, while healthy writes and
  bash succeeded. **Completion time only** for file tools; file start and runtime remain
  UNKNOWN. The dependent `read_file` was ordered *after* the independent batch by the
  experimenter, not by verified platform dependency detection.
- The bounded `bash(timeout=1)` returned `timeout`/null exit after ~1.325 s but a
  later sentinel established the command finished ~2.00 s after its start; a healthy
  sibling write succeeded. This is one case of **stop waiting**, not a universal kill
  guarantee, independent background-process semantics or retry policy.
- D1 attempted an exploratory direct-control but **submitted only a singleton**:
  no 3-call direct batch was observed. Do not assert that a direct multi-call mode is
  impossible; do not compare D1 span to real batches.
