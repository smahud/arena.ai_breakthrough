# Limitations & Unknowns (explicit, per directive §11)

- **L-1 Self-observation ceiling.** The executing system studied itself. Behavior and artifacts
  are VERIFIED; internal mechanisms (planner representation, model composition, routing) are
  structurally unobservable from inside (F-13). All internal-facing statements in this repo are
  INFERRED/HYPOTHESIS/UNKNOWN by construction. This is the study's hardest boundary.
- **L-2 Sample size.** One environment (this sandbox), one continuous session (~14 min of tool
  time), n=1 per experiment, single actor. No repetition statistics; no cross-platform
  comparison. Generalization beyond this environment is INFERRED at best.
- **L-3 Protected internals out of scope by contract.** Hidden prompts, private routing, model
  identifiers, credentials: not accessed, not probed, not reported (contract rules 4/11). Any
  external claims about such internals would violate this project's contract.
- **L-4 Cross-turn continuity untested.** Exp-04 measured within-session continuity only.
  Constraint survival across user messages/days/compaction: UNKNOWN (H-3).
- **L-5 Scripted vs organic failures.** Exp-03 faults were designed; only one organic failure
  (F-14, exp02 stream B) was observed. Recovery under adversarial/heisenbug classes
  (flaky concurrency, resource exhaustion, network partitions mid-call): UNKNOWN.
- **L-6 Timing measurements are coarse.** 2-vCPU sandbox; `duration_ms` includes platform
  overhead; true parallel-overlap of batched calls not measurable from results (H-1).
- **L-7 No user-in-the-loop stress.** Clarification behavior, interrupt handling, and
  mid-task goal changes *by the user* (as opposed to scripted CR-1) were not exercised.
- **L-8 Reference implementation scale.** `minagent` validates the functional architecture at
  toy scale (dozens of tasks, local tools). Behavior at production scale (hundreds of
  concurrent tools, remote APIs, long horizons) is UNKNOWN.
- **L-9 GitHub delivery unverified end-to-end.** Connector unsupported here (F-10); the
  documented publishing steps in `report/phase-8-delivery.md` are therefore *instructions*,
  not a verified workflow.
