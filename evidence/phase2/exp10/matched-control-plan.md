# EXP-10 exploratory matched control X1 (registered before run)

**Registered:** 2026-11-06 after completion of primary N=3 results and the D1 singleton; independent of original pre-registration, not a Phase-1 repeat claimed as new.

**Question:** Could the contrast between historical Exp-08 T4 and Phase-2 EXP-10 be explained *solely* by N and sleep duration? T4 used N=4, nominal d=1.0 s and observed a 4.064 s span with adjacent-only overlap. The primary Phase-2 trials used N=3, d=.25/.75 s and all-pair overlap.

**Predictions / alternatives:** If N/d alone force serial-like timing in this invocation envelope, matched N=4/d=1.0 should yield a span near 4 s and mainly adjacent overlap. If all-pair overlap persists, N/d alone are insufficient; wrapper mode, historical session environment, platform policy changes, clock differences, jitter, or other unobserved factors remain viable. A single exploratory batch is descriptive, not a causal proof or confidence interval.

**Variables/controls:** One explicit `multi_tool_use.parallel` batch of *four independent* bash calls using the same Python `interval.py` with unique `X1-0`…`X1-3` JSON files, d=1.0 s, same workspace/clock method and result transcription as the primary trials. No shared writes or dependencies. The only intended changes from primary are N and d; comparison with historical T4 remains confounded by batch interface and session.

**Prespecified measurements / criteria:** record four returned statuses/durations and raw inside-tool `start_ns/end_ns`; calculate span, all 6 pairwise intersections, ordered start gaps, and same method as `analyze.py`; compare T4's 4.064 s and adjacent-only overlap. Success = four valid records and honest limitations; no criterion depends on a preferred timing pattern. Do not overwrite prior 12 records. Preserve analysis and interpretation in EXP-10 RESULTS, with a distinct exploratory label.
