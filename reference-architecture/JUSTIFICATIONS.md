# Component Justification Ledger (contract rule 3 audit)

Every component of `src/minagent/` must trace to a requirement or finding. This table is the
audit; a component without a row here must be deleted.

| Component / decision | Justified by | Requirement or finding |
|---|---|---|
| Planner with dep-aware ready-set | directive §5 "task planning"; Exp-01 build-order observation | RQ1; F-05 |
| Pluggable `decompose_fn` provider | directive §5 "configurable model-provider interfaces" | requirement, not finding |
| ThreadPoolExecutor(4) for independent tasks | Exp-02 batch dispatch; 2 vCPU measured | F-01, F-09 |
| Uniform ToolResult (exit_code, duration_ms, output) | the only telemetry shape actually observable | F-13 |
| shell adapter uses pipes carefully / captures stderr | pipefail & masking incidents | F-03 |
| write adapter tmp+os.replace atomic | jsonstore stream C design validated in Exp-02 | Exp-02 S2 |
| RecoveryPolicy classify-by-exit-code (127 vs 1 vs syntax) | Exp-03 fault classes F1/F2/F3a | F-02 |
| Bounded repair attempts (max 2) + report failures | contract rule 9 (no concealment); Exp-03 one-call recoveries | F-02, rule 9 |
| Validator false-green guard (count>0 / pattern) | `NO TESTS RAN` + tee-masked exit codes | F-03, F-08 |
| StateStore atomic JSON, restart-survivable | Exp-06 SIGKILL durability pattern | F-05/Exp-06 S3 |
| TraceReporter append-only JSONL | directive §7 evidence & traceability | requirement |
| Single global replan budget | observed replanning was evidence-driven and rare | F-05; avoids speculative complexity |
| `Task.blind_retries` (default 0) + `blind_retry` trace event | Exp-09 before/after logs: transient fault FAILED@1 under patch-only policy, DONE@2 with bounded blind retry | F-17 |
| Executor note: in-process threads unaffected by F-16 | minagent runs inside ONE platform call; concurrency test measures real overlap (3×0.25 s < 0.6 s wall) | F-16, F-01 |
| NO rollback engine / NO bus / NO vendor SDK | absence-of-evidence + contract rule 3 | L-5, L-8 |
