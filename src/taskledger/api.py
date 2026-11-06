"""HTTP-free routing core: dispatch(method, path, body) -> (status, payload).

Keeping routing logic out of the socket layer makes it unit-testable without a server
and lets EXP-06 swap storage without touching this file.
"""


class TaskAPI:
    def __init__(self, storage):
        self.storage = storage

    def dispatch(self, method, path, body=None):
        if path == "/api/health":
            return 200, {"status": "ok"}

        if path == "/api/tasks":
            if method == "GET":
                return 200, {"tasks": self.storage.list()}
            if method == "POST":
                data = body or {}
                title = str(data.get("title", "")).strip()
                if not title:
                    return 400, {"error": "title required"}
                return 201, self.storage.create(title)

        if path.startswith("/api/tasks/"):
            tid = path.rsplit("/", 1)[1]
            if not tid:
                return 404, {"error": "not found"}
            if method == "GET":
                t = self.storage.get(tid)
                return (200, t) if t else (404, {"error": "not found"})
            if method == "PATCH":
                t = self.storage.update(tid, body or {})
                return (200, t) if t else (404, {"error": "not found"})
            if method == "DELETE":
                return (204, None) if self.storage.delete(tid) else (404, {"error": "not found"})

        return 404, {"error": "no route"}
