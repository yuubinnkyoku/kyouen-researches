#!/usr/bin/env python3
"""Independent finite verifier for the n=11 center/reply-27 frontier witness.

Checks:
* exact safe s4 edge/class counts from board geometry;
* a half-integral dual certificate proving every cover needs >=31 classes;
* the explicit 31-class witness covers all 119 third moves;
* the selected classes expand to exactly 2262 distinct canonical s5 roots;
* those roots have zero overlap with the 209 s5 roots already certified LOSS
  for the separate reply r2=0 lane.

This is a structural proof-frontier result only. It does not assert that the
31 selected reply-27 classes are LOSS.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WITNESS = HERE / "output/reply27-direct-union-cover.json"

FIRST = 60
R2 = 27
KNOWN_R2_0_LOSS = [
    (1152921504606846983, 0),
    (1152921504606848001, 4),
]


def classes_for(r2):
    base = {FIRST, r2}
    verts = legal_after(base)
    edges = set()
    for a in verts:
        for b in legal_after(base | {a}):
            if b == a:
                continue
            edges.add((min(a, b), max(a, b)))

    groups = defaultdict(list)
    coverage = defaultdict(set)
    for a, b in sorted(edges):
        key = d4_canonical_key([FIRST, r2, a, b])
        groups[key].append((a, b))
        coverage[key].update((a, b))
    return verts, edges, groups, coverage


def children_for(r2, key, groups):
    base = {FIRST, r2}
    out = set()
    for a, b in groups[key]:
        occ = base | {a, b}
        for z in legal_after(occ):
            out.add(d4_canonical_key([FIRST, r2, a, b, z]))
    return out


def main():
    doc = json.loads(WITNESS.read_text(encoding="utf-8"))
    assert doc["root"] == [FIRST, R2]

    verts, edges, groups, coverage = classes_for(R2)
    assert len(verts) == doc["n_vertices"] == 119
    assert len(edges) == doc["n_safe_edges"] == 6871
    assert len(groups) == doc["n_all_classes"] == 3384

    dual = set(doc["dual_positive_vertices"])
    assert len(dual) == doc["dual_numerator"] == 62
    max_num = 0
    for key in groups:
        num = len(coverage[key] & dual)
        max_num = max(max_num, num)
        assert num <= doc["dual_denominator"], (key, num)
    assert max_num == doc["max_dual_class_numerator"] == 2
    # Weight 1/2 on 62 vertices gives dual objective 31.
    assert doc["dual_numerator"] // doc["dual_denominator"] == 31

    selected = [tuple(x) for x in doc["classes"]]
    assert len(selected) == len(set(selected)) == 31
    for key in selected:
        assert key in groups, ("selected class missing", key)
    selected_cov = set().union(*(coverage[key] for key in selected))
    assert selected_cov == set(verts)
    # Feasible 31-class cover + dual lower bound 31 => exact optimum.
    assert doc["optimal_class_count"] == 31

    selected_s5 = set().union(*(children_for(R2, key, groups) for key in selected))
    assert len(selected_s5) == doc["selected_unique_s5"] == 2262

    _, _, g0, _ = classes_for(0)
    known = set().union(*(children_for(0, key, g0) for key in KNOWN_R2_0_LOSS))
    assert len(known) == doc["known_r2_0_loss_s5"] == 209
    overlap = selected_s5 & known
    assert len(overlap) == doc["overlap_with_known_r2_0_loss_s5"] == 0

    print("REPLY27_FRONTIER_VERIFIED")
    print("safe_edges=6871 classes=3384 dual=31 selected=31 coverage=119/119")
    print("selected_unique_s5=2262 known_r2_0_loss_s5=209 overlap=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
