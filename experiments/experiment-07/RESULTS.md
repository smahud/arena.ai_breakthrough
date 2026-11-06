# Experiment 07 — RESULTS

Executed: 2026-11-06T13:54Z (retrieval) → 14:01:33Z (validation).
Evidence: `exp07-semver-spec.md` (fetched normative text), `exp07-tests.log`.
Artifact: `src/semverlite/` + `tests/test_semverlite.py`.

## Research-to-implementation chain (each step VERIFIED)

1. **Source evaluation:** `web_search` returned semver.org as the authoritative spec (plus an
   rc.1 page and a Spanish translation, both rejected as non-normative/derived sources).
   `fetch_page(https://semver.org)` chunk 0/3 contained the full numbered rules 01–11 and the
   BNF grammar; chunk 0 was sufficient (rules + example + grammar all present) — later chunks
   not fetched (avoiding unnecessary retrieval, per directive §3).
2. **Extraction → design:** the implementation's regex was transcribed from the fetched BNF;
   the comparator encodes spec rule 11 sub-rules 1–4 literally, each cited in code comments.
   Precedence key: `(major, minor, patch, has_no_prerelease, typed_identifier_list)` with
   `(0,int,"")` for numeric and `(1,0,str)` for alphanumeric identifiers, giving numeric <
   alphanumeric and ASCII lexical order as two emergent properties of tuple comparison.
3. **Validation against the source's own examples:** the spec's worked chain
   `1.0.0-alpha < … < 1.0.0-rc.1 < 1.0.0` tested in both directions (pairwise `<` and
   shuffle→sort round-trip, fixed seed): `spec chain reproduced: True`.
4. **Negative space from normative text:** 8 invalid forms rejected, each traceable to a rule
   number (`01.2.3`→r02, `1.0.0-`→r09, `1.0.0-alpha.01`→r09, `1.0.0+`→r10, …).

## Criteria

S1 MET (quotes in evidence file match fetched content). S2 MET (`15 passed`, exit 0).
S3 MET (all 8 invalid cases raise `InvalidVersion`). S4 MET (stdlib `re` only; included in
the clean C-1 audit).

## Finding

Normative-document → code conversion was fully traceable: every comparator branch cites the
rule that mandates it, and every test cites either the spec's example or a rule number. The
retrieval-tool split (search=discover, fetch=extract) was load-bearing: implementation from
the search snippet alone would have lacked the BNF and the leading-zero prohibition.
