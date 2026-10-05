#!/usr/bin/env python3
"""Audit the representative-edge reduction for canonical s4 classes.

For each canonical four-stone D4 class under roots {60,0} and {60,27},
rebuild every raw edge and compare the complete SET of canonical legal s5
children.  D4 equivariance predicts equality inside every class; this finite
audit guards the concrete implementation and key convention.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]


def audit(first: int, r2: int):
    base = {first, r2}
    verts = legal_after(base)
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            groups[d4_canonical_key([first, r2, a, b])].append((a, b))

    bad = []
    edge_hist = Counter()
    child_hist = Counter()
    for key, edges in groups.items():
        edge_hist[len(edges)] += 1
        reference = None
        for a, b in edges:
            occ = base | {a, b}
            children = {
                d4_canonical_key(list(occ | {z}))
                for z in legal_after(occ)
            }
            if reference is None:
                reference = children
                child_hist[len(children)] += 1
            elif children != reference:
                bad.append({
                    "key": list(key),
                    "edge": [a, b],
                    "missing": len(reference - children),
                    "extra": len(children - reference),
                })
    return {
        "root": [first, r2],
        "vertices": len(verts),
        "classes": len(groups),
        "raw_edges": sum(len(v) for v in groups.values()),
        "raw_edges_per_class": dict(sorted(edge_hist.items())),
        "child_count_histogram": dict(sorted(child_hist.items())),
        "mismatching_classes": len(bad),
        "first_mismatches": bad[:5],
    }


def main():
    rows = [audit(60, 0), audit(60, 27)]
    assert rows[0]["vertices"] == 119
    assert rows[0]["classes"] == 3396
    assert rows[0]["raw_edges"] == 6894
    assert rows[1]["vertices"] == 119
    assert rows[1]["classes"] == 3384
    assert rows[1]["raw_edges"] == 6871
    assert all(r["mismatching_classes"] == 0 for r in rows)
    out = {
        "claim": "all raw edges in a canonical s4 class have identical canonical legal s5 child sets",
        "reason": "D4 equivariance; finite audit checks concrete n=11 implementation",
        "cases": rows,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("S4_CLASS_CHILD_INVARIANCE_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
