# taskledger

Zero-dependency task ledger (EXP-01 deliverable of `arena.ai_breakthrough`). Stdlib only (C-1);
frontend fully inline (C-2).

## Run

```bash
cd src && python3 -m taskledger.server 8000
# open http://127.0.0.1:8000/
```

## API

| Method | Path | Behavior |
|---|---|---|
| GET | `/api/health` | `200 {"status":"ok"}` |
| GET | `/api/tasks` | `200 {"tasks":[…]}` |
| POST | `/api/tasks` | `201` created task; `400` if title empty |
| GET/PATCH/DELETE | `/api/tasks/{id}` | `200` / `204` (DELETE) / `404` |

## Architecture

- `api.py` — HTTP-free routing core (`dispatch()`), unit-testable without sockets.
- `storage.py` — pluggable storage behind a 5-method interface (create/list/get/update/delete).
- `server.py` — thin `http.server` adapter + static file serving (path-traversal guarded).
- `static/index.html` — single-page frontend, inline CSS/JS, relative URLs only.

Validation: `python3 benchmarks/run_suite.py` (unit tests + live smoke test).
