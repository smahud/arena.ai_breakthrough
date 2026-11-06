"""Validator with false-green guard (JUSTIFICATIONS row 8; findings F-03, F-08).

Exit code 0 is necessary but NOT sufficient: validation requires positive markers
(`expect`) and rejects known false-green markers (`forbid` — e.g. the literal
"NO TESTS RAN" observed in Exp-05 P2 with exit code 0).
"""
from .tools import shell_tool


class Validator:
    def __init__(self, registry=None):
        self._registry = registry

    def check(self, spec):
        run = self._registry.get(spec.get("tool", "shell")) if self._registry else shell_tool
        res = run({"command": spec["command"]})
        problems = []
        if not res.ok:
            problems.append(f"command failed (exit {res.exit_code})")
        for marker in spec.get("expect", []):
            if marker not in res.output:
                problems.append(f"missing expected marker {marker!r}")
        for marker in spec.get("forbid", []):
            if marker in res.output:
                problems.append(f"false-green marker present: {marker!r}")
        return (len(problems) == 0), ("; ".join(problems) if problems else "validated")
