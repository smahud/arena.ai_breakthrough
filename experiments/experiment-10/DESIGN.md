# Experiment 10 — Tool scheduling beyond the Exp-08 bash batch

**Pre-registered:** 2026-11-06 after audit commit `c0caa6e`, before trial execution.
**Question (RQ2/RQ3):** Does Exp-08's mostly serial bash pattern depend on service duration, and what can be measured about mixed bash/`write_file` dispatch, per-unit failure, dependencies, and a bounded timeout?

## Hypotheses and alternative explanations

- H10-serial: for N=3 same-length bash calls, span grows toward 3d with no non-adjacent overlap; start gaps depend on duration d, possibly a short adjacent handoff as Exp-08 observed.
- H10-overlap: starts are near-contemporaneous, many pairwise intervals overlap and span is nearer d; actual overlap is measured, **not** inferred from per-call `duration_ms`.
- H10-variable: pattern differs across 0.25 s vs 0.75 s workloads or mixed tool types. An OS scheduler, sandbox reuse, transport overhead, provider-side queuing or even distinct workers could each produce a given pattern; **worker count and platform internals remain UNKNOWN**.
- Alternatives: jitter, CPU contention, file-system mtime rounding, clock skew if calls run on different hosts, or tool-specific serialization. Two replicates are descriptive, not a probability estimate.

## Variables and controls

| Variable | Setting |
|---|---|
| Independent | bash service duration `d∈{0.25,0.75}` seconds; two separate batches per `d`, N=3; mixed-batch tool category and one intentionally invalid path; one harmless timeout (`timeout=1`, process work ≤2 s) |
| Controlled | same host-visible workspace, `python3`, per-call unique JSON interval path, no shared file writes, fixed N, no remote services; all calls in a batch independent and safe to dispatch together |
| Measured | `time.time_ns()` around `time.sleep(d)` inside each bash, path-specific JSON + stdout; batch span, pairwise overlaps, start gaps, platform `duration_ms` when returned; `write_file` file mtime_ns **at completion only**; failure result status; healthy sibling presence/content; timeout tool status and eventual sentinel status |
| Unavailable | non-bash *start* time, model-generation latency, hidden queue, hardware worker count, model identity. No inferences from absence of mtime overlap alone. |

## Exact sequence and evidence

1. Create `evidence/phase2/exp10/` and a regular file `blocker` there (so attempting to write `blocker/child.txt` fails harmlessly). Record UTC, baseline commit and environment in `evidence/phase2/exp10/manifest.md`.
2. Run **four** independent N=3 bash batches through the user-facing parallel tool interface: `S1`/`S2` each 0.25 s, `L1`/`L2` each 0.75 s. Each call executes `python3 -c` to write `{trial}-{index}.json` with `start_ns,end_ns,duration_expected_s`, and print the JSON. Do not batch any call whose input depends on a sibling. Preserve returned `duration_ms`, exits, and the result envelope as faithfully as available in `exp10/dispatch-results.md`; never invent a timestamp for a file tool.
3. Analysis script reads only preserved raw JSON (no reenactment) and writes `evidence/phase2/exp10/analysis.log` with N, spans, all overlapping pairs, within-trial gaps, simple min/max over two replicates and `duration_ms - inside_duration` when telemetry exists. Check same-clock assumption; no CI with n=2.
4. One **mixed** batch of independent calls: `bash` timed sleep 0.6 s to its own interval file; healthy `write_file` marker; invalid `write_file` to `blocker/child.txt`; another independent healthy marker. Inspect returned statuses and afterward `stat` markers / bash interval for completion-time ordering. **Failure isolation** = both healthy markers present and correct despite bad call. File mtime is not file-tool start time. Preserve error result verbatim in dispatch record.
5. In a separate independent pair, use a benign bash task doing at most 2 s work with `timeout=1` and a healthy file write; record timeout status and later inspect any sentinel once naturally past the 2 s window. A timeout can stop *waiting* without killing work (tool description); do not claim kill/liveness unless observed. No unbounded server or repeated polling.
6. Read the healthy marker via `read_file` only **after** the mixed batch returned; a true data dependency must wait for a separate turn. Record both content and invocation order, but do not claim the platform enforces dependency semantics.

**Success criteria:** S1 ≥12 well-formed unique timed bash records, plus two per-duration replicate summaries; S2 mixed batch has separate result for each call, both healthy files correct, invalid path fails without corrupting siblings; S3 timeout result and post-timeout sentinel check recorded (including UNKNOWN if ambiguous); S4 exact raw paths, commands, result statuses and limitations in RESULTS, no worker/model identity claim. If `write_file` or a batch facility is unavailable, report the blocker rather than fabricating.

**Reproduction:** on a disposable workspace, use the same four batched call sequences specified above with distinct trial names, run the analysis on JSON interval records (script in the experiment's RESULTS), compare within the *same instance*. The mixed invalid path is inside the workspace and must not be changed to a protected or external path. Result metadata may vary across sessions.

## Prospective exploratory control, registered *after* S1/S2/L1/L2 but before control execution

The four fixed-N trials unexpectedly show all three bash intervals overlapping in an **explicit
`multi_tool_use.parallel` wrapper**, unlike Exp-08's old mostly serial intervals. To distinguish
**invocation path** from workload duration as an alternative explanation, attempt **one N=3,
d=0.75 s batch of direct `functions.bash` calls in the same assistant response without the
explicit wrapper**, saving unique `D1-{0,1,2}.json` intervals. If the tool protocol does not
allow this mode, record the blocker; do *not* substitute three sequential assistant turns.
Compare D1 start order/overlap to L1/L2 with the same script and duration. This is an
**exploratory, adaptively added control**; it is not retroactively part of the pre-registered
S1/S2/L1/L2 trial set, and n=1 permits no stability claim. A difference would not establish
whether the cause is wrapper scheduling, session environment, or other interface differences
from Exp-08. No change to primary success criteria. **Actual outcome:** only D1-0 was submitted, so no 3-call direct control was executed; no protocol restriction can be inferred.

## Second prospective exploratory matched-N/d control (X1; registered before running it)

See [`../../evidence/phase2/exp10/matched-control-plan.md`](../../evidence/phase2/exp10/matched-control-plan.md). This is **after** primary results, **not** a retroactive primary endpoint: run a single explicit-wrapper batch with N=4 and d=1.0 s (`X1-0`…`X1-3`) to match historical Exp-08 T4's N/d. Compare inside-tool intervals and spans with T4. No same-session historical invocation-mode control is available; alternate explanations remain even if matched timing differs.
