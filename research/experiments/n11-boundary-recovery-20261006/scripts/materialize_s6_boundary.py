#!/usr/bin/env python3
"""Materialize complete canonical safe s6 boundaries of canonical safe s5 keys."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def points_from_key(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < (1 << 64) and 0 <= hi < (1 << 57)):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1] + [i + 64 for i in range(57) if hi >> i & 1])


def checked_key(key: tuple[int, int], stones: int) -> tuple[int, int]:
    pts = points_from_key(key)
    if len(pts) != stones or has_forbidden_quad(pts):
        raise ValueError(f"not a safe s{stones} key: {key}")
    canonical = tuple(d4_canonical_key(pts))
    if canonical != key:
        raise ValueError(f"key is not canonical (lo,hi): {key}, canonical={canonical}")
    return canonical


def parse_range(text: str) -> tuple[int, int]:
    try:
        lo_text, hi_text = text.split(":", 1)
        return int(lo_text), int(hi_text)
    except Exception as exc:
        raise argparse.ArgumentTypeError("expected LO:HI") from exc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parent-lo-hi", type=parse_range, action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--meta-out", type=Path, required=True)
    ap.add_argument("--probe-out", type=Path, required=True)
    ap.add_argument("--probes-per-parent", type=int, default=8)
    args = ap.parse_args()
    if args.probes_per_parent < 0:
        ap.error("--probes-per-parent must be nonnegative")

    parents = [checked_key(tuple(k), 5) for k in args.parent_lo_hi]
    if len(set(parents)) != len(parents):
        raise SystemExit("duplicate parent key")

    # child key -> set of selected canonical parent indices
    incidence: dict[tuple[int, int], set[int]] = defaultdict(set)
    child_legal: dict[tuple[int, int], int] = {}
    per_parent: list[list[tuple[int, int]]] = []
    for pi, parent in enumerate(parents):
        parent_points = set(points_from_key(parent))
        children: set[tuple[int, int]] = set()
        for point in legal_after(parent_points):
            child = tuple(d4_canonical_key([*parent_points, point]))
            checked_key(child, 6)
            children.add(child)
            incidence[child].add(pi)
        per_parent.append(sorted(children))
        for child in children:
            nlegal = len(legal_after(set(points_from_key(child))))
            old = child_legal.setdefault(child, nlegal)
            if old != nlegal:
                raise SystemExit(f"inconsistent legal count for {child}")

    # Independent reverse-incidence audit by deleting each point from every child.
    for child, parent_indices in incidence.items():
        cpoints = points_from_key(child)
        predecessors = {tuple(d4_canonical_key([x for x in cpoints if x != removed])) for removed in cpoints}
        for pi in parent_indices:
            if parents[pi] not in predecessors:
                raise SystemExit(f"reverse incidence failure: parent={parents[pi]} child={child}")

    # Exact replay input rows: tag,seq,stones,lo,hi,legal,0,1,0,0,0.
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        for seq, key in enumerate(sorted(incidence)):
            lo, hi = key
            writer.writerow(["target", seq, 6, lo, hi, child_legal[key], 0, 1, 0, 0, 0])

    parent_children = [{"key": list(k), "child_count": len(per_parent[i])} for i, k in enumerate(parents)]
    meta = {
        "schema": "n11-s6-complete-boundary-v1",
        "canonical_key_convention": "(lo,hi); lo contains points 0..63, hi contains points 64..120",
        "canonical_ordering": "D4 minimization compares (hi,lo) lexicographically, then stores/serializes the result as (lo,hi), matching dfpn_edge_classes.d4_canonical_key",
        "parent_keys": [list(k) for k in parents],
        "parents": parent_children,
        "canonical_children": [
            {"key": list(k), "legal_count": child_legal[k], "parent_indices": sorted(incidence[k])}
            for k in sorted(incidence)
        ],
        "child_parent_indices": {f"{k[0]}:{k[1]}": sorted(v) for k, v in sorted(incidence.items())},
        "complete_boundary_count": len(incidence),
        "parent_child_relation_count": sum(map(len, per_parent)),
        "generation": "complete: every legal_after(parent) extension was D4-canonicalized and safety-checked",
        "reverse_incidence_audit": "passed by independently deleting each point from each child and canonicalizing the resulting s5 key",
        "probe_policy": f"heuristic scheduling only: for each parent, choose its first {args.probes_per_parent} children sorted by (legal_count, key); union deduplicated across parents",
    }
    args.meta_out.parent.mkdir(parents=True, exist_ok=True)
    args.meta_out.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    chosen: set[tuple[int, int]] = set()
    for children in per_parent:
        chosen.update(sorted(children, key=lambda k: (child_legal[k], k))[:args.probes_per_parent])
    args.probe_out.parent.mkdir(parents=True, exist_ok=True)
    with args.probe_out.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(["# heuristic scheduling only; union of per-parent lowest-legal-count children"])
        writer.writerow(["tag", "seq", "stones", "lo", "hi", "legal", "is_or", "budget", "result", "nodes", "wall_s"])
        for seq, key in enumerate(sorted(chosen, key=lambda k: (child_legal[k], k))):
            lo, hi = key
            writer.writerow(["target", seq, 6, lo, hi, child_legal[key], 0, 1, 0, 0, 0])

    print(json.dumps({"parents": parent_children, "canonical_children": len(incidence),
                      "parent_child_relations": sum(map(len, per_parent)), "probe_union": len(chosen)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
