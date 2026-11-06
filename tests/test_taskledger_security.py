"""EXP-11: fixture-proven static-path containment regression for the real taskledger server."""
import http.client
import os
import sys
import threading

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from taskledger import server as task_server  # noqa: E402
from taskledger.storage import InMemoryStorage  # noqa: E402


def test_static_sibling_and_symlink_cannot_escape(tmp_path, monkeypatch):
    root = tmp_path / "static"
    root.mkdir()
    (root / "index.html").write_text("<html>safe</html>")
    sibling = tmp_path / "static_extra"
    sibling.mkdir()
    (sibling / "audit.txt").write_text("EXP11_FIXTURE_SENTINEL_NOT_SECRET\n")
    (root / "external-link").symlink_to(sibling / "audit.txt")
    monkeypatch.setattr(task_server, "STATIC", str(root))
    srv = task_server.serve("127.0.0.1", 0, InMemoryStorage())
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        for target, expected in (("/../static_extra/audit.txt", 404), ("/external-link", 404), ("/", 200)):
            conn = http.client.HTTPConnection("127.0.0.1", srv.server_port, timeout=2)
            conn.request("GET", target)
            resp = conn.getresponse()
            body = resp.read().decode()
            conn.close()
            assert resp.status == expected, (target, resp.status)
            assert "EXP11_FIXTURE_SENTINEL_NOT_SECRET" not in body
    finally:
        srv.shutdown()
        srv.server_close()
        thread.join(timeout=2)
