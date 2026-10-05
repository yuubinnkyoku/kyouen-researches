#!/usr/bin/env python3
"""Verify a complete exact-LOSS s5 boundary for one reply=27 s4 class."""
from __future__ import annotations
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

FIRST, R2 = 60, 27

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-lo", type=int, required=True)
    ap.add_argument("--class-hi", type=int, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--expected-children", type=int)
    ap.add_argument("--allow-extra", action="store_true", help="allow unrelated s5 rows in a merged cache; only the target boundary is required to be LOSS")
    args = ap.parse_args()
    target = (args.class_lo, args.class_hi)

    verdict = {}
    with args.cache.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                raise SystemExit(f"unexpected cache row: {row}")
            key = (int(row[1]), int(row[2]))
            stones = int(row[3])
            value = int(row[4])
            if stones != 5:
                raise SystemExit(f"non-s5 cache row: {row}")
            if value not in (1, 2):
                raise SystemExit(f"invalid verdict for {key}: {value}")
            if not args.allow_extra and value != 2:
                raise SystemExit(f"non-LOSS verdict for {key}: {value}")
            old = verdict.get(key)
            if old is not None and old != value:
                raise SystemExit(f"CONFLICT {key}: {old} vs {value}")
            verdict[key] = value

    base = {FIRST, R2}
    groups = defaultdict(list)
    for a in legal_after(base):
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([FIRST, R2, a, b])
            if key == target:
                groups[key].append((a, b))
    edges = groups.get(target, [])
    if not edges:
        raise SystemExit(f"target s4 class does not exist: {target}")

    children = set()
    coverage = set()
    for a, b in edges:
        coverage.update((a, b))
        occ = base | {a, b}
        for z in legal_after(occ):
            children.add(d4_canonical_key(list(occ | {z})))

    if args.expected_children is not None and len(children) != args.expected_children:
        raise SystemExit(
            f"child-count mismatch: expected={args.expected_children} got={len(children)}"
        )
    cached = set(verdict)
    missing = children - cached
    extra = cached - children
    nonloss_children = sorted(k for k in children if verdict.get(k) != 2)
    if missing or nonloss_children or (extra and not args.allow_extra):
        raise SystemExit(
            "cache boundary mismatch: "
            f"missing={len(missing)} nonloss={len(nonloss_children)} "
            f"extra={len(extra)}"
        )

    out = {
        "root": [FIRST, R2],
        "class_key": list(target),
        "raw_edges": [list(e) for e in sorted(edges)],
        "coverage": sorted(coverage),
        "canonical_s5_children": len(children),
        "cached_loss_children": len(children),
        "cache_rows_total": len(verdict),
        "cache_extra_rows": len(extra),
        "cache_boundary_exact": True,
        "allow_extra": args.allow_extra,
        "s4_verdict": "LOSS",
        "reason": "all canonical s5 children are exact LOSS",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("REPLY27_LOSS_CLASS_CACHE_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
