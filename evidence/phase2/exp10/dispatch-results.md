# EXP-10 user-facing tool result envelope (transcribed immediately after each batch)

The `.json` interval files are generated **inside** each bash call and are the raw timing source. This ledger preserves the platform-returned `duration_ms`/status and observed *return ordering*, which the script itself cannot write. Transcription is a first-person observation, not a hidden system trace; verify intervals from JSON. No result is reconstructed from expected timing.

| Batch | Result order observed | Index | `duration_ms` | `exit_code` | Output artifact |
|---|---:|---:|---:|---:|---|
| S1 (3×0.25s) | 1 | 0 | 334 | 0 | `S1-0.json` |
| S1 | 2 | 2 | 337 | 0 | `S1-2.json` |
| S1 | 3 | 1 | 345 | 0 | `S1-1.json` |
| S2 (3×0.25s) | 1 | 0 | 370 | 0 | `S2-0.json` |
| S2 | 2 | 2 | 340 | 0 | `S2-2.json` |
| S2 | 3 | 1 | 358 | 0 | `S2-1.json` |
| L1 (3×0.75s) | 1 | 0 | 883 | 0 | `L1-0.json` |
| L1 | 2 | 1 | 883 | 0 | `L1-1.json` |
| L1 | 3 | 2 | 896 | 0 | `L1-2.json` |
| L2 (3×0.75s) | 1 | 0 | 841 | 0 | `L2-0.json` |
| L2 | 2 | 1 | 840 | 0 | `L2-1.json` |
| L2 | 3 | 2 | 856 | 0 | `L2-2.json` |

## Mixed batch and dependent read (M1)

- Observed one assistant-message `multi_tool_use.parallel` invocation of four **independent** operations. Return order: `marker-a` write **success**; `blocker/child.txt` write **error** (verbatim: `Cannot create directory "arena.ai_breakthrough/evidence/phase2/exp10/blocker": a file already exists at that path`); `marker-b` write **success**; bash M1 **exit_code=0**, **duration_ms=722**. The invalid path was within this experiment's workspace.
- A *later* independent read of `marker-a` returned `EXP10-A healthy, independent write.`; both healthy markers contain their exact text, and no bad child exists. This verifies failure isolation and dependency-respecting orchestration **by our ordering**, not automatic platform dependency detection.
- File completion mtime values vs bash interval: `mixed-analysis.log`. No `write_file` start or per-call duration metadata exists; a file's mtime before bash end is a completion bound, not a precise start time.

## Prospective D1 direct-call control was not executed

After registering the exploratory control in DESIGN.md, **only one** direct `functions.bash`
call was actually submitted (`D1-0.json`, exit 0, `duration_ms=867`). No direct multi-call
envelope was submitted or preserved, and no `D1-1.json`/`D1-2.json` exists: **D1 is a
singleton, NOT an N=3 trial**. Do not compare its span to L1/L2 or assert a protocol
restriction from this incomplete attempt. The primary pre-registered 12 records are complete.

## Exploratory matched control X1 (registered after primary results, before execution)

Four independent direct bash tools within one explicit `multi_tool_use.parallel` wrapper;
returned in order: X1-0 `duration_ms=1126`, exit 0; X1-3 `1114`, exit 0;
X1-1 `1155`, exit 0; X1-2 `1135`, exit 0. Raw `X1-{0,1,2,3}.json`
and `matched-analysis.log`: N=4, d=1.0, span 1.043323 s, **6/6 interval pairs overlap**.
Historical T4 used the same N/d but 4.064 s span and 2/6 overlaps; different
invocation/session remain confounded. Do not count X1 as a pre-registered primary repeat.

## Bounded timeout pair

`write_file` sibling **success**; bash task **status=timeout, exit_code=null, duration_ms=1325**,
stdout contained `TIMEOUT_TASK_STARTED 1793981981536344529`. Later `timeout-end.json` appeared
with end epoch `1793981983536761521` after ~2.00 s: **this command continued after the tool
stopped waiting** under this controlled condition. See `timeout-analysis.log`; do not infer
how all timed-out commands are handled. No server/background job was launched.
