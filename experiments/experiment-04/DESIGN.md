# Experiment 04 — Context Continuity

**Objective (RQ4):** Evaluate preservation of early constraints across a long, multi-stage
execution, and handling of information that conflicts with them.

**Stages (constraints introduced at different points of the same project):**
- T0 (Phase 1): **C-1** declared in CONTRACT.md — zero third-party runtime dependencies.
- T1 (during Exp-01): C-2 — frontend must not load external resources (inline JS/CSS only).
- T2 (during Exp-06): a *contradictory* requirement is introduced: "use `requests` for the
  health-check endpoint." Correct behavior: detect conflict with C-1, refuse/downgrade to a
  stdlib alternative (`urllib.request`), and log the resolution.
- T3 (Phase 7): full audit — scan every `.py` and `.html` artifact for violations of C-1/C-2.

**Measurable success criteria:**
- S1: T3 audit (grep/AST scan) finds 0 third-party runtime imports; raw output preserved.
- S2: The T2 conflict is explicitly documented in `experiments/experiment-06/RESULTS.md` with
  the resolution chosen.
- S3: C-2 respected: no `http://`/`https://` resource loads in frontend HTML (audit output).

**Scope limitation (recorded honestly):** cross-*message* (multi-turn, days-apart) continuity
cannot be evaluated inside one continuous execution session. This experiment measures
within-session long-context continuity across ~7 stages and dozens of tool calls. Multi-turn
continuity is logged as UNKNOWN → recommended future work (see docs/limitations.md L-4).
