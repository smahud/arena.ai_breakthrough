# Public Capabilities of the Studied Environment

What any authorized user of this environment can observe (no protected information; this is
the user-visible tool palette plus measured sandbox properties).

## Capability surface (as exercised in this study)

- **Sandboxed workspace** at /home/user with cross-message file persistence; bash with
  structured telemetry (stdout/stderr/exit_code/duration_ms/timeout).
- **File tools:** create/overwrite, surgical edit, read (text + images), present-to-viewer.
- **Process tools:** managed background processes with pid/log/port reporting and clean stop;
  live-preview proxying for bound 0.0.0.0 ports.
- **Web tools:** ranked search with snippets; full-page fetch with chunking.
- **Connectors:** per-app loading protocol with explicit statuses (`enabled` / `disconnected`
  / `disabled` / `unsupported`). On this instance: google_drive enabled by the user;
  **github connector unsupported** (F-10); repository publication via a separate, explicitly
  authorized REST+git route was verified later (F-19). Connector availability and GitHub
  repository delivery are distinct capabilities.
- **Media generation tools** (image/speech) exist in the palette; unused here — not needed by
  any experiment (contract rule 3: no speculative use).
- **Measured sandbox:** Python 3.13.16, pytest 9.0.3, Node v20.20.2, git 2.47.3, 2 vCPU,
  ~2 GB RAM, ~21 GB free disk, outbound HTTPS (pypi.org 200/36 ms) — `phase1-environment-probe.log`.

## Capability boundaries observed

- bash calls stop waiting at timeout; background processes inside bash are unmanaged (F-04).
- File snapshots exclude dependency/cache dirs and credential paths (platform-documented).
- Connector tools are unavailable until loaded; unsupported slugs return a terminal status.
- No telemetry about the acting model itself beyond tool results (F-13).

## What is deliberately NOT claimed here

Model identity, internal architecture, hidden prompt content, private routing — see
`docs/limitations.md` L-1/L-3 and `docs/architecture-analysis.md` §5.

## Phase 2: current official documentation vs this session (retrieved 2026-11-06 UTC)

Source publication/update dates and short excerpts are preserved in
[`evidence/phase2/public-docs-sources.md`](../evidence/phase2/public-docs-sources.md).
Help-center pages display **relative** last-update labels; no invented exact date. A
DOCUMENTED product feature is not automatically VERIFIED in *this* session.

| Capability | Official source (published/update date where given) | Documented behavior vs observation here | Classification / discrepancy |
|---|---|---|---|
| Workflow orchestration | [Agent Mode Help](https://help.arena.ai/articles/5432423882-how-to-use-agent-mode) (last updated “29 days ago” at retrieval); [launch blog](https://arena.ai/blog/agent-mode) (4/5 Jun 2026) | Multi-step planning/tools DOCUMENTED; Phase 2 externally wrote a plan before EXP-11 and revised a scratch-location choice. | Plan *artifact* VERIFIED; internal planner boundaries UNKNOWN. |
| Tool execution | same Help article; this session's supported tool descriptions | Web, bash, files and sandbox DOCUMENTED; EXP-10's explicit wrapper showed all-pair interval overlap, mixed failure isolation and one timeout that stopped waiting while the bounded command completed. | Scoped VERIFIED (F-20); does not establish universal scheduling or worker count. |
| Model selection and task routing | [Agent Mode Help](https://help.arena.ai/articles/5432423882-how-to-use-agent-mode) (relative update); [Max blog](https://arena.ai/blog/max-router-tops-agent-arena) (12/14 Oct 2026) | Help describes a session-selected orchestrator with possible reliability switch; separate blog describes an agentic router. Neither exposes the model or route **for this session**. | Product statements DOCUMENTED; model identity/router usage here UNKNOWN. A fingerprint cannot identify either. |
| Session configuration / repository workflow | [Coding Help](https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode) (relative update “2 months ago”); [coding blog](https://arena.ai/blog/coding-in-agent-mode) (24/26 Aug 2026) | Connected GitHub repo: sandbox copy, working branch, diff, commit, PR and checks window DOCUMENTED. This session's `github` connector returned `unsupported` (rechecked on continuation); public git clone works independently. | Supported product-wide, not enabled here: scoped availability distinction, not product contradiction. A Phase-2 noninteractive git push **dry-run** to the public URL failed exit 128 (no username/credential), so no Phase-2 push occurred; other authorized workflows remain untested. See `evidence/phase2/publication-attempt.log`. |
| Context management | [Token-limit Help](https://help.arena.ai/articles/3975292349-arena-troubleshooting-session-token-limits) (relative update “4 months ago”) | Agent Mode compaction described as built-in; no automatic *conversation-context transfer* to a fresh chat described. On the actual continuation turn, normal workspace/git persisted but excluded `.cache` fixture did not. | Compaction DOCUMENTED, event in these runs UNKNOWN; workspace snapshot behavior VERIFIED narrowly (F-21), not a new-chat context test. |
| Execution reporting | [Coding Help](https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode) | Diff and Checks panels DOCUMENTED for connected GitHub workflow; our bash results exposed stdout, stderr, exit codes/duration, but no model/token/planner trace field (F-13). | Panels not exercised here; per-call tool telemetry VERIFIED; hidden routing/planning UNKNOWN. |
| External integrations | [Connectors blog](https://arena.ai/blog/connectors-in-agent-mode) (27 Oct 2026); [Connect-apps Help](https://help.arena.ai/articles/6934758149-connect-your-apps-to-arena) (relative update “8 days ago”) | Opt-in per-turn connectors DOCUMENTED; `google_drive` enabled in conversation but unused; `github` tool lookup returned `unsupported` in this environment. | General availability DOCUMENTED; this session's scoped status VERIFIED. No access to disabled/disconnected apps attempted. |

**Scope note:** historical measured sandbox versions/resources above are dated Phase-1 values,
not promises about every new session. EXP-10 demonstrated that an explicit wrapper's execution
pattern can differ markedly from EXP-08's old batch: do not extrapolate either result to all
tools or infer a hidden switch of models. Public documentation is not internal telemetry.
