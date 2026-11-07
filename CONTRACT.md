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

## Phase 2 continuation addendum — 2026-11-06 (supersedes delivery status above)

The preceding **Environment Constraint Log and Consequence** are a dated Phase-1 snapshot,
not the current delivery verdict. The GitHub connector was `unsupported` at that time and
remains unsupported in this session; nevertheless, a later user-authorized REST+git workflow
published the repository, first privately at 15:08Z and then publicly at 16:03Z on explicit
authorization. See `report/phase-8-delivery.md` UPDATE,
`evidence/delivery-verification.log`, and Phase 2's anonymous API/remote-HEAD check in
`evidence/phase2/baseline-repository-probe.log`. Current baseline: **PUBLIC**. An unsupported
connector does not negate other authorized delivery paths; it never authorizes use of
credentials the user has not supplied. Phase 2 must independently verify its own push; prior
publication does not grant this new session write access.

Rules 1–12 remain binding. Phase 2 additionally distinguishes **REFUTED** (a prior claim
contradicted by evidence) from UNKNOWN; records question, hypotheses, alternatives, variables,
controls, measurements, raw observations, results, limits, and reproduction steps for each new
experiment; and preserves historical evidence rather than overwriting it. Because
`benchmarks/run_suite.py` writes tracked `evidence/run-suite-result.json`, run the full pipeline
in a clean `git archive` copy before each commit (or save the newly generated result to a
separate Phase 2 evidence file without replacing the earlier result). Run tests and pipeline
green before each commit, record exit codes, and keep root `report/` phase reports. Neither
research security boundaries nor anti-overengineering requirements are relaxed.

## Phase-2 publication outcome addendum — 2026-11-07 (delivery status only)

The preceding Phase-2 “must independently verify its own push” was a pending condition
**at that time**. The user later explicitly supplied a PAT for this repository; authorized
non-force direct HTTPS git push moved public `master` from `79412fd` to closing report
`600f762`, and independent anonymous Git/API requests confirmed that HEAD, the commit and
the report. See `report/phase2-publication.md`, `evidence/phase2/publication-success.log`.
GitHub connector remained `unsupported`. Rule 11's ban on extracting protected *internal*
credentials remains in force: the research did not probe for them; a user-supplied delivery
credential was used only for the requested push and not written into repository
files/config/URL. Because the user pasted it in this chat/tool input, recommend
revoking/rotating it after publication. The earlier failed no-auth dry-run remains
preserved separately; it was not retroactively changed into a success.

## Constraint C-1 (used by Experiment 04)

> **C-1:** All Python artifacts in this repository must run on the stock sandbox interpreter
> with **zero third-party runtime dependencies** (pytest permitted for testing only).

C-1 is declared here, early in the project, and will be re-checked at the end (Experiment 04).
