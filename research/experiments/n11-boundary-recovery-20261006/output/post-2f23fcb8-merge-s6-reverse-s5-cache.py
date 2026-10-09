#!/usr/bin/env python3
"""Merge audited S6-loss-derived S5 rows while preserving solver node counts."""

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
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_cache(path: Path) -> dict[tuple[int, int], tuple[int, int]]:
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as fp:
        for line_no, row in enumerate(csv.reader(fp), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact S5 row {path}:{line_no}: {row}")
            key, verdict, nodes = (int(row[1]), int(row[2])), int(row[4]), int(row[5])
            lo, hi = key
            points = {p for p in range(64) if lo >> p & 1}
            points.update(64 + p for p in range(57) if hi >> p & 1)
            if (len(points) != 5 or has_forbidden_quad(points)
                    or tuple(d4_canonical_key(points)) != key or verdict not in (1, 2)
                    or nodes < 0 or key in result):
                raise SystemExit(f"unsafe, noncanonical, duplicate, or inexact S5 row: {path}:{line_no}: {row}")
            result[key] = (verdict, nodes)
    return result


def counts(cache: dict[tuple[int, int], tuple[int, int]]) -> dict[str, int]:
    verdicts = Counter(value[0] for value in cache.values())
    return {"rows": len(cache), "WIN": verdicts[1], "LOSS": verdicts[2], "conflict": 0}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--delta", type=Path, required=True)
    ap.add_argument("--reverse-audit", type=Path, required=True)
    ap.add_argument("--s6-raw", type=Path, required=True)
    ap.add_argument("--s6-manifest", type=Path, required=True)
    ap.add_argument("--out-cache", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()

    base, delta = parse_cache(args.base), parse_cache(args.delta)
    audit = json.loads(args.reverse_audit.read_text(encoding="utf-8"))
    comparison = audit.get("cache_comparison", {})
    if (audit.get("cache_out", {}).get("sha256") != sha256(args.delta)
            or audit.get("cache_out", {}).get("rows") != len(delta)
            or comparison.get("new") != len(delta)
            or comparison.get("conflicts") or comparison.get("internal_conflict")
            or comparison.get("opposite_verdict")):
        raise SystemExit("reverse audit does not bind a conflict-free exact S5 delta")
    if any(verdict != 2 or nodes != 0 for verdict, nodes in delta.values()):
        raise SystemExit("reverse-derived S5 delta must contain LOSS rows with zero S5 solver nodes")
    witnessed = {
        tuple(item["key"])
        for item in audit.get("reverse_parents", {}).get("all_canonical_safe_parent_witnesses", [])
        if item.get("loss_witness_keys")
    }
    if not set(delta) <= witnessed:
        raise SystemExit("reverse-derived cache contains a parent without an exact LOSS S6 witness")
    overlap = set(base) & set(delta)
    conflicts = [key for key in overlap if base[key][0] != delta[key][0]]
    if conflicts:
        raise SystemExit(f"exact S5 verdict conflict with base cache: {sorted(conflicts)}")
    if overlap:
        raise SystemExit(f"reverse delta repeats existing cache keys: {sorted(overlap)}")

    merged = dict(base)
    merged.update(delta)
    args.out_cache.parent.mkdir(parents=True, exist_ok=True)
    with args.out_cache.open("w", newline="", encoding="utf-8") as fp:
        fp.write("# exact s5 cache: base plus geometry-audited exact S6 LOSS reverse propagation\n")
        writer = csv.writer(fp, lineterminator="\n")
        for (lo, hi), (verdict, nodes) in sorted(merged.items()):
            writer.writerow(("s5verdict", lo, hi, 5, verdict, nodes))
    receipt = {
        "schema": "n11-s6-reverse-s5-cache-merge-receipt-v1",
        "base": {"path": str(args.base), "sha256": sha256(args.base), **counts(base)},
        "delta": {"path": str(args.delta), "sha256": sha256(args.delta), **counts(delta)},
        "reverse_audit": {"path": str(args.reverse_audit), "sha256": sha256(args.reverse_audit),
                          "s6_loss_unique": audit.get("s6", {}).get("unique_loss_keys"),
                          "all_safe_parent_count": audit.get("reverse_parents", {}).get("all_canonical_safe_parent_count"),
                          "reply27_relevant_parent_count": audit.get("reverse_parents", {}).get("reply27_relevant_parent_count")},
        "s6_raw": {"path": str(args.s6_raw), "sha256": sha256(args.s6_raw)},
        "s6_source_manifest": {"path": str(args.s6_manifest), "sha256": sha256(args.s6_manifest)},
        "merged": {"path": str(args.out_cache), "sha256": sha256(args.out_cache), **counts(merged)},
        "overlap_keys": 0,
        "verdict_conflicts": 0,
        "unknown_rows_merged": 0,
        "reverse_derived_loss_rows": len(delta),
    }
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
