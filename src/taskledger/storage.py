"""Storage layer. v1: in-memory (EXP-06 will replace with SQLite behind the same interface)."""
import time
import uuid


class InMemoryStorage:
    def __init__(self):
        self._tasks = {}

    def create(self, title):
        t = {
            "id": uuid.uuid4().hex[:12],
            "title": title,
            "done": False,
            "created_at": time.time(),
        }
        self._tasks[t["id"]] = t
        return dict(t)

    def list(self):
        return [dict(t) for t in self._tasks.values()]

    def get(self, tid):
        t = self._tasks.get(tid)
        return dict(t) if t else None

    def update(self, tid, fields):
        t = self._tasks.get(tid)
        if not t:
            return None
        if "done" in fields:
            t["done"] = bool(fields["done"])
        if "title" in fields and str(fields["title"]).strip():
            t["title"] = str(fields["title"]).strip()
        return dict(t)

    def delete(self, tid):
        return self._tasks.pop(tid, None) is not None
