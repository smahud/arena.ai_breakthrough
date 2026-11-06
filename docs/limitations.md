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
- **L-5 Scripted vs organic failures.** Exp-03 faults were designed; organic failures observed:
  three (F-14 exp02 stream B; minagent test expectation, phase-6; audit false positive, F-08).
  Transient/flaky class now tested via a deterministic counter-file model (Exp-09, F-17);
  genuinely nondeterministic flakiness, resource exhaustion, and network partitions mid-call
  remain UNKNOWN.
- **L-6 Timing measurements are coarse.** The historical sandbox had 2 vCPU;
  `duration_ms` includes platform overhead. Exp-08's *in-call epoch files* independently
  measure mostly serial bash execution with short adjacent overlap (F-16), correcting the
  original “not measurable” assessment for **bash**. Worker count, scheduling mechanism,
  non-bash start times, and other environments remain UNKNOWN.
- **L-7 No user-in-the-loop stress.** Clarification behavior, interrupt handling, and
  mid-task goal changes *by the user* (as opposed to scripted CR-1) were not exercised.
- **L-8 Reference implementation scale.** `minagent` validates the functional architecture at
  toy scale (dozens of tasks, local tools). Behavior at production scale (hundreds of
  concurrent tools, remote APIs, long horizons) is UNKNOWN.
- **L-9 GitHub delivery unverified end-to-end (HISTORICAL, SUPERSEDED).** The original
  connector-only conclusion was valid for the first delivery attempt, not the later authorized
  REST+git publication. Public repo and remote HEAD were independently verified in Phase 2
  (`evidence/phase2/baseline-repository-probe.log`, F-19). This new session's *write access*
  and any Phase 2 push remain UNKNOWN until independently verified. Original wording is
  preserved in `report/phase-8-delivery.md` under “Original report.”

## Phase-2 update to dated limitations (original wording retained above)

- **L-2 scope:** Phase-1's “one continuous session, n=1” referred to its own trials.
  EXP-10 ran 4 primary batches with **two repeats per duration**, plus one
  prospectively-added exploratory matched N=4/d=1 batch. EXP-11 is **one engineering
  case**, followed by a new-worktree **artifact replay** (not an independent agent run)
  and a real within-chat user turn. No cross-platform or multi-model sample exists.
- **L-4 refined:** a genuine *same-chat* user-message boundary occurred during EXP-11,
  revealing loss of one excluded `.cache` fixture and survival of its persisted patch/git
  artifacts (F-21); a second same-chat turn retained the *new* persistent worktrees and
  uncommitted draft (`second-turn-check.log`). Cross-**new-chat** constraint resolution,
  days-later continuity and
  automatic **compaction events** are still UNKNOWN/PENDING. Public documentation of a
  compaction feature is not an observed compaction occurrence.
- **L-5 scope:** EXP-11's requirement change and red security regression were scripted;
  the original static-file guard defect was independently observed through an owned
  sibling-path probe (F-22). No claim of general security coverage or production
  resilience follows.
- **L-6 refined:** F-16's mostly serial pattern was scoped to its original conditions;
  F-20 finds **all-pair overlap** in a different explicit-wrapper batch, including a
  matched N=4/d=1 exploratory trial. The match rules out **N/d alone** as a sufficient
  explanation under that wrapper, but invocation/session and other differences remain
  confounded. File-tool *completion*, not start, was measured; workers/models UNKNOWN.
- **L-7 retained:** the real “Lanjutkan” turn was not a user-originated change in task
  goal; clarification/interrupt stress and long-horizon feedback remain untested.
- **L-9 actual delivery outcome (2026-11-06T17:40Z):** the prior sentence was the
  **pre-attempt** rule. After local commits, an authorized, noninteractive, no-force
  `git push --dry-run` to the public repository failed **exit 128**: `could not read
  Username for 'https://github.com': terminal prompts disabled` (no credential helper,
  no `origin` in this snapshot; `github` connector `unsupported`). No real push was
  attempted; anonymous remote master still `79412fd`. Phase-2 commits are **local,
  unpublished**, not falsely described as delivered. Full transcript:
  `evidence/phase2/publication-attempt.log`. A later supported authorization can
  unblock a fast-forward push; no token should be pasted or stored in the repo.
