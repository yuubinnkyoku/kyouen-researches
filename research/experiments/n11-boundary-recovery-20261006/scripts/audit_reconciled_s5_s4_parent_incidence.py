#!/usr/bin/env python3
"""Verify reply27 s4 parents and full s5 boundaries of one exact s5 WIN."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
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


def safe_canonical(key: tuple[int, int], stones: int) -> bool:
    pts = points(key)
    return (len(pts) == stones and not has_forbidden_quad(pts)
            and tuple(d4_canonical_key(pts)) == key)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--s5-lo", type=int, required=True)
    ap.add_argument("--s5-hi", type=int, required=True)
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--s5-boundary-audit", type=Path, required=True)
    ap.add_argument("--s4-audit", type=Path, action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite: {args.out}")

    target = (args.s5_lo, args.s5_hi)
    if not safe_canonical(target, 5):
        raise SystemExit(f"unsafe or noncanonical s5 key: {target}")
    s5_boundary = json.loads(args.s5_boundary_audit.read_text(encoding="utf-8"))
    parent_row = s5_boundary["targets"]["parents"]
    if (len(parent_row) != 1 or parent_row[0]["key"] != list(target)
            or parent_row[0]["outcome"] != "WIN"
            or parent_row[0]["child_count"] != 89
            or parent_row[0]["counts"] != {"WIN": 89}
            or not parent_row[0]["full_child_coverage"]):
        raise SystemExit("complete all-WIN S6 boundary audit does not certify the target s5 WIN")

    cache: dict[tuple[int, int], int] = {}
    for line_no, row in enumerate(csv.reader(args.s5_cache.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 cache row {line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if not safe_canonical(key, 5) or verdict not in (1, 2):
            raise SystemExit(f"unsafe, noncanonical, or nonexact cache row {line_no}: {row}")
        if key in cache and cache[key] != verdict:
            raise SystemExit(f"exact s5 verdict conflict at {key}")
        cache[key] = verdict
    if cache.get(target) != 1:
        raise SystemExit("the fully S6-derived s5 WIN is missing from the merged exact cache")

    root = {60, 27}
    groups: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for first in legal_after(root):
        for second in legal_after(root | {first}):
            if second > first:
                groups[tuple(d4_canonical_key([60, 27, first, second]))].append((first, second))
    if len(groups) != 3384:
        raise SystemExit(f"reply27 class geometry mismatch: {len(groups)}")

    target_points = set(points(target))
    incidences: dict[tuple[int, int], set[int]] = defaultdict(set)
    for removed in sorted(target_points):
        parent_points = target_points - {removed}
        parent = tuple(d4_canonical_key(parent_points))
        if parent not in groups:
            continue
        if removed not in legal_after(parent_points):
            raise SystemExit(f"target is not a legal extension of deleted-point parent {parent}")
        incidences[parent].add(removed)

    if not incidences:
        raise SystemExit("no reply27 s4 parent incidence found")
    supplied_audits = {}
    for path in args.s4_audit:
        report = json.loads(path.read_text(encoding="utf-8"))
        key = tuple(report.get("class", {}).get("key", []))
        if key in supplied_audits:
            raise SystemExit(f"duplicate s4 audit for {key}")
        supplied_audits[key] = (path, report)
    if set(supplied_audits) != set(incidences):
        raise SystemExit(f"s4 audit set differs from geometry parents: {sorted(supplied_audits)} vs {sorted(incidences)}")

    audited_classes = []
    for parent in sorted(incidences):
        parent_points = set(points(parent))
        if not safe_canonical(parent, 4) or parent not in groups:
            raise SystemExit(f"unsafe/unreachable s4 parent: {parent}")
        children = set()
        for move in legal_after(parent_points):
            child_points = parent_points | {move}
            if len(child_points) != 5 or has_forbidden_quad(child_points):
                raise SystemExit(f"unsafe legal s5 extension: {parent} + {move}")
            child = tuple(d4_canonical_key(child_points))
            if not safe_canonical(child, 5):
                raise SystemExit(f"unsafe canonical s5 child: {child}")
            children.add(child)
        if target not in children:
            raise SystemExit(f"target s5 key is absent from complete parent boundary: {parent}")
        counts = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
        for child in children:
            verdict = cache.get(child)
            counts[{1: "WIN", 2: "LOSS", None: "UNKNOWN"}[verdict]] += 1
        if counts["WIN"] == 0:
            raise SystemExit(f"s4 class lacks exact WIN s5 child: {parent}")
        path, report = supplied_audits[parent]
        audited_children = {tuple(item["key"]) for item in report["boundary"]["children"]}
        if (audited_children != children or report["boundary"]["status"] != "WIN"
                or report["boundary"]["status_counts"] != dict(sorted(counts.items()))):
            raise SystemExit(f"stored full s4 boundary audit disagrees with regenerated geometry: {parent}")
        audited_classes.append({
            "key": list(parent),
            "deleted_s5_points": sorted(incidences[parent]),
            "coverage_vertices": report["class"]["coverage_vertices"],
            "canonical_s5_children": len(children),
            "status_counts": dict(sorted(counts.items())),
            "status": "WIN",
            "target_child_present": True,
            "full_boundary_audit": {
                "path": path.resolve().relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
            },
        })

    source_paths = [args.s5_cache, args.s5_boundary_audit, Path(__file__).resolve(), EDGE / "dfpn_edge_classes.py"]
    report = {
        "schema": "n11-reply27-s5-win-s4-parent-incidence-audit-v1",
        "root": [60, 27],
        "target_s5": {"key": list(target), "verdict": "WIN",
                      "source_boundary_audit": {"path": args.s5_boundary_audit.resolve().relative_to(ROOT).as_posix(),
                                                "sha256": sha256(args.s5_boundary_audit),
                                                "canonical_s6_children": 89,
                                                "status_counts": {"WIN": 89}}},
        "reply27_s4_class_count": len(groups),
        "parent_incidence_count": sum(map(len, incidences.values())),
        "reply27_s4_parents": audited_classes,
        "cache": {"path": args.s5_cache.resolve().relative_to(ROOT).as_posix(),
                  "sha256": sha256(args.s5_cache), "exact_entries": len(cache), "conflicts": 0},
        "claim": "Every listed parent is a legal canonical reply27 s4 parent of the exact s5 WIN. Its complete canonical s5 boundary was regenerated and independently compared with the saved class audit; every listed class is WIN by an exact s5 child.",
        "sources": [{"path": path.resolve().relative_to(ROOT).as_posix(), "sha256": sha256(path)}
                    for path in source_paths],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"REPLY27_S5_PARENT_INCIDENCE_AUDIT_OK s5={target} s4_parents={len(audited_classes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
