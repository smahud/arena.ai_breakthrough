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
