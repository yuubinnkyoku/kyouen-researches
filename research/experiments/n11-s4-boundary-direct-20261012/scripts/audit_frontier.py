#!/usr/bin/env python3
"""Independently regenerate every S4 child boundary and audit a merged S5 cache."""
from __future__ import annotations

import csv
import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
TARGET = (1297036692683752448, 0)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_cache(path: Path, quarantine):
    cache = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for lineno, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid cache row {lineno}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in quarantine:
                raise ValueError(f"invalid or quarantined cache evidence at row {lineno}: {key}")
            old = cache.get(key)
            if old is not None and old[0] != verdict:
                raise ValueError(f"cache conflict for {key}")
            cache[key] = (verdict, nodes if old is None else min(old[1], nodes))
    return cache


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=EXP / "output/frontier-after-second-batch.json")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    cache = load_cache(CURRENT, quarantined_cache_keys())
    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    if len(rows) != 3384:
        raise ValueError(f"geometry class count mismatch: {len(rows)}")
    counts, classes, universe, secured = Counter(), {}, set(), set()
    target_children = set()
    for row in rows:
        parent = tuple(row["key"])
        mask = parent[0] | (parent[1] << 64)
        if mask.bit_count() != 4 or board.canonical(mask) != mask:
            raise ValueError(f"invalid S4 key {parent}")
        generated = {(k & ((1 << 64) - 1), k >> 64) for k in board.children(mask)}
        stored = {tuple(k) for k in row["children"]}
        if generated != stored or len(stored) != len(row["children"]):
            raise ValueError(f"independent integer-geometry boundary mismatch for {parent}")
        vals = [cache.get(key, (0, 0))[0] for key in generated]
        status = "WIN" if 1 in vals else ("LOSS" if vals and all(v == 2 for v in vals) else "UNKNOWN")
        coverage = set(row["coverage"])
        universe |= coverage
        if status == "LOSS":
            secured |= coverage
        counts[status] += 1
        classes[parent] = {"status": status, "children": generated, "coverage": coverage}
        if parent == TARGET:
            target_children = generated
    remaining = sorted(universe - secured)
    target_counts = Counter(cache.get(k, (0, 0))[0] for k in target_children)
    if len(universe) != 119 or len(target_children) != 106:
        raise ValueError("reply27 third-move coverage or target S4 boundary changed unexpectedly")
    if remaining not in ([100, 108], []):
        raise ValueError(f"unexpected residual third moves: {remaining}")
    if not remaining and (classes[TARGET]["status"] != "LOSS" or target_counts != Counter({2: 106})):
        raise ValueError("119/119 coverage requires all 106 target S5 children to be exact LOSS")
    result = {
        "schema": "n11-s4-direct-s5-full-frontier-audit-v1",
        "exact_cache_path": str(CURRENT.relative_to(ROOT)), "exact_cache_sha256": sha(CURRENT),
        "exact_cache_rows": len(cache),
        "cache_verdict_counts": {"WIN": sum(v[0] == 1 for v in cache.values()), "LOSS": sum(v[0] == 2 for v in cache.values())},
        "geometry_path": str(GEOMETRY.relative_to(ROOT)), "geometry_sha256": sha(GEOMETRY),
        "independent_board_source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "all_3384_s4_boundaries_regenerated": True,
        "all_s4_class_count": len(classes), "all_s4_status_counts": dict(sorted(counts.items())),
        "third_move_count": len(universe), "secured_count": len(secured),
        "secured_third_move_ids": sorted(secured), "remaining_third_move_ids": remaining,
        "target_s4": list(TARGET), "target_s4_children": len(target_children),
        "target_s4_child_counts": {"LOSS": target_counts[2], "WIN": target_counts[1], "UNKNOWN": target_counts[0]},
        "target_s4_status": classes[TARGET]["status"],
        "trust": "S5 solver-trusted exact results; geometry independently regenerated. No terminal-only minimax proof is asserted.",
    }
    out = args.output if args.output.is_absolute() else ROOT / args.output
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
