# Reference Architecture (functional, evidence-backed)

Instantiates the architecture-neutral functional components of `docs/architecture-analysis.md`
§2. Chosen shape: explicit planner + parallel-capable executor (A2) for *inspectability* — not
because A2 was evidenced over A1/A3 (§5 there). Every component is justified by a finding in
`JUSTIFICATIONS.md`; nothing speculative was built (contract rule 3).

```
                ┌──────────────────────────────────────────────┐
                │                  AgentLoop                   │
                │  plan → select-ready → dispatch → reflect    │
                │     ▲            │                 │         │
                │     │            ▼                 ▼         │
                │  replan-once   ToolRegistry     Validator     │
                │                (adapters)     (false-green    │
                │                    │           guard)         │
                │                    ▼                 │       │
                │              RecoveryPolicy ◄────────┘       │
                │              (classify, retry, patch)        │
                │                    │                         │
                │                    ▼                         │
                │   StateStore (JSON, atomic)  TraceReporter    │
                │                              (append JSONL)  │
                └──────────────────────────────────────────────┘
                          Provider interface (pluggable
                          decompose_fn; deterministic default)
```

## Components & invariants

1. **Planner** — decomposes a goal into `Task(id, kind, deps, payload)`; dependency-aware
   ready-set selection. Provider-pluggable (`decompose_fn`) so an LLM or heuristic can supply
   decomposition; default is deterministic (testability, C-1).
2. **Executor** — runs ready tasks; independent tasks dispatched concurrently
   (`ThreadPoolExecutor`, max 4 — 2 vCPU measured, F-09); dependent tasks strictly after deps.
3. **ToolRegistry / adapters** — uniform `run(payload) -> ToolResult(ok, output, exit_code,
   duration_ms, command)`; adapters: `shell` (subprocess w/ timeout + `pipefail` semantics),
   `write_file` (atomic via tmp+replace), `python_inline`. Result shape mirrors the platform
   telemetry profile actually observed (F-13).
4. **RecoveryPolicy** — on failure: classify (exit 127 → environment; nonzero + test output →
   logic; syntax error text → compile-time), then bounded retries with the registered
   `repair_fn` per task; loop shape = F-02 (detect→localize→minimal-patch→re-verify).
5. **Validator** — runs validation commands and requires **positive evidence of work**:
   exit 0 AND a configurable success pattern AND (for test commands) a nonzero test count.
   Directly encodes F-03/F-08 (false-green guard).
6. **StateStore** — atomic JSON persistence of run state (tasks, statuses, attempts);
   survives process restart (pattern proven in Exp-06 durability test).
7. **TraceReporter** — append-only JSONL trace: timestamp, task, tool, command, exit_code,
   duration_ms, attempt, verdict — the evidence discipline of directive §7 as code.
8. **AgentLoop termination** — stops when all tasks done+validated, or retry budget exhausted
   (failed tasks reported, never concealed — contract rule 9), or a single global replan
   (adding missing deps/tasks) has already been consumed.

## Deliberate absences (with reasons)

- No message bus/queue (single process; ThreadPoolExecutor suffices — L-8 acknowledges scale).
- No LLM client implementation (provider interface + deterministic default only; wiring a
  specific vendor SDK would violate C-1 and add speculation).
- No rollback engine (Exp-03 showed idempotent re-run sufficed; non-idempotent classes are
  UNKNOWN L-5 — building speculative rollback would violate contract rule 3).
- No multi-agent delegation layer (none observed; F-01 delegation is tool-level only).
