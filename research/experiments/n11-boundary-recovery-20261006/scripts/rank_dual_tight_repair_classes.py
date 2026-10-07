#!/usr/bin/env python3
"""Rank dual-tight classes in the current exact-cache additive repair.

This is a scheduling/materialization helper only. It rebuilds the geometry and
uses exact s5 cache verdicts; it does not infer outcomes for UNKNOWN classes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FRONTIER_SCRIPTS = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
EDGE_SCRIPTS = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(FRONTIER_SCRIPTS))
sys.path.insert(0, str(EDGE_SCRIPTS))

import cache_aware_reply27_cover as cover  # noqa: E402
from dfpn_edge_classes import legal_after  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--repair-json", type=Path, required=True)
    ap.add_argument("--cardinality-json", type=Path, required=True)
    ap.add_argument("--targets-out", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sources-out", type=Path, required=True)
    args = ap.parse_args()

    cache = cover.load_cache(args.s5_cache)
    verts, coverage, children = cover.build()
    repair = json.loads(args.repair_json.read_text(encoding="utf-8"))
    cardinality = json.loads(args.cardinality_json.read_text(encoding="utf-8"))
    if len(verts) != 119 or len(children) != 3384:
        raise SystemExit("unexpected reply27 geometry cardinality")

    dual = {int(v): float(w) for v, w in cardinality["dual_positive_weights"].items()}
    selected_rows = repair["repair_selected"]
    candidates = []
    for item in selected_rows:
        key = tuple(map(int, item["key"]))
        ss = children.get(key)
        if ss is None:
            raise SystemExit(f"repair class absent from geometry: {key}")
        vals = {ch: cache.get(ch, 0) for ch in ss}
        if 1 in vals.values():
            raise SystemExit(f"repair class is exact WIN: {key}")
        unknown = sorted(ch for ch, verdict in vals.items() if verdict == 0)
        known_loss = sum(verdict == 2 for verdict in vals.values())
        dual_vertices = sorted(v for v in coverage[key] if v in dual)
        dual_weight = sum(dual[v] for v in coverage[key] if v in dual)
        if abs(dual_weight - 1.0) > 1e-9 or len(dual_vertices) != 1:
            raise SystemExit(
                f"selected minimum-cover class is not dual-tight: {key}, "
                f"dual_vertices={dual_vertices}, weight={dual_weight}"
            )
        legal_counts = [len(legal_after(cover.occupied_from_key(ch))) for ch in unknown]
        candidates.append({
            "key": list(key),
            "coverage": sorted(coverage[key]),
            "dual_vertex": dual_vertices[0],
            "dual_weight": str(int(dual_weight)),
            "canonical_s5_children": len(ss),
            "known_loss_s5": known_loss,
            "unknown_s5": len(unknown),
            "unknown_s5_legal_count_min": min(legal_counts, default=0),
            "unknown_s5_legal_count_max": max(legal_counts, default=0),
            "_unknown": unknown,
        })

    candidates.sort(key=lambda x: (
        x["unknown_s5"], x["unknown_s5_legal_count_max"], x["key"]
    ))
    if not candidates:
        raise SystemExit("no selected dual-tight classes")
    best = candidates[0]
    args.targets_out.parent.mkdir(parents=True, exist_ok=True)
    with args.targets_out.open("w", newline="", encoding="utf-8") as fp:
        fp.write("# dual-tight reply27 class completion targets; UNKNOWN only; no verdict asserted\n")
        writer = csv.writer(fp, lineterminator="\n")
        for seq, key in enumerate(best["_unknown"]):
            legal = len(legal_after(cover.occupied_from_key(key)))
            writer.writerow(["reply27-dual-tight", seq, 5, key[0], key[1], legal, 0, 0, 0, 0, 0])

    clean = []
    for rank, row in enumerate(candidates, 1):
        clean.append({k: v for k, v in row.items() if k != "_unknown"} | {"rank": rank})
    result = {
        "root": [60, 27],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual_total": cardinality["rational_dual_total"],
        "dual_certificate_matches_integer_optimum": cardinality["dual_certificate_matches_integer_optimum"],
        "ranking_rule": "selected additive-optimum classes; dual-tight only; unknown s5 count, then max legal count, then canonical key",
        "ranking": clean,
        "next_target": clean[0] | {"targets_csv": str(args.targets_out)},
        "claim": "scheduling order only; UNKNOWN remains UNKNOWN until exact proof",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_paths = [p.resolve() for p in [
        args.s5_cache,
        args.repair_json,
        args.cardinality_json,
        Path(__file__).resolve(),
        FRONTIER_SCRIPTS / "cache_aware_reply27_cover.py",
        FRONTIER_SCRIPTS / "cache_aware_reply27_cardinality.py",
        EDGE_SCRIPTS / "dfpn_edge_classes.py",
    ]]
    source_doc = {
        "schema": "n11-dual-tight-repair-ranking-sources-v1",
        "sources": [
            {"path": str(p.relative_to(ROOT)), "sha256": sha256(p)}
            for p in source_paths
        ],
        "generated": [
            {"path": str(p.resolve().relative_to(ROOT)), "sha256": sha256(p)}
            for p in [args.targets_out, args.out]
        ],
    }
    args.sources_out.parent.mkdir(parents=True, exist_ok=True)
    args.sources_out.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("DUAL_TIGHT_REPAIR_RANKING_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
