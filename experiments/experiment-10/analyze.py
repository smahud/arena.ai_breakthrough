#!/usr/bin/env python3
"""EXP-10: reproducible interval intersections from preserved raw JSON, no network."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "evidence/phase2/exp10"


def analyze(trial):
    rows = [json.loads((DATA / f"{trial}-{i}.json").read_text()) for i in range(3)]
    assert all(r["trial"] == trial and r["index"] == i and r["end_ns"] > r["start_ns"]
               for i, r in enumerate(rows))
    order = sorted(rows, key=lambda r: r["start_ns"])
    span = (max(r["end_ns"] for r in rows) - min(r["start_ns"] for r in rows)) / 1e9
    pairs = [(a["index"], b["index"], round((min(a["end_ns"], b["end_ns"]) -
             max(a["start_ns"], b["start_ns"])) / 1e6, 3))
             for i, a in enumerate(rows) for b in rows[i+1:]
             if min(a["end_ns"], b["end_ns"]) > max(a["start_ns"], b["start_ns"])]
    starts = [r["start_ns"] for r in order]
    gaps_ms = [round((b-a)/1e6, 3) for a, b in zip(starts, starts[1:])]
    print(trial, "expected_s=", rows[0]["expected_seconds"], "span_s=", round(span, 4),
          "overlapping_pairs=", len(pairs), "/3", "pairs_ms=", pairs,
          "start_order=", [r["index"] for r in order], "start_gaps_ms=", gaps_ms)
    for r in order:
        print(" ", trial, r["index"], "start_ns=", r["start_ns"],
              "end_ns=", r["end_ns"], "inside_ms=", round((r["end_ns"]-r["start_ns"])/1e6, 3))
    return span


if __name__ == "__main__":
    print("Source: 12 JSON files generated inside bash calls; current trial interval intersections.")
    spans = {trial: analyze(trial) for trial in ("S1", "S2", "L1", "L2")}
    for prefix in ("S", "L"):
        two = [spans[f"{prefix}{i}"] for i in (1, 2)]
        print(prefix, "replicate span range_s=", [round(min(two), 4), round(max(two), 4)])
    assert len(list(DATA.glob('S[12]-*.json'))) == 6
    assert len(list(DATA.glob('L[12]-*.json'))) == 6
