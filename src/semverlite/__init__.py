"""semverlite — SemVer 2.0.0 parser/comparator derived from the normative spec text
retrieved live from semver.org (evidence/exp07-semver-spec.md). Stdlib only (C-1).

Implements spec rules 02 (core form, no leading zeroes), 09 (pre-release), 10 (build
metadata ignored for precedence), 11 (precedence algorithm).
"""
import re

# Regex transcribed from the spec's BNF grammar (fetched chunk, semver.org).
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class InvalidVersion(ValueError):
    pass


class Version:
    __slots__ = ("raw", "major", "minor", "patch", "prerelease", "build")

    def __init__(self, raw):
        if not isinstance(raw, str):
            raise InvalidVersion(f"not a string: {raw!r}")
        m = SEMVER_RE.match(raw)
        if not m:
            raise InvalidVersion(f"invalid semver: {raw!r}")
        self.raw = raw
        self.major, self.minor, self.patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
        self.prerelease = m.group(4)  # None when absent
        self.build = m.group(5)       # ignored in precedence (spec rule 10)

    def _precedence_key(self):
        # Spec rule 11: numeric core first; a pre-release ranks BELOW its normal version;
        # per-identifier: numeric < alphanumeric, numeric compared as numbers,
        # alphanumeric in ASCII order; larger field-set wins when prefix equal.
        if self.prerelease is None:
            return (self.major, self.minor, self.patch, 1, [])
        ids = []
        for part in self.prerelease.split("."):
            ids.append((0, int(part), "") if part.isdigit() else (1, 0, part))
        return (self.major, self.minor, self.patch, 0, ids)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._precedence_key() == other._precedence_key()

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._precedence_key() < other._precedence_key()

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __hash__(self):
        return hash(self._precedence_key())

    def __repr__(self):
        return f"Version({self.raw!r})"


def parse(raw):
    return Version(raw)


def sort_versions(raws):
    return [v.raw for v in sorted(Version(r) for r in raws)]
