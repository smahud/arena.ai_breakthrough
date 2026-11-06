# Evidence: SemVer 2.0.0 specification (retrieved live)

Retrieval method: `fetch_page(https://semver.org)` chunk 0 of 3, plus `web_search` discovery
layer — both executed 2026-11-06 (UTC) during this session. Verbatim normative excerpts from
the fetched content (full text available at https://semver.org/spec/v2.0.0.html):

> 02. A normal version number MUST take the form X.Y.Z where X, Y, and Z are
>     non-negative integers, and MUST NOT contain leading zeroes.

> 09. A pre-release version MAY be denoted by appending a hyphen and a series of dot separated
>     identifiers immediately following the patch version. Identifiers MUST comprise only ASCII
>     alphanumerics and hyphens [0-9A-Za-z-]. Identifiers MUST NOT be empty. Numeric identifiers
>     MUST NOT include leading zeroes. Pre-release versions have a lower precedence than the
>     associated normal version. Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7,
>     1.0.0-x.7.z.92, 1.0.0-x-y-z.--.

> 10. Build metadata MAY be denoted by appending a plus sign and a series of dot separated
>     identifiers ... Build metadata MUST be ignored when determining version precedence.

> 11. Precedence ... 4.1 Identifiers consisting of only digits are compared numerically.
>     4.2 Identifiers with letters or hyphens are compared lexically in ASCII sort order.
>     4.3 Numeric identifiers always have lower precedence than non-numeric identifiers.
>     4.4 A larger set of pre-release fields has a higher precedence than a smaller set, if all
>     of the preceding identifiers are equal.

Official worked example (basis of test validation):

> Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 <
> 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0.

BNF grammar for valid versions was also present in the fetched chunk (see semver.org).

**EXP-05 P3 note:** `web_search` returned a condensed paraphrase of the precedence rules
(sufficient for orientation); `fetch_page` returned the full numbered normative text and BNF
(sufficient for implementation). Recorded selection: search → discover, fetch → extract.
