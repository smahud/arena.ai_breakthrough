# Experiment 03 — Failure Recovery

**Objective (RQ3, RQ4):** Observe diagnosis → correction → retry → verification behavior under
controlled, harmless failures.

**Fault injections (3 classes):**
- F1 *Compile-time*: syntax error in a module (caught before execution).
- F2 *Logic/test-time*: off-by-one in a pure function caught by its test suite.
- F3 *Runtime/environment*: command invokes a nonexistent binary (exit 127 class) and a script
  that fails mid-way leaving partial state, requiring cleanup awareness.

**Procedure:** For each fault: (1) write faulty artifact; (2) execute, capture full stderr/stdout
and exit code via `tee` to evidence; (3) diagnose *quoting the actual error text*; (4) apply
minimal fix; (5) re-execute; (6) verify green. All raw output preserved even for failed runs.

**Measurable success criteria:**
- S1: Each fault's first (failed) run is preserved with nonzero exit code in `evidence/`.
- S2: Each diagnosis in RESULTS.md quotes a string that literally appears in the captured log.
- S3: Every failed run is followed by a passing run of the same command (exit 0).
- S4: Fixes are minimal — measured by diff line count (target ≤5 changed lines per fault).

**Honesty rule:** the failures here are *scripted by design*; what is studied is the recovery
loop's observable shape (detect → locate → minimal patch → re-verify), not whether failures
"surprised" the system.
