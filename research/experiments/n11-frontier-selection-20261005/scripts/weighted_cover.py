#!/usr/bin/env python3
"""Optimize the n=11 center/corner 31-class proof frontier for s5 work.

This is an Othello-style proof-frontier experiment: keep the already-proved
minimum class count (31), but among those minimum covers minimize the additive
number of s5 child roots not already supplied by the verified base LOSS class.

The objective is deliberately an additive proxy.  After optimization we also
report the exact number of UNIQUE new canonical s5 roots in the selected cover.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix, vstack

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import (  # noqa: E402
    FIRST,
    R2,
    d4_canonical,
    legal_after,
    report,
)

OUT = Path(__file__).resolve().parents[1] / "output"
THEOREM_COVER = (
    ROOT / "research/experiments/n11-cover-duality/output/center-corner-cover.json"
)


def class_s5_children(raw_edges):
    out = set()
    base = {FIRST, R2}
    for a, b in raw_edges:
        occ4 = base | {a, b}
        for z in legal_after(occ4):
            out.add(d4_canonical([FIRST, R2, a, b, z]))
    return out


def load_theorem_cover():
    data = json.loads(THEOREM_COVER.read_text(encoding="utf-8"))
    case = next(c for c in data["cases"] if c["n"] == 11)
    return [tuple(row["key"]) for row in case["classes"]]


def solve():
    classes, raw = report(stream=open("/dev/null", "w", encoding="utf-8"))
    keys = sorted(classes)
    verts = sorted(set().union(*classes.values()))
    vidx = {v: i for i, v in enumerate(verts)}
    kidx = {k: i for i, k in enumerate(keys)}

    child = {k: class_s5_children(raw[k]) for k in keys}

    # Existing verified LOSS class {0,1,2,60}; all its s5 children are known LOSS.
    base_key = d4_canonical([FIRST, R2, 1, 2])
    known = set(child[base_key])

    rows, cols = [], []
    for j, k in enumerate(keys):
        for v in classes[k]:
            rows.append(vidx[v])
            cols.append(j)
    cover = csc_matrix(
        (np.ones(len(rows)), (rows, cols)), shape=(len(verts), len(keys))
    )

    # Exact 31-class cover, forcing reuse of the existing verified LOSS class.
    exact_count = csc_matrix(np.ones((1, len(keys))))
    force = csc_matrix(
        ([1.0], ([0], [kidx[base_key]])), shape=(1, len(keys))
    )
    A = vstack([cover, exact_count, force], format="csc")
    lb = np.concatenate([np.ones(len(verts)), [31.0, 1.0]])
    ub = np.concatenate(
        [np.full(len(verts), np.inf), [31.0, 1.0]]
    )

    costs = np.array([len(child[k] - known) for k in keys], dtype=float)
    res = milp(
        c=costs,
        constraints=LinearConstraint(A, lb=lb, ub=ub),
        integrality=np.ones(len(keys)),
        bounds=Bounds(0, 1),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    if res.x is None or res.status != 0:
        raise SystemExit(f"MILP did not prove optimum: status={res.status} {res.message}")

    selected = [keys[i] for i, x in enumerate(res.x) if x > 0.5]
    selected_children = set().union(*(child[k] for k in selected))
    selected_new = selected_children - known

    theorem = load_theorem_cover()
    theorem_children = set().union(*(child[k] for k in theorem))
    theorem_new = theorem_children - known

    result = {
        "scope": "n=11 root {60,0}; all 3396 safe canonical s4 classes",
        "known_cache_model": "all s5 children of verified LOSS class orbit {0,1,2,60}",
        "known_s5_roots": len(known),
        "class_count_constraint": 31,
        "weighted_objective": "sum over selected classes of uncached canonical s5 child count",
        "weighted_milp_status": int(res.status),
        "weighted_mip_gap": float(res.mip_gap),
        "weighted_additive_objective": int(round(res.fun)),
        "weighted_selected_classes": len(selected),
        "weighted_unique_s5_roots": len(selected_children),
        "weighted_unique_new_s5_roots": len(selected_new),
        "theorem_witness_classes": len(theorem),
        "theorem_unique_s5_roots": len(theorem_children),
        "theorem_unique_new_s5_roots": len(theorem_new),
        "unique_new_reduction": len(theorem_new) - len(selected_new),
        "unique_new_reduction_fraction": (
            (len(theorem_new) - len(selected_new)) / len(theorem_new)
        ),
        "weighted_selected": [
            {
                "key": list(k),
                "coverage": sorted(classes[k]),
                "s5_children": len(child[k]),
                "uncached_additive_cost": len(child[k] - known),
            }
            for k in selected
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "weighted-cover.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    solve()
