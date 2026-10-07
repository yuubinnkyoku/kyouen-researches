#!/usr/bin/env python3
"""Verify an s4 WIN derived from a fully exact-WIN canonical s6 boundary."""
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


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def checked_key(key: tuple[int, int], stones: int) -> tuple[int, int]:
    occupied = points(key)
    if len(occupied) != stones or has_forbidden_quad(occupied):
        raise ValueError(f"unsafe s{stones} key: {key}")
    canonical = tuple(d4_canonical_key(occupied))
    if canonical != key:
        raise ValueError(f"noncanonical s{stones} key: {key} -> {canonical}")
    return key


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_s5_cache(path: Path) -> dict[tuple[int, int], int]:
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid s5 cache row {path}:{line_no}: {row}")
            key = checked_key((int(row[1]), int(row[2])), 5)
            verdict = int(row[4])
            if verdict not in (1, 2):
                raise ValueError(f"non-exact s5 cache row {path}:{line_no}: {row}")
            previous = result.setdefault(key, verdict)
            if previous != verdict:
                raise ValueError(f"s5 cache conflict {key}: {previous} vs {verdict}")
    return result


def read_s6_raw(path: Path) -> dict[tuple[int, int], dict]:
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or row[0] != "replay" or int(row[2]) != 6 or int(row[4]) != 1:
                raise ValueError(f"invalid s6 AND replay {path}:{line_no}: {row}")
            key = checked_key((int(row[9]), int(row[10])), 6)
            item = {"legal_count": int(row[3]), "verdict": int(row[6]), "nodes": int(row[7])}
            if item["verdict"] not in (0, 1, 2) or item["nodes"] < 0 or key in result:
                raise ValueError(f"invalid/duplicate s6 replay {key}: {row}")
            actual_legal = len(legal_after(set(points(key))))
            if item["legal_count"] != actual_legal:
                raise ValueError(f"s6 legal count mismatch {key}: {item['legal_count']} != {actual_legal}")
            result[key] = item
    return result


def boundary(parent: tuple[int, int], stones: int) -> set[tuple[int, int]]:
    occupied = set(points(parent))
    children = set()
    for move in legal_after(occupied):
        child_points = tuple(sorted((*occupied, move)))
        if len(child_points) != stones or has_forbidden_quad(child_points):
            raise ValueError(f"illegal/unsafe extension {parent} + {move}")
        child = tuple(d4_canonical_key(child_points))
        checked_key(child, stones)
        children.add(child)
    return children


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--s4-lo", type=int, required=True)
    ap.add_argument("--s4-hi", type=int, required=True)
    ap.add_argument("--base-s5-cache", type=Path, required=True)
    ap.add_argument("--merged-s5-cache", type=Path, required=True)
    ap.add_argument("--derived-s5-cache", type=Path, required=True)
    ap.add_argument("--s6-summary", type=Path, required=True)
    ap.add_argument("--s6-raw", type=Path, required=True)
    ap.add_argument("--s6-exact-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    s4 = checked_key((args.s4_lo, args.s4_hi), 4)
    base = read_s5_cache(args.base_s5_cache)
    merged = read_s5_cache(args.merged_s5_cache)
    derived = read_s5_cache(args.derived_s5_cache)
    raw = read_s6_raw(args.s6_raw)
    summary = json.loads(args.s6_summary.read_text(encoding="utf-8"))

    children = boundary(s4, 5)
    base_partition = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    for child in children:
        value = base.get(child)
        base_partition[{1: "WIN", 2: "LOSS", None: "UNKNOWN"}[value]] += 1
    if base_partition["WIN"]:
        raise SystemExit(f"base cache already has a WIN child; this is not the expected frontier: {base_partition}")

    exact_rows = {key: item for key, item in raw.items() if item["verdict"] in (1, 2)}
    # s6 cache has its own schema and is compared directly with raw replay rows.
    s6_cache_rows = {}
    with args.s6_exact_cache.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s6verdict" or int(row[3]) != 6:
                raise ValueError(f"invalid s6 cache row {args.s6_exact_cache}:{line_no}: {row}")
            key = checked_key((int(row[1]), int(row[2])), 6)
            value = int(row[4])
            if value not in (1, 2) or key in s6_cache_rows:
                raise ValueError(f"non-exact/duplicate s6 cache row {key}: {row}")
            s6_cache_rows[key] = value
    if s6_cache_rows != {key: item["verdict"] for key, item in exact_rows.items()}:
        raise SystemExit("exact s6 cache differs from exact raw s6 replay rows")

    parents = {tuple(row["key"]): row for row in summary["parents"]}
    s5_wins = [key for key, row in parents.items() if row["outcome"] == "WIN"]
    if len(s5_wins) != 1:
        raise SystemExit(f"expected one exact s5 WIN derived from s6, got {s5_wins}")
    witness = s5_wins[0]
    checked_key(witness, 5)
    if witness not in children:
        raise SystemExit(f"s5 WIN witness is not a legal canonical child of s4 class: {witness}")
    s6_children = boundary(witness, 6)
    parent_summary = parents[witness]
    if parent_summary["child_count"] != len(s6_children):
        raise SystemExit("saved s5 summary child count differs from geometry")
    if len(s6_children) != len(set(s6_children)):
        raise SystemExit("duplicate canonical s6 children")
    missing_or_nonwin = [key for key in sorted(s6_children)
                         if key not in s6_cache_rows or s6_cache_rows[key] != 1]
    if missing_or_nonwin:
        raise SystemExit(f"s5 WIN lacks all-WIN exact s6 boundary: {missing_or_nonwin[:5]}")
    if parent_summary["counts"] != {"0": 0, "1": len(s6_children), "2": 0}:
        raise SystemExit(f"saved s5 boundary verdict counts differ: {parent_summary['counts']}")
    if {key: value for key, value in derived.items()} != {witness: 1}:
        raise SystemExit("derived s5 cache differs from the one geometry-verified s5 WIN")

    expected = dict(base)
    for key, value in derived.items():
        if key in expected and expected[key] != value:
            raise SystemExit(f"s5 verdict conflict while merging: {key}")
        expected[key] = value
    if merged != expected:
        raise SystemExit("merged exact s5 cache differs from base plus s6-derived exact s5 evidence")

    merged_partition = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    for child in children:
        value = merged.get(child)
        merged_partition[{1: "WIN", 2: "LOSS", None: "UNKNOWN"}[value]] += 1
    if merged_partition["WIN"] < 1:
        raise SystemExit("s4 class has no exact s5 WIN witness")
    witness_parents = {
        tuple(d4_canonical_key([p for p in points(witness) if p != removed]))
        for removed in points(witness)
    }
    if s4 not in witness_parents:
        raise SystemExit("s5 WIN witness fails reverse s4 incidence audit")

    root = {60, 27}
    if len(legal_after(root)) != 119:
        raise SystemExit("root {60,27} geometry does not have 119 legal third moves")

    def reply27_coverage(parent: tuple[int, int]) -> set[int]:
        covered = set()
        for first in legal_after(root):
            for second in legal_after(root | {first}):
                if second <= first:
                    continue
                if tuple(d4_canonical_key([60, 27, first, second])) == parent:
                    covered.update((first, second))
        return covered

    def class_status(cache: dict[tuple[int, int], int], s5_children: set[tuple[int, int]]) -> str:
        values = [cache.get(key) for key in s5_children]
        if 1 in values:
            return "WIN"
        if values and all(value == 2 for value in values):
            return "LOSS"
        return "UNKNOWN"

    coverage = reply27_coverage(s4)
    if not coverage:
        raise SystemExit(f"s4 class is not reachable after root {{60,27}}: {s4}")

    parent_impacts = []
    for parent in sorted(witness_parents):
        parent_coverage = reply27_coverage(parent)
        parent_children = boundary(parent, 5)
        if witness not in parent_children:
            raise SystemExit(f"reverse s4 incidence disagrees with forward geometry: {parent} -> {witness}")
        parent_impacts.append({
            "key": list(parent),
            "reachable_from_reply27": bool(parent_coverage),
            "coverage_vertices": sorted(parent_coverage),
            "canonical_s5_children": len(parent_children),
            "status_before_merge": class_status(base, parent_children),
            "status_after_merge": class_status(merged, parent_children),
            "witness_child": list(witness),
        })

    report = {
        "schema": "n11-dual-tight-s4-win-from-s6-geometry-audit-v1",
        "outcome_provenance": "The solver's exact s6 WIN results are trusted. This audit independently regenerates the complete s5 and s6 canonical safe boundaries, verifies every s6 child of the derived s5 WIN is exact WIN, and checks s5/s4 reverse incidence.",
        "root": [60, 27],
        "s4_class": {"key": list(s4), "status": "WIN", "coverage_vertices": sorted(coverage)},
        "complete_canonical_s5_boundary": {
            "child_count": len(children), "before_merge": dict(base_partition),
            "after_merge": dict(merged_partition),
            "children": [{"key": list(key), "status": {1: "WIN", 2: "LOSS", None: "UNKNOWN"}[merged.get(key)]}
                         for key in sorted(children)],
        },
        "s5_win_witness": {
            "key": list(witness), "child_count": len(s6_children),
            "complete_canonical_s6_boundary": "all exact WIN",
            "s6_children": [list(key) for key in sorted(s6_children)],
            "solver_rows": [{"key": list(key), **raw[key]} for key in sorted(s6_children)],
        },
        "unresolved_peer_s5": [
            {"key": row["key"], "outcome": row["outcome"], "counts": row["counts"],
             "unresolved_children": row["unresolved_children"]}
            for row in summary["parents"] if row["outcome"] == "UNKNOWN"
        ],
        "s5_witness_canonical_s4_parents": [list(key) for key in sorted(witness_parents)],
        "reply27_parent_class_impacts_from_witness": parent_impacts,
        "dispatch_consequence": "Once this s5 child was proven WIN, the enclosing s4 class was WIN and remaining unstarted s5 work for that class was stopped.",
        "status": {"class": "WIN", "root_60_27": "UNKNOWN", "empty_board": "UNKNOWN"},
        "sources": [{"path": str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/"),
                     "sha256": sha256(path), "bytes": path.stat().st_size}
                    for path in [args.base_s5_cache, args.merged_s5_cache, args.derived_s5_cache,
                                 args.s6_summary, args.s6_raw, args.s6_exact_cache, Path(__file__).resolve()]],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"DUAL_TIGHT_S4_S6_WIN_GEOMETRY_OK class={s4} s5={witness} s6={len(s6_children)}/{len(s6_children)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
