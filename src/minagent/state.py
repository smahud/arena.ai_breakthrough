"""State + trace persistence (JUSTIFICATIONS rows 10-11: Exp-06 durability pattern, §7 evidence)."""
import json
import os
import tempfile
import threading
import time


def _atomic_write_json(path, data):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


class StateStore:
    """Run state, restart-survivable (same durability property proven in Exp-06 S3)."""

    def __init__(self, path=None):
        self.path = path
        self.data = {"tasks": {}, "meta": {}}

    def update(self, tasks):
        self.data["tasks"] = {
            t.id: {"status": t.status, "attempts": t.attempts, "deps": list(t.deps)}
            for t in tasks
        }
        self.data["meta"]["updated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def save(self):
        if self.path:
            _atomic_write_json(self.path, self.data)

    @classmethod
    def load(cls, path):
        s = cls(path)
        with open(path, "r", encoding="utf-8") as f:
            s.data = json.load(f)
        return s


class TraceReporter:
    """Append-only JSONL execution trace: timestamp, task, tool, command, exit_code,
    duration_ms, attempt, verdict (directive §7 as code). Thread-safe."""

    def __init__(self, path):
        self.path = path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    def event(self, type, **kw):
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "epoch": round(time.time(), 3), "type": type}
        rec.update(kw)
        line = json.dumps(rec, sort_keys=True, default=str)
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def read(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
