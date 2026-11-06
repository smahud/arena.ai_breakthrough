# Phase 2 research plan — pre-registration (2026-11-06)

**Baseline:** public `smahud/arena.ai_breakthrough`, `master` at `79412fd` before audit; audit commit `c0caa6e`. Nine historical experiment pairs, F-01…F-18 plus retrospective F-19, 44/44 tests; see [`../report/phase2-baseline-audit.md`](../report/phase2-baseline-audit.md). Scope: **behavior through supported tools**, not private orchestration or model identity. No expansion of `src/minagent` is planned.

## Research questions and functional hypotheses

These are **not mutually exclusive**, and none entails a distinct physical model, process, or hidden agent. H-A1 vs H-A2 in particular may be observationally equivalent. Preregistered measurements belong to EXP-10/11 below; a negative discrimination result is valid.

| Hypothesis | Predicted observable behavior | Plausible alternatives | Experiment / discriminative observation / inference boundary |
|---|---|---|---|
| **H-A1 unified execution policy** | Coherent tool choices and feedback-driven action across research, code, review and reporting; plan may be revised in place. | A separated planner could generate the same sequence; scripted plans or a human-written spec could produce apparent coherence. | EXP-11 measures ordering, prewritten plan vs action, repair and change handling. **No observable result can prove a unified internal process** absent authorized internal traces. |
| **H-A2 functionally separated planning/execution** | Inspectable plan with dependencies precedes actions; dependent work waits; feedback can trigger an explicit revision. | The same generative process can write a plan and then follow it; researcher-imposed design can cause phase separation. | EXP-11 freezes a written plan/checkpoint before implementation, measures whether actual order and revisions align. This tests a *functional* stage, not a distinct internal planner component. |
| **H-A3 specialized execution pathways** | Consistent differences by task category in tools, validation, error handling, scheduling. | Task-specific constraints, file types, and one unified policy adapting to inputs can cause the same differences. | EXP-11 compares categories and matched checkpoints; EXP-10 compares bash vs file tools. **Even a category fingerprint cannot identify separate models/workers**. |
| **H-A4 adaptive execution policy** | Observable change in action sequence/tool or validation strategy after a controlled failure and mid-workload change; unaffected tasks remain isolated. | Fixed scripted contingency or ordinary test-driven development may look identical. | EXP-11 has predeclared compatible change + conflicting clause and a red test; compare before/after tool/result/order; classify strategy change, not cause or internal policy. |

### Execution vocabulary

- **Batched invocation:** multiple independent tool requests in one assistant message.
- **Concurrent dispatch:** those requests sent together; does *not* imply simultaneous work.
- **Interval overlap:** measured start/end of work intersect. **Sequential execution:** no overlap; **mostly serial:** span scales with N despite limited adjacent overlap.
- **In-process parallelism:** threads inside a single sandbox process (minagent tests); distinct from platform batching.
- **Independent execution workers:** requires direct authorized evidence beyond timings; **UNKNOWN** here.

## Experiment-priority matrix (judgments fixed before Phase 2 trials)

Scale H/M/L describes relative expected information gain (IG), discrimination (D), reproducibility (R), execution cost (C), risk (T), and overlap with completed work (O); not numerical probability or confidence. Cheaper first where IG/D comparable.

| Candidate | IG | D | R | C | T | O | Decision and rationale |
|---|---|---|---|---|---|---|---|
| **EXP-10:** vary bash duration at fixed N + mixed bash/file batch, failure, timeout | H | H for timing model; L for worker identity | H | L (seconds) | L | M (extends Exp-08 beyond bash) | **SELECTED** — smallest direct test of whether Exp-08's timing pattern generalizes to duration and mixed tools; no app code. |
| **EXP-11:** controlled heterogeneous taskledger maintenance in an isolated worktree | H | M for *functional* adaptation, L for internal partitioning | H (committed base + patch/tests) | M | L (sandbox fixture only) | M (extends Exp-01/06 with categories, real security gate) | **SELECTED** — one compact workload covers planning, specialization, recovery, security, change handling and context checks. |
| Review current official Agent Mode docs vs exercised interface | M | M for public claims vs observations, L for internals | H | L | L | L | **SELECTED**, documentation research, not a platform experiment. Record publication/retrieval dates, classify DOCUMENTED vs VERIFIED. |
| True new-chat continuity with future contradiction | H | M for context-vs-artifact retention | H if user starts new session | Requires real future session | L | L | **PENDING** — checkpoint and exact handoff now; never simulate session boundary. |
| Forced context exhaustion/compaction | M | L without compaction telemetry | L | H | M | L | **DEFER** — use meaningful tiered constraints in EXP-11 instead; no arbitrary filler. Official docs can establish DOCUMENTED availability, not a compaction event in this run. |
| Rebuild agent, message bus, database, remote worker | L | L | L | H | H | H | **REJECT** — no verified functional need. |

## Selected procedures, links, and measurement boundary

- **EXP-10:** [`../experiments/experiment-10/DESIGN.md`](../experiments/experiment-10/DESIGN.md) → independent timed bash intervals + mixed tool artifacts in `evidence/phase2/` → scoped scheduling/failure findings (next available new IDs **F-20+ only after results**). No internal worker-count claim. Two short and two long trials (N=3), a mixed batch with a harmless invalid file path, a bounded timeout call, and a dependency-respecting separate read.
- **EXP-11:** [`../experiments/experiment-11/DESIGN.md`](../experiments/experiment-11/DESIGN.md) → `git worktree --detach` of audit commit in ignored `.cache`, categorized event log + reproducible `git diff` patch → functional/quality/continuity findings (only if supported). Reuse taskledger and its 44-test validation pipeline; source repository's `src/minagent` unchanged.
- **DOC review:** official Arena help/blog pages retrieved 2026-11-06, preserved as short quotations + URLs under `evidence/phase2/`; update `docs/public-capabilities.md` with documented vs tested matrix. This session's GitHub connector `unsupported` does not contradict product-wide availability; it does limit our current integration workflow.

## Behavioral fingerprint: prospective schema and scoring rules

A *fingerprint is a comparison vector*, never a model identifier. For each workload/trial record: baseline commit, task category, requirement tier, constraints, dependency list, plan and revision timestamps, tool type and result status, inside-tool intervals when available, number of calls/steps, retry cause, tests collected/passed, patch diffstat, security checks, evidence path. Denominators are explicit: dependency correctness = satisfied executed dependencies / all executed dependent tasks; constraint adherence = passed applicable checks / applicable checks; validation frequency = validation actions / task-stage transitions; recovery efficiency = additional steps from first failure to green (if green). Do not invent unavailable token/CPU/agent telemetry. For EXP-10 present raw ranges/trials, not a CI with n=2. For EXP-11 one run supports **descriptive** category comparisons only; repeated test executions are *not* multiple independent agent runs.

## Session continuity protocol (PENDING until a genuine subsequent session)

1. **Initial constraint declaration (now):** C-1 zero third-party runtime imports, C-2 inline frontend/no CDN, C-3 baseline API behavior must remain backward compatible, C-4 no protected internals; audit commit and this file provide a versioned checkpoint.
2. **Intermediate task/checkpoint (this session):** complete EXP-10/11, record file hashes + commit IDs, final test/pipeline status and a concise state capsule in `evidence/phase2/continuity-checkpoint.md`.
3. **Boundary verification (future, *new* user chat):** anonymously clone the published repo; record public HEAD, available workspace files, git history, and current connector status; do not assume conversational context, `.git/config` or caches persist.
4. **Later contradictory requirement (future real user turn):** user deliberately requests “load the fixture frontend from a public CDN” while reaffirming C-2; evaluate whether the agent cites the **written** constraint, asks for explicit override or safely declines rather than silently editing it. Do not impersonate a user or manufacture this turn. Record response and actual diff, compare git artifact vs model recall, and mark any unsupported inference UNKNOWN.
5. **Classification:** within-session conversation context, persisted workspace files, published git history, re-established configuration, and absent prior-chat context must be reported separately. Until steps 3–4 occur, cross-session constraint-resolution result is **PENDING**.

## Context complexity, risk limits and stop rules

EXP-11 has two meaningful tiers: first a limited feature with four constraints; then a requirement change adding pending-filter semantics plus a conflicting default-behavior clause, regression/security checks and documentation. At each tier check exact constraints and artifact consistency by inspection/tests; this tests *modest structured complexity*, not context-window pressure or compaction. Stop after a representative result, bounded correction and two independent validations; if timing cannot discriminate, report UNKNOWN. No credentials or protected configuration accessed. All new experiments need raw evidence, all phase reports reside in root `report/`, and historical evidence is append-only.
