# Final Research Summary

Session: 2026-11-06T13:52–14:16Z · single continuous autonomous execution · sandbox env per
F-09 · full catalog: `docs/findings.md`.

## 1. Verified capabilities (VERIFIED, reproduced from preserved logs)

Zero-dependency full-stack delivery with live smoke testing (Exp-01); concurrent dispatch of
independent work units with failure isolation (F-01, F-15); regular one-step recovery loops
for compile/logic/environment faults, injected and organic alike (F-02, F-14); surgical
architecture adaptation against a committed baseline, SIGKILL-durable (F-05); session-long
constraint enforcement with contract-first contradiction resolution (F-06); normative
research → validated implementation with full source traceability (Exp-07, 15/15 against the
spec's own examples); managed process lifecycle with structured telemetry (F-04).

## 2. Observable orchestration patterns

Authoring parallelizes / validation serializes · batches never contain a call and its own
dependency · checkpoints precede risky change (diffstat as measurement instrument) ·
conflicts resolve toward the earlier *written* artifact and resolutions are logged ·
everything needed later is externalized to files at observation time (contract = normative
memory, evidence logs = episodic memory).

## 3. Evidence supporting architectural conclusions

The functional architecture (plan → dep-aware dispatch → reflect-on-telemetry → validate with
false-green guard → recover via classify/patch/re-verify → checkpoint → report) is supported
by converging evidence across all 7 experiments; the reference implementation `minagent`
instantiates it and passes 13 targeted tests, each mapped to its justifying finding.

## 4. Unresolved internal mechanisms (UNKNOWN — explicitly not claimed)

Whether batched calls execute on parallel workers (H-1); whether planning is a distinct
internal phase or an emergent property of one generative loop (H-2 — A1/A2/A3 all fit);
cross-turn/cross-day continuity (H-3); behavior under context-window pressure (H-4); model
composition, routing, prompt architecture (L-1/L-3 — out of scope by contract).

## 5. Reproducible experiments

All 7: each DESIGN.md pre-registers criteria; each procedure uses only documented sandbox
capabilities; each RESULTS.md quotes preserved raw logs. Re-running requires Python ≥3.10 +
pytest only (C-1). Timing-sensitive criteria (Exp-02 S4, minagent concurrency bound) carry
generous margins for weaker hardware.

## 6. Reference implementation results

`src/minagent` — 7 stdlib-only modules; 13/13 tests including a wall-clock concurrency check,
a literal "NO TESTS RAN" false-green rejection, exp03-shaped failure classification, and
Exp-06-shaped state durability. Its first validation run failed organically and was recovered
in one step by the very loop shape it encodes — the strongest single demonstration of the
study's central regularity.

## 7. Recommended next research steps

1. Batch-size vs latency curves (N=1…8) to resolve H-1.
2. Multi-session continuity protocol: constraints declared in session 1, contradicted in
   session 3 (resolves H-3/L-4).
3. Context-pressure experiment: force long transcripts, detect compaction/summarization
   artifacts (H-4).
4. Non-idempotent failure classes: appends, external side effects, network partitions —
   tests whether rollback (absent here by design, L-5) becomes necessary.
5. Adversarial validation: flaky tests and intermittent faults — does bounded-retry hold?
6. Scale the reference implementation (remote tools, queues) only if a measured requirement
   appears — keep contract rule 3 binding.

## Delivery

Complete local repository, clean tree, green validation; GitHub publishing unavailable on
this instance (F-10, re-verified 14:51Z) — runbook in `phase-8-delivery.md`. No claim of
publication is made.

---

## ADDENDUM — follow-up session (14:51–14:55Z, `report/phase-9-followup.md`)

Two §7 recommendations executed immediately after delivery:

1. **H-1 RESOLVED (Exp-08 → F-16):** batched bash calls execute **sequentially with ~0.13 s
   pipelined handoffs** (interval-timestamp method; T4 span 4.06 s, T8 span 7.08 s, scaling
   1.74). This **corrects** item 2 of this summary's earlier framing and F-01's
   "overlap INFERRED-likely": batching saves round-trips, not execution wall-time. Corrections
   propagated to findings.md, EXP-02 RESULTS (addendum), architecture-analysis §6, README.
2. **Transient-fault gap closed (Exp-09 → F-17):** patch-only retry (F-02) left flaky commands
   unrecoverable (FAILED@1, logged); minimal bounded extension `blind_retries` (default 0,
   traced) recovers them (DONE@2). Suite now **44/44**; all pre-existing tests unmodified.
3. Remaining open: H-2 (planner representation), H-3 (cross-turn continuity), H-4 (context
   pressure), plus Exp-08 residual (non-bash batch timing).
