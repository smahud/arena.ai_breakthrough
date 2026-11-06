"""EXP-06 / CR-1: NEW persistence tests. The pre-existing API tests in
test_taskledger.py are deliberately UNMODIFIED — their passing proves the
storage abstraction held (Exp-06 S1)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from taskledger.api import TaskAPI                # noqa: E402
from taskledger.storage import SQLiteStorage      # noqa: E402


def test_sqlite_crud(tmp_path):
    s = SQLiteStorage(str(tmp_path / "db.sqlite3"))
    t = s.create("persist me")
    assert s.get(t["id"])["title"] == "persist me"
    assert s.update(t["id"], {"done": True})["done"] is True
    assert len(s.list()) == 1
    assert s.delete(t["id"]) is True
    assert s.list() == []


def test_durability_across_storage_instances(tmp_path):
    """Data survives closing and reopening the store (process-restart analogue)."""
    path = str(tmp_path / "db.sqlite3")
    s1 = SQLiteStorage(path)
    t = s1.create("survivor")
    s1._conn.close()
    s2 = SQLiteStorage(path)
    got = s2.get(t["id"])
    assert got is not None and got["title"] == "survivor"


def test_api_layer_unaware_of_swap(tmp_path):
    """Same API contract holds on SQLite storage (no api.py changes were needed)."""
    api = TaskAPI(SQLiteStorage(str(tmp_path / "db.sqlite3")))
    s, t = api.dispatch("POST", "/api/tasks", {"title": "x"})
    assert s == 201
    s, p = api.dispatch("GET", "/api/tasks")
    assert s == 200 and p["tasks"][0]["id"] == t["id"]
    assert api.dispatch("DELETE", f"/api/tasks/{t['id']}")[0] == 204
