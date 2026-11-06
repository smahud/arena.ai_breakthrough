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
