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
