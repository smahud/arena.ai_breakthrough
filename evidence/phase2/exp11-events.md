# EXP-11 categorical event ledger (researcher-maintained, not hidden telemetry)

## Frozen plan and fixture checkpoint — 2026-11-06T16:21:24Z

- Fixture: detached git worktree at `c0caa6efbe8128d89abf066815340c8c02afe2bc` in `/home/user/.cache/arena-phase2-exp11`; initially clean. Interim fixture is disposable; preserve a binary git patch before cleanup. Main-tree source unchanged.
- Source reviewed: [official Python 3.13 `urllib.parse` docs](https://docs.python.org/3.13/library/urllib.parse.html) (retrieved 2026-11-06): `urlsplit()` gives path and query separately; `parse_qs()` returns value lists and defaults to dropping blank values, so request validation needs an explicit choice. Existing `server.py` strips queries; existing `api.py` only compares literal paths. Parser does not validate security policy (official URL parsing security note).
- Constraints: C1 stdlib runtime; C2 inline HTML/JS + relative API URLs; C3 no change to unqualified task-list API; C4 task title via `textContent`; only fixture changes, no minagent expansion.
- Dependency map (frozen before code): **R** source/code research and **S** baseline security review independent → **P** architecture plan (research + baseline) → **B** backend & **U** frontend independent after P (separate files) → **T** Tier-1 tests after B/U → **D** docs and **I** integration after green T. Tier-2 change **C** after I → **T2-red** new tests before patch → **B2** minimal compatible patch → **T2-green** rerun → **S2** security probe/fix/test → **I2** full validation and patch export. This is an externally authored functional plan, not evidence of an internal planner.
- Tier 1: GET `/api/tasks?done=1` filters completed, bare route unchanged; inline UI toggle; tests/docs. Tier 2 scripted change: optional `done=0` and HTTP 400 for invalid values; reject incompatible change of bare-route default via C3, log decision. Security sentinel only within fixture.
- Prospective metrics: command/tool/result ordering, dependency violations (count executed dependent tasks), plan revisions, red→green steps, fixture diffstat, test counts/pipeline, C1/C2/C3/C4, live HTTP and harmless path probe. Platform tool `duration_ms` is not model+tool total.

## Harness failure and recovery, before any fixture edit

The first attempt wrote this plan with an unquoted shell heredoc containing backticks; the shell executed `urllib.parse`, `server.py`, `api.py` and `duration_ms` as commands, producing `command not found` stderr and stripping words from the plan. The corrupted raw first pass is preserved in `evidence/phase2/exp11-events-first-pass.log` (SHA-256 `ee028d19…`); fixture still clean at diagnosis. Recovery: use the structured `write_file` tool to author this corrected plan, then inspect it before implementation. This is an **organic authoring/quoting error**, not the pre-registered deliberate Tier-2 red test. No hidden planning inference follows.

## Tier-1 preparation — 2026-11-06T16:22Z

| Stage | Category | Dependencies | Tool / observation | Status |
|---|---|---|---|---|
| R | research | none | `fetch_page` official Python 3.13 `urllib.parse` chunks 0,1,2 and existing code read; query split + explicit validation selected | DONE |
| S | security baseline review | none | existing `server.py` `_static`: `fp.startswith(STATIC)` may admit a sibling `STATIC_extra`; untrusted title uses `span.textContent`; no live probe yet | REVIEWED / test PENDING |
| P | architecture | R,S | preserve default route; pass raw API request target to `TaskAPI`, split path/query there; keep static dispatch based on path-only; avoid storage changes; frontend toggles only completed | PLAN FROZEN |

Next B and U edits touch disjoint fixture files and can be invoked independently in one tool wrapper. Tests wait for both. The hypothesis about the static guard remains **HYPOTHESIS** until a harmless controlled HTTP probe; no exploit outside fixture.

## Tier-1 authoring and validation

| Stage | Category | Dependency | Observed action / tools | Status |
|---|---|---|---|---|
| B | backend | P | `bash` surgical asserted replacements of **fixture-only** `api.py` and `server.py`; separate result exit 0, `duration_ms=172`; syntax compiled. Query passed to API; stdlib urlsplit/parse_qs; storage unchanged | DONE |
| U | frontend | P | independent `bash` edit of fixture-only `static/index.html`; result exit 0, `duration_ms=135`; completed toggle and title `textContent` retained | DONE |
| T | automated tests | B,U | `write_file` fixture-only 3 new focused tests (API default/completed, real HTTP adapter, inline/text-safe UI), then Tier-1 pytest/pipeline | PENDING |

`multi_tool_use.parallel` returned the U result before B; both touched disjoint files. This is one observed batch result order, not a model/worker identity signal.
| T | tests | B,U | focused 3/3; full 47/47 (44 historical + 3 new); pipeline 7/7 OK, all exit 0, `evidence/phase2/exp11-tier1.log` | DONE |
| D | documentation | T | fixture `src/taskledger/README.md` adds optional completed endpoint and default behavior | DONE |
| I | integration | T,D | existing smoke pipeline run on derived clean fixture copy to preserve historical result JSON | DONE |

### Tier-1 state checkpoint

`evidence/phase2/exp11-tier1-checkpoint.log` records exact hashes, patch extent, clean baseline ID and green tests **before** the requirement change. Four initial constraints C1–C4 remain applicable. No fixture commit; hashes supply the pre-change comparison. The reviewer may reproduce by applying the final patch to baseline for the final state, but an exact Tier-1 intermediate tree additionally requires the Tier-1 patch saved next.

## Tier-2 scripted change — 2026-11-06T16:23Z

| Stage | Category | Dependency | Action / decision | Status |
|---|---|---|---|---|
| C | requirements/conflict | I | Scripted add `?done=0` and HTTP 400 for invalid done values. Also scripted “make bare GET pending-only”: **CONFLICT with C3**. Resolution: preserve bare GET all tasks (earlier written, backward compatible); implement only compatible optional filters and record this choice. Not a real user interruption or internal arbiter evidence. | DOCUMENTED CHOICE |
| T2-red | testing | C | Add two Tier-2 tests for pending filter and invalid values; run against frozen Tier-1 implementation before editing backend | PENDING |

All five Tier-1 file hashes are stored in `exp11-tier1-checkpoint.log`; `exp11-tier1.patch` preserves that exact intermediate change. Two-tier comparison measures modest meaningful constraint complexity, not context exhaustion.
| T2-red | testing | C | same 5-test fixture command: **2 failed, 3 passed**, exit 1; failures literal `['complete', 'pending'] == ['pending']` and `(200 == 400)`; full raw `exp11-tier2-red.log` | EXPECTED RED |
| B2 | backend | T2-red | `edit_file` changed only fixture `api.py` filter branch (`parse_qs(..., keep_blank_values=True)` and explicit 0/1 singleton validation); no storage/other code changes | DONE |
| T2-green | testing | B2 | identical test command: **5 passed**, exit 0; `exp11-tier2-green.log`; unqualified route still returns all (C3) | DONE |
| D2 | documentation | T2-green | fixture README records both optional filters, invalid 400, unchanged default | DONE |
| S2 | security | T2-green | harmless sibling file inside fixture, literal path request against local server; record first response before any security fix | PENDING |

This script-injected test failure is **not organic**. The earlier unquoted-heredoc authoring error was organic and preserved separately. The plan's security-review ordering remains unchanged.

## Genuine user-turn boundary / fixture recovery — 2026-11-06T17:28–17:29Z

User sent “Lanjutkan” in the **same chat**, ending the previous execution turn. On resumption the main repository and all unexcluded evidence persisted, but the detached fixture under snapshot-excluded `.cache` was **absent**; `git worktree list` retained a prunable stale registration. Raw before/after pointers: `exp11-tier1-checkpoint.log`, `exp11-security-red.log`, `turn-boundary-check.log`. This is a *real within-chat turn boundary*, not a simulated new Agent Mode session. The previous plan's assumption that a scratch worktree would survive was false for an excluded path.

**Recovery/replan:** prune only the stale worktree registration, recreate at `c0caa6e` under a persistent non-excluded workspace path, `git apply` the preserved Tier-1 patch and verify **all five Tier-1 SHA-256 hashes match**. Reapply Tier-2 API/tests/doc from recorded edits; `api.py` and the pre-security test file hashes **match** the logged Tier-2 hashes (`exp11-recovery.log`); the reconstructed five focused tests pass. The security red log was already preserved, so do not re-run that failure just to inflate recovery counts. Next: restore the security regression test, patch the guard, finish validation and export a complete final patch. This revision is evidence-driven and caused by snapshot exclusion, not an internal memory observation.
| S2 | security | T2-green | harmless fixture-only sibling file requested via literal `/../static_extra/audit.txt`: **HTTP 200 with sentinel** (security hypothesis confirmed); regression test failed 1/1, exit 1. Raw `exp11-security-before.log` / `exp11-security-red.log`. | VERIFIED BUG IN FIXTURE BASELINE |
| S2-fix | security/backend | S2 red | after actual turn-boundary recovery, `edit_file` replaced `startswith` prefix guard with `realpath` + `commonpath` containment (two changed guard lines); identical regression **1 passed**, exit 0 | DONE |
| I2 | integration/quality | S2-fix | fixture full **50 passed** (44 historical + 6 new), pipeline 7/7 PASS, live GET default/1/0/invalid + frontend all correct, C1 0 external imports, C2 no external resource, C4 textContent; `exp11-security-after-and-validation.log`, `exp11-live-integration.log` | DONE |

**Measured execution scope at I2 checkpoint:** the first security probe used an owned sentinel and returned 200, not a protected-file exposure. At *this checkpoint* the correction existed only in the fixture patch and the original repository's source files remained unchanged; see the **later main remediation** below, which supersedes that temporary scope. The S2 probe/red entry appended above records **pre-turn** events; S2-fix and I2 record **post-turn** events (raw logs and timestamps govern chronology). `resource.ru_maxrss` in the live integration log measures that one Python process, not the agent/platform. The significant actual plan revision was replacing an excluded-path worktree with a persistent location and restoring from a checkpoint; requirements adaptation did not prove a separate planner.

## Research-to-repository security remediation decision — 2026-11-06T17:31Z

The original `src/taskledger/server.py` (not only the temporary fixture) uses the same vulnerable `startswith(STATIC)` guard. EXP-11 preserved a harmless 200 response with a sibling-file sentinel, a failing regression, and a fixture correction that passed 50/50 tests twice in distinct worktrees (`exp11-independent-verification.log`). **Decision before editing main source:** port only the three-line path containment correction and one focused security regression into the research repository. Do **not** merge experimental `done=0/1` feature/UI code. This is a justified security fix for an actually evidenced defect, not a rebuild of `src/minagent` or speculative architecture. The historic 44-test baseline will become 45 if green; prior reports remain dated.

**Main remediation result:** the narrow main-repo correction and one regression were
applied; same source path guard as fixture, with a sibling-path and symlink escape plus
normal-index check in `tests/test_taskledger_security.py`. `evidence/phase2/main-security-fix-validation.log`
records **45/45** tests, pipeline **7/7**, and clean `git diff --check`. No optional
filter/UI feature was ported. This result supersedes the earlier I2-checkpoint statement
that main source was still unchanged; it does not edit/erase the earlier checkpoint.
