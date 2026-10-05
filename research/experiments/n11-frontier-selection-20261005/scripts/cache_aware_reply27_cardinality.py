#!/usr/bin/env python3
"""Exact cardinality repair and LP-dual certificate for reply=27.

Classify every canonical s4 class from an exact s5 verdict cache.  All vertices
already covered by proved LOSS classes are secured.  WIN classes are forbidden.
On the remaining vertices, solve the minimum-cardinality cover by UNKNOWN
classes, then solve the fractional dual packing.

If the dual optimum equals the integer cover optimum, the output includes a
short independently checkable lower-bound certificate: nonnegative weights on
unsecured third-move vertices with every usable class having weight sum <= 1.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import csc_matrix

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402
import reply27_geometry_cache as geometry_cache  # noqa: E402

FIRST, R2 = 60, 27


def load_cache(path: Path):
    out = {}
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                continue
            key = (int(row[1]), int(row[2]))
            verdict = int(row[4])
            if verdict not in (1, 2):
                raise SystemExit(f"invalid cache verdict {verdict}: {key}")
            old = out.get(key)
            if old is not None and old != verdict:
                raise SystemExit(f"CONFLICT key={key} old={old} new={verdict}")
            out[key] = verdict
    return out


def build(cache_path=None):
    if cache_path is not None:
        return geometry_cache.as_cardinality(geometry_cache.load_cache(cache_path))
    base = {FIRST, R2}
    verts = set(legal_after(base))
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            groups[d4_canonical_key([FIRST, R2, a, b])].append((a, b))
    assert len(verts) == 119
    assert len(groups) == 3384
    coverage = {
        key: {x for a, b in edges for x in (a, b)}
        for key, edges in groups.items()
    }
    children = {}
    for key, edges in groups.items():
        ss = set()
        for a, b in edges:
            occ = base | {a, b}
            for z in legal_after(occ):
                ss.add(d4_canonical_key(list(occ | {z})))
        children[key] = ss
    return verts, coverage, children


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--geometry-cache", type=Path,
                    help="optional validated reply27 geometry index")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    cache = load_cache(args.s5_cache)
    verts, coverage, children = build(args.geometry_cache)
    status = {}
    for key, ss in children.items():
        vals = [cache.get(ch, 0) for ch in ss]
        if 1 in vals:
            status[key] = "WIN"
        elif vals and all(v == 2 for v in vals):
            status[key] = "LOSS"
        else:
            status[key] = "UNKNOWN"

    secured = set()
    loss_keys = []
    for key, st in status.items():
        if st == "LOSS":
            loss_keys.append(key)
            secured.update(coverage[key])
    uncovered = sorted(verts - secured)

    candidates = sorted(
        key for key, st in status.items()
        if st == "UNKNOWN" and (coverage[key] & set(uncovered))
    )
    selected = []
    dual_weights = {}
    ilp = lp = None

    if uncovered:
        vidx = {v: i for i, v in enumerate(uncovered)}
        rows = []
        cols = []
        for j, key in enumerate(candidates):
            for v in coverage[key]:
                if v in vidx:
                    rows.append(vidx[v])
                    cols.append(j)
        A = csc_matrix(
            (np.ones(len(rows)), (rows, cols)),
            shape=(len(uncovered), len(candidates)),
        )

        ilp = milp(
            c=np.ones(len(candidates)),
            constraints=LinearConstraint(
                A,
                lb=np.ones(len(uncovered)),
                ub=np.full(len(uncovered), np.inf),
            ),
            integrality=np.ones(len(candidates)),
            bounds=Bounds(0, 1),
            options={"presolve": True, "mip_rel_gap": 0.0},
        )
        if ilp.x is None or ilp.status != 0:
            raise SystemExit(
                f"cardinality MILP not optimal: {ilp.status} {ilp.message}"
            )
        selected = [
            candidates[i] for i, x in enumerate(ilp.x) if x > 0.5
        ]

        # Dual of fractional set cover:
        # max sum_v w_v, w>=0, sum_{v in class} w_v <=1.
        lp = linprog(
            c=-np.ones(len(uncovered)),
            A_ub=A.T,
            b_ub=np.ones(len(candidates)),
            bounds=[(0, None)] * len(uncovered),
            method="highs",
        )
        if lp.status != 0:
            raise SystemExit(f"dual LP failed: {lp.status} {lp.message}")
        for v, x in zip(uncovered, lp.x):
            if x > 1e-9:
                dual_weights[v] = str(Fraction(float(x)).limit_denominator(1000))

        # Recheck the rationalized certificate exactly.
        rat = {v: Fraction(s) for v, s in dual_weights.items()}
        dual_total = sum(rat.values(), Fraction(0))
        max_class = max(
            sum((rat.get(v, Fraction(0)) for v in coverage[k]), Fraction(0))
            for k in candidates
        )
        if max_class > 1:
            raise SystemExit(
                f"rationalized dual infeasible: max class weight {max_class}"
            )
    else:
        dual_total = Fraction(0)
        max_class = Fraction(0)

    repaired = set(secured)
    for key in selected:
        repaired.update(coverage[key])
    assert repaired == verts

    hist = Counter(status.values())
    ilp_opt = int(round(ilp.fun)) if ilp is not None else 0
    lp_opt = float(-lp.fun) if lp is not None else 0.0
    certificate_tight = dual_total == ilp_opt

    out = {
        "root": [FIRST, R2],
        "cache_entries": len(cache),
        "class_status_counts": dict(sorted(hist.items())),
        "secured_vertices": len(secured),
        "uncovered_vertices": len(uncovered),
        "minimum_additional_classes": ilp_opt,
        "fractional_dual_optimum": lp_opt,
        "rational_dual_total": str(dual_total),
        "dual_max_class_weight": str(max_class),
        "dual_certificate_matches_integer_optimum": certificate_tight,
        "dual_positive_weights": {
            str(v): w for v, w in sorted(dual_weights.items())
        },
        "selected_classes": [
            {
                "key": list(k),
                "coverage": sorted(coverage[k]),
            }
            for k in selected
        ],
        "proved_loss_classes": [list(k) for k in sorted(loss_keys)],
        "claim": (
            "exact minimum number of additional UNKNOWN s4 classes under "
            "the supplied exact s5 cache; UNKNOWN classes are work targets"
        ),
    }
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print("CACHE_AWARE_REPLY27_CARDINALITY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
