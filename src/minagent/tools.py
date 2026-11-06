"""Tool adapters (justification: JUSTIFICATIONS.md rows 3-6)."""
import os
import subprocess
import sys
import tempfile
import time

from .types import ToolResult


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, fn):
        self._tools[name] = fn

    def get(self, name):
        return self._tools[name]

    def names(self):
        return sorted(self._tools)


def _timed(fn):
    def wrapper(payload):
        t0 = time.monotonic()
        r = fn(payload)
        r.duration_ms = int((time.monotonic() - t0) * 1000)
        return r
    return wrapper


@_timed
def shell_tool(payload):
    """bash with pipefail ON — F-03: unguarded pipelines masked a real test failure."""
    cmd = payload["command"]
    timeout = payload.get("timeout", 30)
    try:
        p = subprocess.run(["/bin/bash", "-o", "pipefail", "-c", cmd],
                           capture_output=True, text=True, timeout=timeout,
                           cwd=payload.get("cwd"))
        return ToolResult(p.returncode == 0, (p.stdout or "") + (p.stderr or ""),
                          p.returncode, 0, cmd)
    except subprocess.TimeoutExpired:
        return ToolResult(False, f"timeout after {timeout}s", None, 0, cmd)


@_timed
def write_file_tool(payload):
    """Atomic write via tmp + os.replace — pattern validated in Exp-02 stream C."""
    path, content = payload["path"], payload["content"]
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return ToolResult(True, f"wrote {len(content)} chars to {path}", 0, 0, f"write_file:{path}")


@_timed
def python_inline_tool(payload):
    p = subprocess.run([sys.executable, "-c", payload["code"]],
                       capture_output=True, text=True, timeout=payload.get("timeout", 30))
    return ToolResult(p.returncode == 0, (p.stdout or "") + (p.stderr or ""),
                      p.returncode, 0, "python:-c")


def default_registry():
    reg = ToolRegistry()
    reg.register("shell", shell_tool)
    reg.register("write_file", write_file_tool)
    reg.register("python_inline", python_inline_tool)
    return reg
