#!/usr/bin/env python3
"""Optimize the reply-27 s4 proof frontier after loading an exact s5 cache.

Every canonical s4 class is rebuilt from board geometry and classified from the
cache:
- WIN if at least one canonical s5 child is cached WIN;
- LOSS if every canonical s5 child is cached LOSS;
- UNKNOWN otherwise.

All vertices covered by proved LOSS classes are secured for free.  On the
remaining vertices, an exact MILP chooses UNKNOWN classes minimizing the
additive number of uncached s5 children.  The additive objective is a scheduling
proxy; the script also reports the exact distinct union of uncached s5 targets
for the selected repair.

No UNKNOWN cache entry is accepted and no game verdict is inferred merely from
the optimizer.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

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
                raise SystemExit(f"UNKNOWN/invalid cache verdict {verdict}: {key}")
            old = out.get(key)
            if old is not None and old != verdict:
                raise SystemExit(f"CONFLICT key={key} old={old} new={verdict}")
            out[key] = verdict
    return out


def build():
    base = {FIRST, R2}
    verts = legal_after(base)
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
    return set(verts), coverage, children


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    cache = load_cache(args.s5_cache)
    verts, coverage, children = build()

    status = {}
    unknown_children = {}
    for key, ss in children.items():
        vals = [cache.get(ch, 0) for ch in ss]
        if 1 in vals:
            status[key] = "WIN"
        elif all(v == 2 for v in vals):
            status[key] = "LOSS"
        else:
            status[key] = "UNKNOWN"
            unknown_children[key] = {ch for ch in ss if ch not in cache}

    secured = set()
    loss_keys = []
    for key, s in status.items():
        if s == "LOSS":
            loss_keys.append(key)
            secured.update(coverage[key])
    uncovered = sorted(verts - secured)

    selected = []
    res = None
    if uncovered:
        candidates = sorted(k for k, s in status.items() if s == "UNKNOWN")
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
        costs = np.array(
            [len(unknown_children[k]) for k in candidates],
            dtype=float,
        )
        res = milp(
            c=costs,
            constraints=LinearConstraint(
                A,
                lb=np.ones(len(uncovered)),
                ub=np.full(len(uncovered), np.inf),
            ),
            integrality=np.ones(len(candidates)),
            bounds=Bounds(0, 1),
            options={"presolve": True, "mip_rel_gap": 0.0},
        )
        if res.x is None or res.status != 0:
            raise SystemExit(
                f"MILP did not prove optimum: status={res.status} {res.message}"
            )
        selected = [
            candidates[i] for i, x in enumerate(res.x) if x > 0.5
        ]

    selected_unknown = (
        set().union(*(unknown_children[k] for k in selected))
        if selected else set()
    )
    repaired_coverage = set(secured)
    for key in selected:
        repaired_coverage.update(coverage[key])

    hist = Counter(status.values())
    out = {
        "root": [FIRST, R2],
        "cache_entries": len(cache),
        "class_status_counts": dict(sorted(hist.items())),
        "secured_vertices": len(secured),
        "uncovered_vertices_before_repair": len(uncovered),
        "repair_classes": len(selected),
        "repair_additive_unknown_s5": (
            int(round(res.fun)) if res is not None else 0
        ),
        "repair_unique_unknown_s5": len(selected_unknown),
        "covered_vertices_after_repair": len(repaired_coverage),
        "milp_status": int(res.status) if res is not None else 0,
        "milp_gap": float(res.mip_gap) if res is not None else 0.0,
        "proved_loss_classes": [list(k) for k in sorted(loss_keys)],
        "repair_selected": [
            {
                "key": list(k),
                "coverage": sorted(coverage[k]),
                "uncached_s5": len(unknown_children[k]),
            }
            for k in selected
        ],
        "claim": (
            "scheduling frontier only; selected UNKNOWN classes are not "
            "certificates until their remaining s5 children are proved LOSS"
        ),
    }
    assert repaired_coverage == verts
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print("CACHE_AWARE_REPLY27_COVER_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
