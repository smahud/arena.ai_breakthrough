"""EXP-07 validation: tests derived from the fetched spec text, including the spec's own
worked precedence example (quoted in evidence/exp07-semver-spec.md)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from semverlite import InvalidVersion, Version, sort_versions  # noqa: E402

OFFICIAL_CHAIN = [
    "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta",
    "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0",
]


def test_official_precedence_chain():
    vs = [Version(v) for v in OFFICIAL_CHAIN]
    for a, b in zip(vs, vs[1:]):
        assert a < b, f"{a.raw} should be < {b.raw}"
    assert vs == sorted(vs)


def test_chain_shuffled_sorts_back():
    shuffled = ["1.0.0-beta.11", "1.0.0", "1.0.0-alpha.beta", "1.0.0-rc.1",
                "1.0.0-beta", "1.0.0-alpha.1", "1.0.0-beta.2", "1.0.0-alpha"]
    assert sort_versions(shuffled) == OFFICIAL_CHAIN


def test_numeric_core_ordering():
    assert sort_versions(["2.1.1", "1.0.0", "2.0.0", "2.1.0"]) == ["1.0.0", "2.0.0", "2.1.0", "2.1.1"]


def test_parse_fields():
    v = Version("1.2.3-rc.1+build.99")
    assert (v.major, v.minor, v.patch, v.prerelease, v.build) == (1, 2, 3, "rc.1", "build.99")


def test_build_metadata_ignored_in_precedence():
    assert Version("1.0.0+20130313144700") == Version("1.0.0+21AF26D3----117B344092BD")
    assert Version("1.0.0-beta+exp.sha.5114f85") == Version("1.0.0-beta")


@pytest.mark.parametrize("bad", [
    "1.0",            # incomplete core (rule 02)
    "01.2.3",         # leading zero in core (rule 02)
    "1.0.0-",         # empty pre-release (rule 09)
    "v1.0.0",         # prefix not allowed
    "1.0.0-alpha..1", # empty identifier (rule 09)
    "1.0.0-alpha.01", # leading zero in numeric pre-release id (rule 09)
    "1.0.0+",         # empty build (rule 10)
    "",
])
def test_invalid_versions_rejected(bad):
    with pytest.raises(InvalidVersion):
        Version(bad)


def test_numeric_lower_than_alphanumeric_ids():
    # spec 11.4.3: numeric identifiers always have lower precedence
    assert Version("1.0.0-1") < Version("1.0.0-alpha")


def test_larger_fieldset_wins_on_equal_prefix():
    # spec 11.4.4
    assert Version("1.0.0-alpha") < Version("1.0.0-alpha.1")
