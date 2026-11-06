"""Core data types. ToolResult mirrors the telemetry profile actually observable on the
studied platform (stdout/stderr merged output, exit_code, duration_ms — finding F-13)."""
from dataclasses import dataclass, field

PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"


@dataclass
class ToolResult:
    ok: bool
    output: str
    exit_code: int | None
    duration_ms: int = 0
    command: str = ""


@dataclass
class Task:
    id: str
    tool: str = "shell"
    payload: dict = field(default_factory=dict)
    deps: tuple = ()
    validate: dict | None = None      # {"command":…, "expect":[…], "forbid":[…]}
    repair: object = None             # fn(task, attempt, result) -> bool (F-02 minimal patch)
    max_attempts: int = 2             # bounded retries (Exp-03: 1 retry sufficed; +1 margin)
    blind_retries: int = 0            # EXP-09: identical re-runs allowed WITHOUT a patch, for
                                      # transient/flaky faults. Default 0 preserves F-02 semantics
                                      # (deterministic failures are never blindly re-run).
                                      # Still capped by max_attempts.
    status: str = PENDING
    attempts: int = 0
    result: ToolResult | None = None
