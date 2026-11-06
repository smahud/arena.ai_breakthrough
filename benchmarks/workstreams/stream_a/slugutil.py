"""Stream A: slugify. Zero cross-stream imports by design (EXP-02 S3)."""
import re

def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return s.strip("-")
