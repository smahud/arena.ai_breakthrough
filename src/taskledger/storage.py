"""Storage layer.

v1: InMemoryStorage (EXP-01). v2 (EXP-06 / CR-1): SQLiteStorage added behind the SAME
5-method interface (create/list/get/update/delete) so the API layer needs zero changes.
Stdlib only (C-1). Note: one connection with check_same_thread=False + commit-per-write;
sqlite3 serializes access at connection level — adequate for this workload, documented
rather than over-engineered with a pooling layer nobody asked for.
"""
import os
import sqlite3
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


class SQLiteStorage:
    """CR-1: persistence across process restarts. Same interface as InMemoryStorage."""

    _COLS = "id,title,done,created_at"

    def __init__(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id TEXT PRIMARY KEY, title TEXT NOT NULL, "
            "done INTEGER NOT NULL DEFAULT 0, created_at REAL NOT NULL)"
        )
        self._conn.commit()

    @staticmethod
    def _row(r):
        return {"id": r[0], "title": r[1], "done": bool(r[2]), "created_at": r[3]} if r else None

    def create(self, title):
        t = {"id": uuid.uuid4().hex[:12], "title": title, "done": False, "created_at": time.time()}
        self._conn.execute("INSERT INTO tasks VALUES (?,?,?,?)",
                           (t["id"], t["title"], int(t["done"]), t["created_at"]))
        self._conn.commit()
        return dict(t)

    def list(self):
        rows = self._conn.execute(
            f"SELECT {self._COLS} FROM tasks ORDER BY created_at").fetchall()
        return [self._row(r) for r in rows]

    def get(self, tid):
        r = self._conn.execute(f"SELECT {self._COLS} FROM tasks WHERE id=?", (tid,)).fetchone()
        return self._row(r)

    def update(self, tid, fields):
        cur = self.get(tid)
        if cur is None:
            return None
        title = str(fields["title"]).strip() if str(fields.get("title", "")).strip() else cur["title"]
        done = bool(fields["done"]) if "done" in fields else cur["done"]
        self._conn.execute("UPDATE tasks SET title=?, done=? WHERE id=?", (title, int(done), tid))
        self._conn.commit()
        return {"id": tid, "title": title, "done": done, "created_at": cur["created_at"]}

    def delete(self, tid):
        c = self._conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
        self._conn.commit()
        return c.rowcount > 0
