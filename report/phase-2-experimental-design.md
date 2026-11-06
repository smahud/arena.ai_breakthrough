# Phase 2 — Experimental Design Report

**When:** 2026-11-06T13:53–13:54Z. **Artifacts:** `experiments/experiment-0N/DESIGN.md` ×7.

## Design decisions
- All 7 directive workloads (Exp-01…07) instantiated; each DESIGN.md fixes objective,
  measurable success criteria (S1…S4), procedure, evidence paths, and observation targets
  **before** execution (contract rule 5).
- Cross-experiment coupling was deliberate and documented: Exp-05 P2 reuses Exp-01's suite;
  Exp-05 P3 feeds Exp-07; Exp-04 stages T0–T3 span the whole session; Exp-06 mutates Exp-01's
  artifact. This maximizes distinct evidence per unit of execution (directive §3: avoid
  redundant tests).
- Fault-injection honesty clause added to Exp-03 (scripted faults study loop *shape*, not
  spontaneous discovery); Exp-04 scope limitation (single session) declared upfront.
- 7 designs written as 7 parallel `write_file` calls in one dispatch (F-01 pattern).

## Criteria-quality self-check
Every S-criterion is mechanically checkable (exit codes, hashes, grep, diffstat, quoted log
text). No criterion relies on subjective judgment.

## Deviations
None at design time. (One design gap surfaced later in execution: Exp-02 S4's wall-clock
overlap turned out unmeasurable from tool results — recorded as PARTIAL/UNKNOWN in RESULTS
rather than retro-fitting the criterion.)
