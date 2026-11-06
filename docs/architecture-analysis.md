# Functional Architecture Analysis

Goal (directive §4): a *functional* reference architecture consistent with observations, with
the epistemic layer of each element marked. This document makes **no claim** about hidden
prompts, routing configuration, model identities, or runtime internals — those are UNKNOWN
(F-13) and out of scope by contract rule 11.

## 1. Observable layer (VERIFIED through supported interfaces)

```
user goal
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│ TURN LOOP (directly observable via tool-call/result traffic)│
│                                                             │
│  plan(next actions) ──► dispatch batch ──► tool results     │
│        ▲                   │  (bash / write_file /          │
│        │                   │   start_process / fetch / …)   │
│        │                   ▼                                │
│  reflect on results ◄── structured telemetry:               │
│        │               stdout, stderr, exit_code,           │
│        ▼               duration_ms, ports, status           │
│  validate? recover? continue? ──► artifacts (files, git,    │
│                                    evidence logs)           │
└─────────────────────────────────────────────────────────────┘
```

Observable facts: batched independent dispatch (F-01), structured per-call telemetry (F-13),
workspace persistence across calls, managed background processes (F-04), connectors gated by
`list_connector_tools` with explicit status semantics (F-10).

## 2. Functional components (behaviorally evidenced)

| Component | Evidence | Class |
|---|---|---|
| Goal interpretation & scoping | experiment DESIGns written before code; scope limits stated (Exp-04, Exp-07 chunk restraint) | VERIFIED behavior |
| Decomposition & sequencing | Exp-01 build order storage→api→server→frontend→tests→pipeline; designs precede execution | VERIFIED behavior |
| Batched invocation with per-unit results | F-01, F-15 | VERIFIED for observed batches; runtime overlap separately measured by F-16 |
| Validation layer | run_suite.py, pytest, audits; false-green guards needed (F-03, F-08) | VERIFIED |
| Recovery controller | F-02, F-14 loop shape | VERIFIED |
| Externalized state | CONTRACT.md (constraints), evidence/ (raw memory), git (checkpoints) | VERIFIED |
| Conflict arbitration | T2 resolution toward earlier contract (F-06) | VERIFIED |
| Reporting | phase reports, RESULTS.md per experiment | VERIFIED |

## 3. Documented layer (public platform documentation)

The platform documents (via tool descriptions visible to any user of this environment):
sandbox persistence rules, preview-host requirements (bind 0.0.0.0), bash-not-for-servers
guidance — empirically confirmed by F-04 — connector loading protocol, snapshot exclusions.
These are **DOCUMENTED**, and where tested here also VERIFIED.

## 4. Inferred layer (INFERRED — indirect evidence only)

- A control process that groups independent tool calls per assistant message and returns
  aggregated results (from F-01/F-15). Whether grouping implies parallel workers is UNKNOWN.
- Goal-conditioned re-planning between turns/steps rather than a fixed upfront plan: Exp-06's
  checkpoint-then-adapt and the mid-batch pivot to `pipefail` show plan mutation in response to
  evidence, but the mutation's internal representation is unobservable.

## 5. Alternative architectures consistent with ALL observations (directive §4.4)

- **A1 Single generative loop (ReAct-style):** one policy emits interleaved reasoning +
  tool calls; "planning" is just the next-token continuation conditioned on the transcript.
- **A2 Explicit planner/executor split:** a planner component produces a task structure that a
  scheduler dispatches, with a separate reflector.
- **A3 Multi-specialist composition:** several narrowly-scoped workers (coder, tester,
  documenter) coordinated by an orchestrator.

All three can produce batched invocation with mostly serial bash timing, separate validation
steps, short recovery loops, written constraint handling, and F-13's tool-result telemetry.
None alone specifies an internal worker count. **Nothing in this study's evidence
discriminates between A1–A3.** Per directive §2E, no distinct models or agents are inferred
from style/speed differences; the number and arrangement of internal generators is UNKNOWN.
The reference implementation (Phase 6) therefore instantiates the *functional* components of
§2 — which are architecture-neutral — with an explicit planner (A2 shape) chosen for
inspectability, not because A2 was evidenced over A1.

## 6. What would discriminate (future authorized experiments)

- ~~Latency-vs-batch-size curves (N=1..8) for all-at-once bash execution (H-1)~~ —
  **DONE for Exp-08 conditions**: mostly serial *with measured adjacent overlap* (F-16).
  Remaining: non-bash completion ordering and mechanism under different workloads. Timing
  alone cannot identify worker count or protected implementation boundaries.
- Cross-message constraint tests over days (H-3, L-4).
- Context-pressure tests: force long transcripts, watch for compaction artifacts (H-4).
- Deliberate mid-batch contradiction to test arbitration ordering at scale.
