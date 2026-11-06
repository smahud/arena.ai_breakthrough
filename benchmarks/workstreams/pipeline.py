"""EXP-02 integration: composes the three independently-built streams."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for s in ("stream_a", "stream_b", "stream_c"):
    sys.path.insert(0, os.path.join(HERE, s))
from slugutil import slugify          # noqa: E402
from textstats import textstats       # noqa: E402
from jsonstore import load, save      # noqa: E402

def process(title: str, body: str, store_path: str) -> dict:
    rec = {"slug": slugify(title), "stats": textstats(body)}
    data = load(store_path)
    data[rec["slug"]] = rec["stats"]
    save(store_path, data)
    return rec
