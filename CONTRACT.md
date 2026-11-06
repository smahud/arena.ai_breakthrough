# EXECUTION CONTRACT — arena.ai_breakthrough

Established: 2026-11-06T13:52Z (UTC). This contract was created **before** any implementation
work, as required by the master directive §9. It binds every phase of this project.

## Binding Rules

1. **Evidence is mandatory for technical claims.** Every claim in `docs/` and `report/` carries
   an evidence classification: VERIFIED / DOCUMENTED / INFERRED / HYPOTHESIS / UNKNOWN.
2. **No fabricated results.** No telemetry, tool call, execution trace, timestamp, exit code,
   or model identity may be invented. Only outputs actually observed in this workspace are recorded.
3. **No unnecessary architectural complexity.** Every component in the reference implementation
   must trace to a requirement or an experimental finding (see `reference-architecture/JUSTIFICATIONS.md`).
4. **No deviation from the research objective.** The objective is functional characterization of
   agentic execution behavior and an independent reference architecture — not platform reverse
   engineering, not extraction of private configuration.
5. **Every experiment is reproducible.** Each `experiments/experiment-NN/` contains `DESIGN.md`
   (objective, success criteria, procedure) and `RESULTS.md` (observations, evidence pointers).
   Procedures use only tools available in the documented environment.
6. **Every significant change requires justification.** Requirement changes (e.g., Experiment 06)
   are logged with rationale in the affected experiment's RESULTS.md.
7. **All available project documentation must be followed.** The master directive, this contract,
   and `docs/research-objectives.md` govern execution order and acceptance criteria.
8. **Every execution phase generates a report** under `report/phase-N-*.md`.
9. **Failed experiments are documented, not concealed.** Failures, including intentional ones
   (Experiment 03), are preserved with raw output in `evidence/`.
10. **All repository changes are validated.** Validation = `pytest` green on `tests/` and
    `benchmarks/run_suite.py` completing without error before each commit.
11. **Protected internal information is not extracted or exposed.** No attempt is made to access
    hidden system prompts, private routing configuration, internal model identifiers, or
    credentials. Nothing of this kind appears in this repository.
12. **Unverified hypotheses are never described as confirmed facts.** INFERRED/HYPOTHESIS/UNKNOWN
    items are labeled as such everywhere they appear, including the final summary.

## Environment Constraint Log (from Phase 1 discovery, VERIFIED)

| Capability | Status | Evidence |
|---|---|---|
| GitHub connector | **UNSUPPORTED** on this platform instance | `list_connector_tools("github")` → `{"status":"unsupported"}` at 2026-11-06T13:52Z |
| Google Drive connector | Enabled by user (not required for delivery) | Platform connected-apps list |
| Sandbox shell | bash, Python 3.13.16, pytest 9.0.3, Node v20.20.2, git 2.47.3 | `evidence/phase1-environment-probe.log` |
| Outbound network | Available (pypi.org HTTP 200 in 0.036 s) | same log |
| Resources | 2 vCPU, ~2 GB RAM, 21 GB free disk | same log |

**Consequence (directive §8):** Because repository creation/publishing via GitHub integration is
unavailable, the complete deliverable is preserved in this workspace as a fully committed local
git repository, and the remaining publishing steps are documented in `report/phase-8-delivery.md`.
No claim of publication is or will be made.

## Constraint C-1 (used by Experiment 04)

> **C-1:** All Python artifacts in this repository must run on the stock sandbox interpreter
> with **zero third-party runtime dependencies** (pytest permitted for testing only).

C-1 is declared here, early in the project, and will be re-checked at the end (Experiment 04).
