#!/usr/bin/env python3
"""EXP-10: unique per-call, inside-tool epoch interval; stdlib only."""
import json
import pathlib
import sys
import time


def main():
    trial, index, seconds = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    primary = trial in {"S1", "S2", "L1", "L2", "M1", "D1"} and index in (0, 1, 2) and seconds in (0.25, 0.75, 0.6)
    exploratory_matched = trial == "X1" and index in (0, 1, 2, 3) and seconds == 1.0
    if not (primary or exploratory_matched):
        raise SystemExit("unexpected EXP-10 trial, index or duration")
    output = pathlib.Path(__file__).resolve().parents[2] / "evidence/phase2/exp10" / f"{trial}-{index}.json"
    start = time.time_ns()
    time.sleep(seconds)
    end = time.time_ns()
    record = {"trial": trial, "index": index, "expected_seconds": seconds,
              "start_ns": start, "end_ns": end, "path": str(output)}
    output.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
