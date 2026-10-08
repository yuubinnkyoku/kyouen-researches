#!/usr/bin/env python3
"""Materialize only exact-cache UNKNOWN children from a verified s4 boundary."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--boundary-audit", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--targets-out", type=Path, required=True)
    ap.add_argument("--manifest-out", type=Path, required=True)
    args = ap.parse_args()
    if args.targets_out.exists() or args.manifest_out.exists():
        raise SystemExit("refusing to overwrite an existing materialization")

    audit = json.loads(args.boundary_audit.read_text(encoding="utf-8"))
    if (audit.get("schema") != "n11-reply27-s4-complete-s5-boundary-audit-v1"
            or audit.get("cache", {}).get("sha256") != sha256(args.cache)
            or audit.get("cache", {}).get("conflicts") != 0):
        raise SystemExit("boundary audit is stale or conflict-bearing")
    class_key = tuple(map(int, audit.get("class", {}).get("key", [])))
    class_points = points(class_key)
    if (len(class_key) != 2 or len(class_points) != 4 or has_forbidden_quad(class_points)
            or tuple(d4_canonical_key(class_points)) != class_key):
        raise SystemExit("class key is unsafe or noncanonical")

    cache = {}
    for line_no, row in enumerate(csv.reader(args.cache.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid exact s5 cache row {args.cache}:{line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if (len(points(key)) != 5 or has_forbidden_quad(points(key))
                or tuple(d4_canonical_key(points(key))) != key or verdict not in (1, 2)):
            raise SystemExit(f"invalid/noncanonical exact cache row {args.cache}:{line_no}: {row}")
        if key in cache and cache[key] != verdict:
            raise SystemExit(f"exact verdict conflict for {key}")
        cache[key] = verdict

    children = set()
    for move in legal_after(set(class_points)):
        child_points = tuple(sorted((*class_points, move)))
        if not has_forbidden_quad(child_points):
            children.add(tuple(d4_canonical_key(child_points)))
    audited = audit.get("boundary", {}).get("children", [])
    audited_status = {tuple(map(int, row["key"])): row.get("verdict") for row in audited}
    if len(children) != audit.get("boundary", {}).get("canonical_children") \
            or len(audited_status) != len(children) or set(audited_status) != children:
        raise SystemExit("complete canonical s5 boundary differs from independent geometry")

    statuses = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    unknown = []
    for key in sorted(children):
        actual = cache.get(key)
        if audited_status[key] != actual:
            raise SystemExit(f"boundary audit/cache verdict mismatch for {key}")
        statuses["UNKNOWN" if actual is None else "WIN" if actual == 1 else "LOSS"] += 1
        if actual is None:
            legal = len(legal_after(set(points(key))))
            unknown.append(["reply27-dual-tight-unknown", len(unknown), 5,
                            key[0], key[1], legal, 0, 0, 0, 0, 0])
    if (dict(sorted(statuses.items())) != audit.get("boundary", {}).get("status_counts")
            or audit.get("boundary", {}).get("status") != "UNKNOWN"
            or not unknown):
        raise SystemExit("boundary status counts differ from exact cache or are not UNKNOWN")

    args.targets_out.parent.mkdir(parents=True, exist_ok=True)
    with args.targets_out.open("w", newline="", encoding="utf-8") as stream:
        stream.write("# complete canonical s5 UNKNOWN boundary; no verdict asserted\n")
        csv.writer(stream, lineterminator="\n").writerows(unknown)
    code = Path(__file__).resolve()
    edge = ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py"
    manifest = {
        "schema": "n11-dual-tight-class-unknown-materialization-v1",
        "class_key": list(class_key),
        "boundary_children": len(children),
        "boundary_status_counts": dict(sorted(statuses.items())),
        "unknown_targets": len(unknown),
        "sources": [
            {"path": str(p.resolve().relative_to(ROOT.resolve())).replace("\\", "/"),
             "sha256": sha256(p), "bytes": p.stat().st_size}
            for p in (args.boundary_audit, args.cache, code, edge)
        ],
        "output": {"path": str(args.targets_out.resolve().relative_to(ROOT.resolve())).replace("\\", "/"),
                   "sha256": sha256(args.targets_out), "bytes": args.targets_out.stat().st_size},
        "claim": "Geometry rebuilt the full canonical s5 boundary; only children absent from the exact cache are materialized as unresolved targets.",
    }
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"class": list(class_key), "children": len(children),
                      "statuses": dict(sorted(statuses.items())), "unknown_targets": len(unknown),
                      "targets_sha256": sha256(args.targets_out),
                      "manifest_sha256": sha256(args.manifest_out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
