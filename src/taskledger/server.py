"""Stdlib HTTP server wrapping TaskAPI + static frontend. Run: python3 -m taskledger.server PORT"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .api import TaskAPI
from .storage import InMemoryStorage

STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


def make_handler(api):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status, payload, ctype="application/json"):
            if payload is None:
                self.send_response(status)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            raw = json.dumps(payload).encode() if ctype == "application/json" else payload
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _route(self, method):
            path = self.path.split("?", 1)[0]
            if not path.startswith("/api"):
                return self._static(path)
            length = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(length)) if length else None
                status, payload = api.dispatch(method, path, body)
            except Exception as exc:  # observed-error containment, not concealment: surfaced as 500
                status, payload = 500, {"error": f"{type(exc).__name__}: {exc}"}
            self._send(status, payload)

        def _static(self, path):
            if path == "/":
                path = "/index.html"
            fp = os.path.normpath(os.path.join(STATIC, path.lstrip("/")))
            if not fp.startswith(STATIC) or not os.path.isfile(fp):
                return self._send(404, {"error": "not found"})
            ctype = "text/html; charset=utf-8" if fp.endswith(".html") else "text/plain"
            with open(fp, "rb") as f:
                self._send(200, f.read(), ctype)

        def do_GET(self):
            self._route("GET")

        def do_POST(self):
            self._route("POST")

        def do_PATCH(self):
            self._route("PATCH")

        def do_DELETE(self):
            self._route("DELETE")

        def log_message(self, *args):
            pass

    return Handler


def serve(host="127.0.0.1", port=8000, storage=None):
    api = TaskAPI(storage if storage is not None else InMemoryStorage())
    return ThreadingHTTPServer((host, port), make_handler(api))


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = serve("0.0.0.0", port)
    print(f"taskledger listening on {port}", flush=True)
    srv.serve_forever()
