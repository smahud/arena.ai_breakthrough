# Research Objectives

## Primary Question

How do modern agentic AI systems accomplish complex engineering tasks — and what functional
architecture is sufficient to reproduce the *observable* behavior?

## Sub-Questions

- **RQ1 (Planning):** How are goals decomposed into units of work, sequenced, and verified?
- **RQ2 (Coordination):** Which work units execute independently/in parallel, and how are
  intermediate artifacts exchanged and aggregated?
- **RQ3 (Tool orchestration):** How are tools selected, invoked, and recovered from failure?
- **RQ4 (Adaptivity):** How does behavior change under complexity growth, tool failure,
  contradictory information, and mid-flight requirement change?
- **RQ5 (Architecture):** What minimal functional architecture is consistent with all
  observations — and what alternative architectures explain the same data?

## Method

Practical engineering tasks executed inside an authorized sandbox are the primary instrument
(directive §1). The researcher is *also* the subject: this project is executed by the agentic
system under study, so observations of planning/decomposition/recovery are first-person
execution records, cross-checked against artifacts (logs, exit codes, file trees, test output).

**Epistemic limitation, stated up front (see `docs/limitations.md` L-1):** a system observing
itself cannot verify its own internal mechanisms. All statements about internals are INFERRED
or UNKNOWN; only behavior and artifacts are VERIFIED.

## Success Criteria for the Project Itself

1. ≥7 experiments, each with design, raw evidence, and classified findings.
2. A functional reference architecture distinguishing observable / documented / inferred layers.
3. An independent, dependency-free reference implementation with a green test suite.
4. A phase report for each of the 8 execution phases.
5. Zero unsubstantiated claims in final conclusions (audit in `report/phase-7-verification.md`).
