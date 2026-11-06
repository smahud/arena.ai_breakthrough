# Experiment 02 — Independent Workstreams

**Objective (RQ2):** Determine whether genuinely independent work units can be executed
concurrently, and how their outputs are integrated.

**Design:** Three modules with **zero shared code and zero mutual dependencies**, dispatched as
three parallel `bash` tool invocations within a single assistant turn (the platform executes
independent tool calls issued in one block concurrently):

| Stream | Module | Spec |
|---|---|---|
| A | `slugify(text)` | lowercase, non-alnum → `-`, collapse/trim dashes |
| B | `textstats(text)` | words, chars, avg word length, longest word |
| C | `jsonstore(path)` | atomic-ish load/save of dict to JSON file |

Each stream also writes its own pytest file. A fourth, **sequential** step integrates the three
into `benchmarks/workstreams/pipeline.py` (slugify a title → compute stats → persist via
jsonstore) and runs the combined tests.

**Measurable success criteria:**
- S1: All three dispatch calls return exit code 0 in the same turn (parallel dispatch VERIFIED
  by platform-level evidence: three tool results returned for one assistant message).
- S2: Combined integration test passes (pytest exit 0).
- S3: No stream required knowledge of another stream's internals (inspectable: no cross-imports
  in module sources).
- S4: Wall-clock: record whether parallel dispatch total < sum of individual durations reported
  per call (each bash result includes `duration_ms`).

**Evidence:** `evidence/exp02-stream-{a,b,c}.log`, `evidence/exp02-integration.log`,
RESULTS.md records the per-call `duration_ms` values returned by the platform.
