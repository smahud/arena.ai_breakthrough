# Experiment 05 — Tool Selection

**Objective (RQ3):** Given tasks solvable by multiple authorized tools, observe which tool is
chosen, and measure reliability/efficiency differences empirically.

**Comparisons (each run ≥3 trials, timed by the platform's own `duration_ms` on bash results
and by `time` inside the shell):**
- P1 *File authoring*: `write_file` tool vs `bash` heredoc vs Python `open().write()` —
  identical ~2 KB payload; compare integrity (sha256 equality) and overhead.
- P2 *Test running*: `pytest` vs `python -m unittest` on the same test module — compare
  duration and output verbosity (Exp-01 suite is the subject).
- P3 *Spec retrieval*: `web_search` vs `fetch_page` for obtaining the SemVer 2.0.0 spec
  (feeds Experiment 07) — compare precision of retrieved normative content.
- P4 *Server lifecycle*: `start_process`/`stop_process` vs backgrounding with `nohup &` inside
  bash — compare controllability (documented platform guidance says bash must not host
  long-running servers; verify what actually happens).

**Measurable success criteria:**
- S1: All P1 outputs byte-identical (sha256 match recorded).
- S2: A selection matrix in RESULTS.md maps task class → tool chosen → measured cost.
- S3: At least one observed behavioral difference that changes future tool choice, documented
  with evidence (not merely asserted).

**Evidence:** `evidence/exp05-p{1..4}-*.log`.

## Phase 2 evidence correction (2026-11-06)

The planned P1 “~2 KB payload” was not what the three preserved canonical artifacts show:
all are **122 bytes** and share a SHA-256. This dated design is preserved as pre-registration;
report only the **executed** size as VERIFIED. The extra 2541-B assertion in RESULTS has no
matching preserved raw artifact and remains UNKNOWN (audit:
`evidence/phase2/baseline-evidence-crosscheck.log`).
