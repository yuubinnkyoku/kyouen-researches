#!/usr/bin/env python3
"""Derive exact s5 verdicts from a fully enumerated hard9 s6 boundary.

For each hard s5 parent:
- any exact LOSS s6 child proves the s5 LOSS (five stones is an AND node);
- all canonical s6 children exact WIN proves the s5 WIN;
- otherwise it remains UNKNOWN and is not emitted.

The script rejects missing boundary keys and conflicting replay verdicts.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", type=Path, required=True)
    ap.add_argument("--replay", nargs="+", required=True)
    ap.add_argument("--cache-out", type=Path, required=True)
    args = ap.parse_args()

    meta = json.loads(args.meta.read_text(encoding="utf-8"))
    hard = [tuple(x) for x in meta["hard_s5"]]
    parents = {
        tuple(map(int, key.split(":"))): list(value)
        for key, value in meta["parents"].items()
    }
    expected = set(parents)
    result = {}

    paths = []
    for pattern in args.replay:
        paths.extend(glob.glob(pattern))
    if not paths:
        raise SystemExit("no replay files")

    for path in sorted(set(paths)):
        with open(path, newline="", encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or row[0] != "replay":
                    continue
                key = (int(row[9]), int(row[10]))
                verdict = int(row[6])
                if key not in expected:
                    raise SystemExit(f"unexpected boundary key {key}")
                if verdict not in (0, 1, 2):
                    raise SystemExit(f"bad replay verdict {verdict}: {key}")
                old = result.get(key)
                if old is not None and old != verdict:
                    raise SystemExit(
                        f"CONFLICT key={key} old={old} new={verdict}"
                    )
                result[key] = verdict

    missing = expected - set(result)
    if missing:
        raise SystemExit(f"missing boundary results: {len(missing)}")
    if len(expected) != 816:
        raise SystemExit(f"expected 816 canonical s6, got {len(expected)}")

    child = [[] for _ in hard]
    for key, ps in parents.items():
        for p in ps:
            child[p].append(key)

    classified = []
    status = []
    for i, key in enumerate(hard):
        vals = [result[ch] for ch in child[i]]
        if 2 in vals:
            verdict = 2
            label = "LOSS"
        elif vals and all(v == 1 for v in vals):
            verdict = 1
            label = "WIN"
        else:
            verdict = 0
            label = "UNKNOWN"
        status.append(label)
        if verdict:
            classified.append((key, verdict))
        print(
            "HARD_S5",
            i,
            key,
            label,
            "children",
            len(vals),
            "win",
            sum(v == 1 for v in vals),
            "loss",
            sum(v == 2 for v in vals),
            "unknown",
            sum(v == 0 for v in vals),
        )

    args.cache_out.parent.mkdir(parents=True, exist_ok=True)
    with args.cache_out.open("w", encoding="utf-8") as fp:
        fp.write(
            "# s5 verdict cache: n=11 schema=1 "
            "(boundary-derived exact verdicts; UNKNOWN omitted)\n"
        )
        for (lo, hi), verdict in sorted(classified):
            fp.write(f"s5verdict,{lo},{hi},5,{verdict},0\n")

    print(
        json.dumps(
            {
                "boundary_s6": len(expected),
                "classified_s5": len(classified),
                "status_counts": {
                    s: status.count(s) for s in ("WIN", "LOSS", "UNKNOWN")
                },
            },
            sort_keys=True,
        )
    )
    print("HARD9_S5_CACHE_DERIVATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
