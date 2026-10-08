#!/usr/bin/env python3
"""Rebuild and audit one complete canonical s5 boundary for a reply27 s4 class."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    return tuple([i for i in range(64) if (lo >> i) & 1]
                 + [64 + i for i in range(57) if (hi >> i) & 1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--class-lo", type=int, required=True)
    ap.add_argument("--class-hi", type=int, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite boundary audit: {args.out}")

    class_key = (args.class_lo, args.class_hi)
    class_points = points(class_key)
    if (len(class_points) != 4 or has_forbidden_quad(class_points)
            or tuple(d4_canonical_key(class_points)) != class_key):
        raise SystemExit(f"unsafe or noncanonical s4 class: {class_key}")

    root = {60, 27}
    vertices = set(legal_after(root))
    if len(vertices) != 119:
        raise SystemExit(f"expected 119 legal third moves, got {len(vertices)}")
    coverage = set()
    for first in vertices:
        for second in legal_after(root | {first}):
            if second > first and tuple(d4_canonical_key([60, 27, first, second])) == class_key:
                coverage.update((first, second))
    if not coverage:
        raise SystemExit(f"s4 class is not reachable from reply27 root: {class_key}")

    raw_children = []
    for move in legal_after(set(class_points)):
        child = tuple(sorted((*class_points, move)))
        if len(child) != 5 or has_forbidden_quad(child):
            raise SystemExit(f"unsafe legal extension: {class_key} + {move}")
        canonical = tuple(d4_canonical_key(child))
        if canonical != tuple(d4_canonical_key(points(canonical))):
            raise SystemExit(f"canonicalization failed for extension: {canonical}")
        raw_children.append(canonical)
    children = sorted(set(raw_children))
    if not children:
        raise SystemExit(f"s4 class has no legal canonical s5 children: {class_key}")

    cache: dict[tuple[int, int], int] = {}
    duplicate_rows = 0
    for line_no, row in enumerate(csv.reader(args.cache.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid exact s5 cache row {line_no}: {row}")
        key = (int(row[1]), int(row[2]))
        value = int(row[4])
        key_points = points(key)
        if (len(key_points) != 5 or has_forbidden_quad(key_points)
                or tuple(d4_canonical_key(key_points)) != key or value not in (1, 2)):
            raise SystemExit(f"unsafe, noncanonical, or nonexact cache row {line_no}: {row}")
        old = cache.get(key)
        if old is not None:
            if old != value:
                raise SystemExit(f"exact verdict conflict at {key}: {old} vs {value}")
            duplicate_rows += 1
        cache[key] = value

    statuses = {key: cache.get(key) for key in children}
    counts = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    for value in statuses.values():
        counts[{1: "WIN", 2: "LOSS", None: "UNKNOWN"}[value]] += 1
    status = ("WIN" if counts["WIN"] else
              "LOSS" if counts["UNKNOWN"] == 0 and counts["LOSS"] == len(children) else
              "UNKNOWN")
    if status == "LOSS" and not all(statuses[key] == 2 for key in children):
        raise SystemExit("LOSS boundary is not fully covered by exact LOSS children")

    inputs = [args.cache, Path(__file__).resolve(), EDGE / "dfpn_edge_classes.py"]
    report = {
        "schema": "n11-reply27-s4-complete-s5-boundary-audit-v1",
        "root": [60, 27],
        "class": {"key": list(class_key), "points": list(class_points),
                  "coverage_vertices": sorted(coverage)},
        "boundary": {
            "generation": "all legal s5 extensions, D4-canonicalized and deduplicated",
            "canonical_children": len(children),
            "raw_legal_extensions": len(raw_children),
            "duplicate_extensions_collapsed_by_canonicalization": len(raw_children) - len(children),
            "status_counts": dict(sorted(counts.items())),
            "status": status,
            "children": [{"key": list(key), "verdict": statuses[key]} for key in children],
        },
        "cache": {"path": args.cache.resolve().relative_to(ROOT).as_posix(),
                  "sha256": sha256(args.cache), "exact_entries": len(cache),
                  "duplicate_same_verdict_rows": duplicate_rows, "conflicts": 0},
        "claim": "Only exact cache WIN/LOSS rows are propagated. UNKNOWN means at least one canonical child lacks an exact verdict.",
        "sources": [{"path": p.resolve().relative_to(ROOT).as_posix(),
                     "sha256": sha256(p)} for p in inputs],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"REPLY27_S4_BOUNDARY_AUDIT_OK class={class_key} children={len(children)} status={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
