#!/usr/bin/env python3
"""Verify the direct-union 31-class n=11 center/corner proof frontier witness.

The witness is only a target set for future exact s5 solving. This verifier
checks geometry, D4 keys, full third-move coverage, the two already verified
LOSS classes, exclusion of the verified WIN class, and the exact union size of
all required canonical s5 roots. It does not infer any new s4 verdict.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import FIRST, R2, d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WITNESS = HERE / "output/direct-union-cover.json"
THEOREM = ROOT / "research/experiments/n11-cover-duality/output/center-corner-cover.json"


def build_classes():
    base = {FIRST, R2}
    verts = legal_after(base)
    groups = defaultdict(list)
    coverage = defaultdict(set)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([FIRST, R2, a, b])
            groups[key].append((a, b))
            coverage[key].update((a, b))
    return verts, groups, coverage


def children_for(key, groups):
    base = {FIRST, R2}
    out = set()
    for a, b in groups[key]:
        occ = base | {a, b}
        for z in legal_after(occ):
            out.add(d4_canonical_key([FIRST, R2, a, b, z]))
    return out


def main():
    doc = json.loads(WITNESS.read_text(encoding="utf-8"))
    verts, groups, coverage = build_classes()
    assert len(verts) == 119
    assert len(groups) == 3396

    selected = [tuple(row["key"]) for row in doc["selected"]]
    assert len(selected) == 31
    assert len(set(selected)) == 31
    for key in selected:
        assert key in groups, ("missing class", key)

    forced = [tuple(x) for x in doc["forced_known_loss_keys"]]
    forbidden = tuple(doc["forbidden_known_win_key"])
    assert all(k in selected for k in forced)
    assert forbidden not in selected

    selected_cov = set().union(*(coverage[k] for k in selected))
    assert selected_cov == set(verts)

    child = {}
    needed = set(selected) | set(forced)
    for key in needed:
        child[key] = children_for(key, groups)
    known = set().union(*(child[k] for k in forced))
    all_selected = set().union(*(child[k] for k in selected))
    unknown = all_selected - known

    assert len(known) == doc["known_s5"] == 209
    assert len(all_selected) == doc["selected_unique_s5"] == 2528
    assert len(unknown) == doc["unique_unknown_s5"] == 2319

    theorem = json.loads(THEOREM.read_text(encoding="utf-8"))
    case = next(c for c in theorem["cases"] if c["n"] == 11)
    theorem_keys = [d4_canonical_key(row["key"]) for row in case["classes"]]
    for key in theorem_keys:
        if key not in child:
            child[key] = children_for(key, groups)
    theorem_union = set().union(*(child[k] for k in theorem_keys))
    theorem_unknown = theorem_union - known
    assert len(theorem_keys) == 31
    assert set().union(*(coverage[k] for k in theorem_keys)) == set(verts)
    assert len(theorem_union) == 3336
    assert len(theorem_unknown) == 3229

    print("DIRECT_UNION_WITNESS_VERIFIED")
    print("classes=31 coverage=119/119")
    print("known_s5=209 selected_unique_s5=2528 unique_unknown_s5=2319")
    print("theorem_unknown_s5=3229 reduction=910 fraction=%.8f" % (910 / 3229.0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
