#!/usr/bin/env python3
"""EXP-01 validation pipeline: import check -> unit tests -> live server smoke test.

Writes a machine-readable result JSON (S3) and exits nonzero on any failure.
Stdlib only (C-1). Usage: python3 benchmarks/run_suite.py
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(ROOT, "evidence", "run-suite-result.json")


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def http(method, url, body=None, timeout=5):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw and r.headers.get("Content-Type", "").startswith("application/json") else raw.decode(errors="replace"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def main():
    results = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "steps": []}

    def step(name, ok, detail):
        results["steps"].append({"name": name, "ok": bool(ok), "detail": detail})
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        return ok

    # 1. import check
    p = subprocess.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, %r); import taskledger.api, taskledger.server, taskledger.storage" % os.path.join(ROOT, "src")],
                       capture_output=True, text=True)
    step("imports", p.returncode == 0, p.stderr.strip() or "all modules import")

    # 2. unit tests
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", os.path.join(ROOT, "tests")],
                       capture_output=True, text=True, cwd=ROOT)
    step("pytest", p.returncode == 0, (p.stdout.strip().splitlines() or [""])[-1])

    # 3. live smoke test
    port = free_port()
    env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"))
    srv = subprocess.Popen([sys.executable, "-m", "taskledger.server", str(port)],
                           env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    try:
        up = False
        for _ in range(50):
            try:
                if http("GET", base + "/api/health", timeout=1)[0] == 200:
                    up = True
                    break
            except Exception:
                time.sleep(0.2)
        step("server_up", up, f"port {port}")
        if up:
            s, page = http("GET", base + "/")
            step("frontend", s == 200 and "<html" in page.lower(), f"GET / -> {s}")
            s, t = http("POST", base + "/api/tasks", {"title": "smoke"})
            step("post_task", s == 201, f"POST -> {s}")
            s, p2 = http("GET", base + "/api/tasks")
            step("list_contains_task", s == 200 and any(x["title"] == "smoke" for x in p2["tasks"]), f"GET -> {s}")
            s, _ = http("DELETE", base + f"/api/tasks/{t['id']}")
            step("delete_task", s == 204, f"DELETE -> {s}")
    finally:
        srv.terminate()
        srv.wait(timeout=5)

    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results["all_ok"] = all(r["ok"] for r in results["steps"])
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print("RESULT:", "OK" if results["all_ok"] else "FAILED", "->", RESULT_PATH)
    sys.exit(0 if results["all_ok"] else 1)


if __name__ == "__main__":
    main()
