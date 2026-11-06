# Experiment 05 — RESULTS

Executed: 2026-11-06T13:54–14:00Z. Evidence: `exp05-p1-hashes.log`, `exp05-p2-runners.log`,
`exp05-p4-lifecycle.log`, `exp07-semver-spec.md` (P3).

## P1 — File authoring (VERIFIED)

Same 92-byte canonical payload via `write_file` tool, bash heredoc, Python `open().write()`:
sha256 `e04bec28…` identical across all three (1 distinct hash / 3 methods). Earlier 2541-byte
generated payload also matched between Python write and source (`21408dfb…`).
→ Authoring fidelity is tool-independent; selection is about *ergonomics/telemetry*, not integrity.
Platform-tool note: `write_file` results carry no timing metadata; bash results carry
`duration_ms` + exit code — bash is the only self-measuring authoring path here.

## P2 — Test runners (VERIFIED; highest-impact finding)

Same 10-test module: `pytest -q` → `10 passed`, wall 341 ms. `unittest discover` →
**`Ran 0 tests … NO TESTS RAN`**, wall 57 ms.
→ Runner must match test style. The dangerous property is the *signal*, not the speed:
an unconfigured runner can return "success-shaped" output with zero coverage. Any validation
step must assert **test count > 0**, not merely exit status. (Feeds reference implementation:
`validator.py` false-green guard.)

## P3 — Spec retrieval (VERIFIED)

`web_search` → condensed paraphrase of precedence rules (orientation-grade).
`fetch_page(semver.org)` → full numbered normative text + BNF grammar (implementation-grade).
→ Pattern: search to discover, fetch to extract. EXP-07 was implementable only from the fetch.

## P4 — Server lifecycle (VERIFIED; two failure modes observed)

| Aspect | `start_process` | `nohup &` inside bash |
|---|---|---|
| Call return | 704 ms, structured: pid, log tail, listening ports | **30 s timeout**, `exit_code: null` — background process held the call's pipe open |
| Work actually done | server up | server up after ~1.5 s; remaining ~28.5 s dead time |
| Survives across calls | yes (HTTP 200 from later call) | yes (HTTP 200 from later call) |
| Managed stop | `stop_process` → `status: stopped` | none; required manual `pkill` |
| Cleanup hazard | none observed | `pkill -f "taskledger.server 8198"` **killed the invoking shell itself** (pattern matched the shell's own cmdline, pid 2013) → call truncated, `exit_code: -1`; verified post-mortem: target died, session survived at platform level |

## Selection matrix (S2)

| Task class | Tool chosen after measurement | Why |
|---|---|---|
| Long-running server | `start_process` | managed lifecycle, fast return, port telemetry |
| One-shot scripts/tests | `bash` (+`set -o pipefail`) | exit codes + timing |
| Small known-content files | `write_file` | atomic, no shell quoting hazards |
| Generated/templated files | bash heredoc/Python | programmatic content |
| Fact discovery | `web_search` | breadth |
| Normative extraction | `fetch_page` | full text |
| Process cleanup | record PID at launch; kill by PID | `pkill -f` self-match hazard |

## S3 — behavior-changing differences: 3 documented (pipefail adoption, false-green guard,
PID-based cleanup). MET.

## Phase 2 P1 evidence correction (2026-11-06)

The original “92-byte canonical” is **REFUTED** by `wc -c` on all three preserved files:
**122 bytes each**, hash `e04bec28…` equal across the three methods. The “2541-byte … also
matched” statement has no corresponding preserved source/target or hash log and is **UNKNOWN**
under the evidence contract. The claim of fidelity is scoped to **one 122-byte three-method
trial**, not arbitrary sizes. Original statements are retained above as a historical record;
check `evidence/phase2/baseline-evidence-crosscheck.log` and
`report/phase2-baseline-audit.md` C06.
