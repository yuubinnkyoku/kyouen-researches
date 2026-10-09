#!/usr/bin/env python3
"""Materialize the exact UNKNOWN portion of the round-4 S4 boundary from round-3 evidence."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after

out = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
boundary_path = out / "post-9681c588-next98-round3-class-boundary-audit.json"
cache_path = out / "post-9681c588-next98-round3-merged-s5.cache"
targets_path = out / "post-9681c588-next98-round4-full-unknown-targets.csv"
class_key = (1152921504741065728, 68719476736)
audit = json.loads(boundary_path.read_text(encoding="utf-8"))
assert tuple(audit["class"]["key"]) == class_key
children = {tuple(row["key"]): row["verdict"] for row in audit["boundary"]["children"]}
assert len(children) == audit["boundary"]["canonical_children"] == 102
cache = {}
with cache_path.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        if not row or row[0].lstrip().startswith("#"):
            continue
        assert len(row) == 6 and row[0] == "s5verdict" and int(row[3]) == 5
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        assert verdict in (1, 2) and key not in cache
        cache[key] = verdict
for key, verdict in children.items():
    assert cache.get(key) == verdict
points = tuple(i for i in range(121) if (
    (i < 64 and class_key[0] >> i & 1) or
    (i >= 64 and class_key[1] >> (i - 64) & 1)
))
assert len(points) == 4 and not has_forbidden_quad(points)
unknown = sorted(key for key, verdict in children.items() if verdict is None)
assert len(unknown) == 63
rows = [["# Canonical UNKNOWN s5 children before the round-4 probe; ordering has no proof meaning"]]
for i, key in enumerate(unknown, 1):
    pts = tuple(j for j in range(121) if (
        (j < 64 and key[0] >> j & 1) or
        (j >= 64 and key[1] >> (j - 64) & 1)
    ))
    assert len(pts) == 5 and not has_forbidden_quad(pts)
    assert tuple(d4_canonical_key(pts)) == key
    legal_count = len(legal_after(set(pts)))
    rows.append(["reply27-dual-tight-full", i, 5, key[0], key[1], legal_count, 0, 0, 0, 0, 0])
with targets_path.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f, lineterminator="\n").writerows(rows)
print(f"MATERIALIZED_ROUND4_UNKNOWN_TARGETS class={class_key} children={len(children)} unknown={len(unknown)}")
