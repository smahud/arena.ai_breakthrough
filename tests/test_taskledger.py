"""EXP-01 API-level tests. These target dispatch(), NOT the storage implementation —
by design they must survive EXP-06's storage swap unmodified (Exp-06 S1)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from taskledger.api import TaskAPI            # noqa: E402
from taskledger.storage import InMemoryStorage  # noqa: E402


def make_api():
    return TaskAPI(InMemoryStorage())


def test_health():
    s, p = make_api().dispatch("GET", "/api/health")
    assert s == 200 and p["status"] == "ok"


def test_empty_list():
    s, p = make_api().dispatch("GET", "/api/tasks")
    assert s == 200 and p["tasks"] == []


def test_create_and_list():
    api = make_api()
    s, t = api.dispatch("POST", "/api/tasks", {"title": "write report"})
    assert s == 201 and t["title"] == "write report" and t["done"] is False
    s, p = api.dispatch("GET", "/api/tasks")
    assert [x["id"] for x in p["tasks"]] == [t["id"]]


def test_create_rejects_empty_title():
    s, p = make_api().dispatch("POST", "/api/tasks", {"title": "   "})
    assert s == 400 and "error" in p


def test_get_one_and_404():
    api = make_api()
    _, t = api.dispatch("POST", "/api/tasks", {"title": "a"})
    s, got = api.dispatch("GET", f"/api/tasks/{t['id']}")
    assert s == 200 and got["title"] == "a"
    assert api.dispatch("GET", "/api/tasks/nope")[0] == 404


def test_patch_done():
    api = make_api()
    _, t = api.dispatch("POST", "/api/tasks", {"title": "a"})
    s, upd = api.dispatch("PATCH", f"/api/tasks/{t['id']}", {"done": True})
    assert s == 200 and upd["done"] is True


def test_patch_missing_404():
    assert make_api().dispatch("PATCH", "/api/tasks/nope", {"done": True})[0] == 404


def test_delete_then_gone():
    api = make_api()
    _, t = api.dispatch("POST", "/api/tasks", {"title": "a"})
    assert api.dispatch("DELETE", f"/api/tasks/{t['id']}")[0] == 204
    assert api.dispatch("GET", f"/api/tasks/{t['id']}")[0] == 404
    assert api.dispatch("DELETE", f"/api/tasks/{t['id']}")[0] == 404


def test_unknown_route():
    assert make_api().dispatch("GET", "/api/whatever")[0] == 404


def test_titles_trimmed():
    _, t = make_api().dispatch("POST", "/api/tasks", {"title": "  padded  "})
    assert t["title"] == "padded"
