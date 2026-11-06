# Experiment 07 — Research-to-Implementation

**Objective (RQ1, RQ3):** Convert external normative documentation into a validated executable
artifact, observing source evaluation → design → implementation → validation.

**Task:** Implement a SemVer 2.0.0 parser/comparator (`src/semverlite/`) derived from the
official specification at semver.org, retrieved live via `fetch_page` (tool choice recorded for
Exp-05 P3; `web_search` used first as discovery layer).

**Procedure:** (1) retrieve spec; (2) extract the normative precedence rules and the official
regex *from the fetched text* (quote it in RESULTS.md); (3) implement parser, precedence
comparison, and pre-release/build-metadata rules; (4) validate against the spec's own worked
example (`1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 <
1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0`) plus edge cases; (5) commit.

**Measurable success criteria:**
- S1: RESULTS.md quotes spec text that literally appears in the saved fetched page
  (`evidence/exp07-semver-spec.md`).
- S2: The full official precedence chain sorts correctly (pytest, exit 0).
- S3: Invalid versions (e.g., `1.0`, `01.2.3`, `1.0.0-`, `v1.0.0`) are rejected per spec.
- S4: Zero third-party imports (C-1 holds under new work).

**Evidence:** `evidence/exp07-semver-spec.md` (fetched page), `evidence/exp07-tests.log`.
